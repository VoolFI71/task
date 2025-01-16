from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hash_password: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[int] = mapped_column(Integer, default=0) 

