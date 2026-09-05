async def test_register_user(client):
    response = await client.post(
        '/users/register',
        json = {
            'email':'test@example.com',
            'password':'testpassword12'
        }
    )

    assert response.status_code == 201
    assert response.json()['email'] == 'test@example.com'
    assert 'hashed_password' not in response.json()

async def test_login_auth(client):
    response1 = await client.post(
        '/users/register',
        json = {
            'email':'test@example.com',
            'password':'testpassword12'
        }
    )

    assert response1.status_code == 201

    response2 = await client.post(
        '/auth/login',
        data = {
            'username':'test@example.com',
            'password':'testpassword12'
        }
    )

    assert response2.status_code == 200
    assert 'access_token' in response2.json()
    assert 'refresh_token' in response2.json()

async def test_login_wrong_password(client):
    response1 = await client.post(
        '/users/register',
        json = {
            'email': 'test2@example.com',
            'password': 'testpassword123'
        }
    )

    assert response1.status_code == 201

    response2 = await client.post(
        '/auth/login',
        data = {
            'username':'test2@example.com',
            'password':'testpassword123 '
        }
    )

    assert response2.status_code == 401

async def test_register_duplicate_email(client):
    response1 = await client.post(
        '/users/register',
        json = {
            'email': 'test1@example.com',
            'password': 'testpassword1'
        }
    )

    assert response1.status_code == 201

    response2 = await client.post(
    '/users/register',
    json = {
        'email': 'test1@example.com',
        'password': 'testpassword123'
        }
    )

    assert response2.status_code == 400

