from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from crud.task import create_task, delete_task, get_task, get_tasks, update_task
from database import get_db
from models.user import User
from schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.get('/', response_model=list[TaskResponse])
async def read_tasks(
    db : Annotated[AsyncSession, Depends(get_db)],
    current_user : Annotated[User, Depends(get_current_user)],
    skip : int = 0,
    limit : int = 100,
    completed : bool | None = None,
    sort_by : Literal['title', 'created_at', 'completed'] = 'created_at',
    order : Literal['asc','desc'] = 'desc'
):
    tasks = await get_tasks(db, current_user.id, skip, limit, completed,sort_by, order)

    return tasks

@router.get('/{task_id}', response_model=TaskResponse)
async def read_task(
    db : Annotated[AsyncSession, Depends(get_db)],
    task_id : int,
    current_user : Annotated[User, Depends(get_current_user)]
):
    task = await get_task(db, task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )

    return task

@router.post('/', response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    db : Annotated[AsyncSession, Depends(get_db)],
    task : TaskCreate,
    current_user : Annotated[User, Depends(get_current_user)],
):
    return await create_task(db, task, current_user.id)

@router.patch('/{task_id}', response_model=TaskResponse)
async def update_existing_task(
    db : Annotated[AsyncSession, Depends(get_db)],
    task_id : int,
    task_update : TaskUpdate,
    current_user : Annotated[User, Depends(get_current_user)]
):
    task = await get_task(db, task_id)

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')

    if task.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')

    update_data = await update_task(db,task_id,task_update)

    
    if update_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')

    return update_data

@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(
    db : Annotated[AsyncSession, Depends(get_db)],
    task_id : int,
    current_user : Annotated[User, Depends(get_current_user)]
):
    task = await get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )    

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    
    deleted_data = await delete_task(db, task_id)

    if deleted_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    