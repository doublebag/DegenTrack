import os
from sqlmodel import SQLModel, create_engine, Session
DB_FILE = os.getenv("DATABASE_URL", "sqlite:///./degentracks.db")
connect_args = {}
if DB_FILE.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
engine = create_engine(DB_FILE, echo=False, connect_args=connect_args)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session
