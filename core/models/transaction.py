from sqlalchemy import Integer, String, Column, ForeignKey, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from datetime import datetime

class Transaction(Base):
    from_user = Column(String, ForeignKey('users.username'), nullable=False)
    to_user = Column(String, ForeignKey('users.username'), nullable=False)
    from_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    to_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
