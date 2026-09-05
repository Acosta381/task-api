from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.task import Task

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    email : Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password : Mapped[str] = mapped_column(String(255))
    created_at : Mapped[datetime] = mapped_column(
        server_default= func.now()
    )

    tasks : Mapped[list['Task']] = relationship(back_populates='owner')

    def __repr__(self) -> str:
        return f'<User({self.id}, {self.email!r})>'