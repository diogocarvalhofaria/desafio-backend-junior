from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi_pagination import Page, Params

from app.database import get_db
from app.services.task_service import TaskService
from app.schemas.task import Task, TaskCreate, TaskUpdate, TaskSummary
from app.schemas.base import StandardResponse, MessageResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    service = TaskService(db)
    service.create_task(task)
    return MessageResponse(status=201, message="Tarefa criada com sucesso")


@router.get("/", response_model=StandardResponse[Page[TaskSummary]])
def list_tasks(params: Params = Depends(), db: Session = Depends(get_db)):
    service = TaskService(db)
    result = service.list_tasks(params)
    return StandardResponse(status=200, message="Tarefas listadas com sucesso", data=result)


@router.get("/{task_id}", response_model=StandardResponse[Task])
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    service = TaskService(db)
    result = service.get_task(task_id)
    return StandardResponse(status=200, message="Tarefa recuperada com sucesso", data=result)


@router.put("/{task_id}", response_model=MessageResponse)
def update_task(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    service = TaskService(db)
    service.update_task(task_id, task_update)
    return MessageResponse(status=200, message="Tarefa atualizada com sucesso")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    service = TaskService(db)
    service.delete_task(task_id)
    return None
