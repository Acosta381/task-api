from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

if TYPE_CHECKING:
    from models.user import User


class Task(Base):
    __tablename__ = 'tasks'

    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    title : Mapped[str] = mapped_column(String(255))
    description : Mapped[str | None] = mapped_column(default=None)
    completed : Mapped[bool] = mapped_column(default=False)
    created_at : Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at : Mapped[datetime] = mapped_column(
        server_default = func.now(),
        onupdate = func.now()
    )

    owner_id : Mapped[int] = mapped_column(ForeignKey('users.id'))

    owner : Mapped['User'] = relationship(back_populates='tasks')

    def __repr__(self) -> str:
        return f"<Task(id = {self.id}, title = {self.title!r})>"