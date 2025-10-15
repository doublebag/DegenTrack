from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    hashed_password: str
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WatchlistItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    coin_id: str
    symbol: Optional[str] = None
    added_at: datetime = Field(default_factory=datetime.utcnow)

class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    coin_id: str
    direction: str
    threshold: float
    active: bool = True
    last_triggered_at: Optional[datetime] = None
