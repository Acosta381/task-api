async def test_create_path_requires_auth(client):
    response_create_task = await client.post(
        '/tasks/',
        json = {
            'title':'Test task',
            'description':'test'
        }
    )

    assert response_create_task.status_code == 401

async def test_create_task_success(client):
    response_register_user = await client.post(
        '/users/register',
        json = {
            'email':'test@example.com',
            'password':'testpassword12'
        }
    )

    assert response_register_user.status_code == 201

    user = await client.post(
        '/auth/login',
        data = {
            'username':'test@example.com',
            'password':'testpassword12'
        }
    )

    assert user.status_code == 200

    access_token = user.json()['access_token']

    headers = {'Authorization':f'Bearer {access_token}'}

    user_response = await client.post(
        '/tasks/',
        json = {
            'title':'Test task',
            'description':'test',
        },
        headers = headers
    )

    assert user_response.status_code == 201

async def test_read_task_not_found(client):
    response_register_user = await client.post(
        '/users/register',
        json = {
            'email':'test@example.com',
            'password':'testpassword12'
        }
    )

    assert response_register_user.status_code == 201

    user = await client.post(
        '/auth/login',
        data = {
            'username':'test@example.com',
            'password':'testpassword12'
        }
    )

    assert user.status_code == 200

    access_token = user.json()['access_token']

    headers = {'Authorization':f'Bearer {access_token}'}

    response_task_not_found = await client.get(
        '/tasks/999',
        headers = headers
    )

    assert response_task_not_found.status_code == 404

async def test_read_tasks_returns_only_own_tasks(client):
    response_register_user1 = await client.post(
        '/users/register',
        json = {
            'email':'user1@example.com',
            'password':'user1password12'
        }
    )

    assert response_register_user1.status_code == 201

    user1 = await client.post(
        '/auth/login',
        data = {
            'username':'user1@example.com',
            'password':'user1password12'
        }
    )

    assert user1.status_code == 200

    token_user1 = user1.json()['access_token']

    headers_user1 = {'Authorization':f'Bearer {token_user1}'}

    response_user1 = await client.post(
        '/tasks/',
        json = {
            'title':'Test user1',
            'description':'test user1',
        },
        headers = headers_user1
    )

    assert response_user1.status_code == 201

    response_register_user2 = await client.post(
        '/users/register',
        json = {
            'email':'user2@example.com',
            'password':'user2password12'
        }
    )

    assert response_register_user2.status_code == 201

    user2 = await client.post(
        '/auth/login',
        data = {
            'username':'user2@example.com',
            'password':'user2password12'
        }
    )

    assert user2.status_code == 200

    token_user2 = user2.json()['access_token']

    headers_user2 = {'Authorization':f'Bearer {token_user2}'}

    response_user2 = await client.post(
        '/tasks/',
        json = {
            'title':'Test user2',
            'description':'test user2',
        },
        headers = headers_user2
    )

    assert response_user2.status_code == 201

    response_user1 = await client.get(
        '/tasks/',
        headers = headers_user1
    )

    assert response_user1.status_code == 200

    tasks1 = response_user1.json()

    assert tasks1[0]['title'] == 'Test user1'

    response_user2 = await client.get(
        '/tasks/',
        headers = headers_user2
    )

    assert response_user2.status_code == 200

    tasks2 = response_user2.json()

    assert tasks2[0]['title'] == 'Test user2'

async def test_update_task_sucess(client):
    response_register_user = await client.post(
        '/users/register',
        json = {
            'email':'user@example.com',
            'password':'userpassword12'
        }
    )

    assert response_register_user.status_code == 201

    user = await client.post(
        '/auth/login',
        data = {
            'username':'user@example.com',
            'password':'userpassword12'
        }
    )

    assert user.status_code == 200

    access_token = user.json()['access_token']

    headers = {'Authorization':f'Bearer {access_token}'}

    response_user = await client.post(
        '/tasks/',
        json = {
            'title':'Test user1',
            'description':'test user1',
        },
        headers = headers
    )

    assert response_user.status_code == 201

    task_id = response_user.json()['id']

    response_patch = await client.patch(
        f'/tasks/{task_id}',
        json = {
            'title': 'Patched Testing title'
        },
        headers = headers
    )

    assert response_patch.status_code == 200
    assert response_patch.json()['title'] == 'Patched Testing title'

async def test_cannot_update_other_users_tasks(client):
    response_register_user1 = await client.post(
        '/users/register',
        json = {
            'email':'user1@example.com',
            'password':'user1password12'
        }
    )

    assert response_register_user1.status_code == 201

    user1 = await client.post(
        '/auth/login',
        data = {
            'username':'user1@example.com',
            'password':'user1password12'
        }
    )

    assert user1.status_code == 200

    token_user1 = user1.json()['access_token']

    headers_user1 = {'Authorization':f'Bearer {token_user1}'}

    response_user1 = await client.post(
        '/tasks/',
        json = {
            'title':'Test user1',
            'description':'test user1',
        },
        headers = headers_user1
    )

    assert response_user1.status_code == 201

    response_register_user2 = await client.post(
        '/users/register',
        json = {
            'email':'user2@example.com',
            'password':'user2password12'
        }
    )

    assert response_register_user2.status_code == 201

    user2 = await client.post(
        '/auth/login',
        data = {
            'username':'user2@example.com',
            'password':'user2password12'
        }
    )

    assert user2.status_code == 200

    token_user2 = user2.json()['access_token']

    headers_user2 = {'Authorization':f'Bearer {token_user2}'}

    response_user2 = await client.post(
        '/tasks/',
        json = {
            'title':'Test user2',
            'description':'test user2',
        },
        headers = headers_user2
    )

    assert response_user2.status_code == 201

    task_id = response_user2.json()['id']

    response_updates = await client.patch(
        f'/tasks/{task_id}',
        json = {
            'title':'Test from user 2',
            'description': 'Description from user 2'
        },
        headers = headers_user1
    )

    assert response_updates.status_code == 404

async def test_delete_task_success(client):
    response_register_user = await client.post(
        '/users/register',
        json = {
            'email':'user@example.com',
            'password':'userpassword12'
        }
    )

    assert response_register_user.status_code == 201

    user = await client.post(
        '/auth/login',
        data = {
            'username':'user@example.com',
            'password':'userpassword12'
        }
    )

    assert user.status_code == 200

    access_token = user.json()['access_token']

    headers = {'Authorization':f'Bearer {access_token}'}

    response_user = await client.post(
        '/tasks/',
        json = {
            'title':'Test user',
            'description':'test user',
        },
        headers = headers
    )

    assert response_user.status_code == 201

    task_id = response_user.json()['id']

    response_delete = await client.delete(
        f'/tasks/{task_id}',
        headers = headers
    )

    assert response_delete.status_code == 204

    response_deleted_task = await client.get(
        f'/tasks/{task_id}',
        headers = headers
    )

    assert response_deleted_task.status_code == 404

async def test_cannot_delete_other_users_task(client):
    response_register_user1 = await client.post(
        '/users/register',
        json = {
            'email':'user1@example.com',
            'password':'user1password12'
        }
    )

    assert response_register_user1.status_code == 201

    user1 = await client.post(
        '/auth/login',
        data = {
            'username':'user1@example.com',
            'password':'user1password12'
        }
    )

    assert user1.status_code == 200

    token_user1 = user1.json()['access_token']

    headers_user1 = {'Authorization':f'Bearer {token_user1}'}

    response_user1 = await client.post(
        '/tasks/',
        json = {
            'title':'Test user1',
            'description':'test user1',
        },
        headers = headers_user1
    )

    assert response_user1.status_code == 201

    response_register_user2 = await client.post(
        '/users/register',
        json = {
            'email':'user2@example.com',
            'password':'user2password12'
        }
    )

    assert response_register_user2.status_code == 201

    user2 = await client.post(
        '/auth/login',
        data = {
            'username':'user2@example.com',
            'password':'user2password12'
        }
    )

    assert user2.status_code == 200

    token_user2 = user2.json()['access_token']

    headers_user2 = {'Authorization':f'Bearer {token_user2}'}

    response_user2 = await client.post(
        '/tasks/',
        json = {
            'title':'Test user2',
            'description':'test user2',
        },
        headers = headers_user2
    )

    assert response_user2.status_code == 201

    task_id = response_user2.json()['id']

    response_deleted = await client.delete(
        f'/tasks/{task_id}',
        headers = headers_user1
    )

    assert response_deleted.status_code == 404