from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from models.user import User
from schemas.user import UserCreate


async def get_user_by_email(db : AsyncSession, email : str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))

    return result.scalar_one_or_none()

async def create_user(db : AsyncSession, user : UserCreate) -> User:
    hashed_password = hash_password(user.password)

    new_user = User(email = user.email, hashed_password = hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user