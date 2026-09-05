from collections.abc import (
    Sequence,
)
from typing import Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.task import Task
from schemas.task import TaskCreate, TaskUpdate


async def get_task(db : AsyncSession, task_id : int) -> Task | None:
    result = await db.execute(select(Task).where(Task.id == task_id))

    return result.scalar_one_or_none()

async def get_tasks(db : AsyncSession,
                    owner_id : int,
                    skip : int = 0,
                    limit : int = 100,
                    completed : bool | None = None,
                    sort_by : Literal['title', 'created_at','completed'] = 'created_at',
                    order : Literal['asc','desc'] = 'desc'
) -> Sequence[Task]: #Basically Sequence represents every general type but List[Task] is also correct
    stmt = select(Task).where(Task.owner_id == owner_id)

    if completed is not None:
        stmt = stmt.where(Task.completed == completed)

    column = getattr(Task, sort_by)

    if order == 'desc':
        stmt = stmt.order_by(column.desc())
    else:
        stmt = stmt.order_by(column.asc())

    stmt = stmt.offset(skip).limit(limit)

    result = await db.execute(stmt)

    return result.scalars().all()

async def create_task(db: AsyncSession, task : TaskCreate, owner_id : int) -> Task:
    new_task = Task(**task.model_dump(), owner_id = owner_id)

    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task

async def update_task(db : AsyncSession, task_id : int, task_update : TaskUpdate) -> Task | None:
    existing_task = await get_task(db, task_id)

    if existing_task is None:
        return None

    update_data = task_update.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(existing_task,key,value)

    await db.commit()
    await db.refresh(existing_task)

    return existing_task

async def delete_task(db : AsyncSession, task_id : int) -> bool | None:
    existing_data = await get_task(db, task_id)

    if existing_data is None:
        return None

    await db.delete(existing_data)
    await db.commit()

    return True