from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.schemas import TaskCreate
from app.models import TodoTask
from app.crud import create_task, get_tasks, delete_task, delete_all_tasks

# Initialize tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def homepage(request: Request, db: Session = Depends(get_db)):
    tasks = get_tasks(db)
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})


@app.post("/add_task")
def add_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db),
):
    task = TaskCreate(title=title, description=description)
    create_task(db, task)
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete_task/{task_id}")
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    delete_task(db, task_id)
    return RedirectResponse(url="/", status_code=303)


@app.post("/clear_tasks")
def clear_tasks(db: Session = Depends(get_db)):
    delete_all_tasks(db)
    return RedirectResponse(url="/", status_code=303)
