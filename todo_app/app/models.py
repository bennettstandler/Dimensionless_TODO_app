from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base

class TodoTask(Base):
    __tablename__ = "todo_tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
