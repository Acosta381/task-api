from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import create_user, get_user_by_email
from database import get_db
from schemas.user import UserCreate, UserResponse

router = APIRouter(prefix='/users', tags = ['users'])

@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(db : Annotated[AsyncSession, Depends(get_db)], user : UserCreate):
    existing_user = await get_user_by_email(db, user.email)

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail = 'Email already registered'
        )

    return await create_user(db, user)