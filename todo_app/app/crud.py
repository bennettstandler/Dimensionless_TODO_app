from sqlalchemy.orm import Session
from app.models import TodoTask
from app.schemas import TaskCreate

def create_task(db: Session, task: TaskCreate):
    db_task = TodoTask(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TodoTask).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, task: TaskCreate):
    db_task = db.query(TodoTask).filter(TodoTask.id == task_id).first()
    if db_task:
        for key, value in task.dict().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(TodoTask).filter(TodoTask.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

def delete_all_tasks(db: Session):
    db.query(TodoTask).delete()
    db.commit()
