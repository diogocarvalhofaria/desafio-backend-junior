from fastapi import APIRouter, Depends, status, Query
from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi_pagination import Page, Params

from app.database import get_db
from app.services.task_service import TaskService
from app.schemas.task import Task, TaskCreate, TaskUpdate, TaskSummary
from app.schemas.base import StandardResponse, MessageResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=StandardResponse[Task],
    status_code=status.HTTP_201_CREATED,
    summary="Criar tarefa",
    description="Cria uma nova tarefa vinculada a um projeto existente. Retorna a tarefa criada com seu ID gerado.",
    response_description="Tarefa criada com sucesso",
    responses={
        404: {"description": "Projeto associado não encontrado"},
    },
)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    service = TaskService(db)
    created = service.create_task(task)
    return StandardResponse(status=201, message="Tarefa criada com sucesso", data=created)


@router.get(
    "/",
    response_model=StandardResponse[Page[TaskSummary]],
    summary="Listar tarefas",
    description="Retorna a lista paginada de todas as tarefas. Filtre por `project_id`, `completed` ou busca parcial em `title`.",
    response_description="Lista de tarefas paginada",
)
def list_tasks(
    params: Params = Depends(),
    project_id: Optional[UUID] = Query(None, description="Filtrar pelo ID do projeto"),
    completed: Optional[bool] = Query(None, description="Filtrar por status de conclusão"),
    title: Optional[str] = Query(None, description="Filtrar por título"),
    db: Session = Depends(get_db),
):
    service = TaskService(db)
    result = service.list_tasks(params, project_id=project_id, completed=completed, title=title)
    return StandardResponse(status=200, message="Tarefas listadas com sucesso", data=result)


@router.get(
    "/{task_id}",
    response_model=StandardResponse[Task],
    summary="Detalhar tarefa",
    description="Retorna os dados completos de uma tarefa pelo seu ID.",
    response_description="Dados da tarefa",
    responses={
        404: {"description": "Tarefa não encontrada"},
    },
)
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    service = TaskService(db)
    result = service.get_task(task_id)
    return StandardResponse(status=200, message="Tarefa recuperada com sucesso", data=result)


@router.put(
    "/{task_id}",
    response_model=StandardResponse[Task],
    summary="Atualizar tarefa",
    description="Atualiza os dados de uma tarefa existente. Apenas os campos enviados serão alterados. Use `completed: true` para marcar a tarefa como concluída.",
    response_description="Tarefa atualizada com sucesso",
    responses={
        404: {"description": "Tarefa não encontrada"},
    },
)
def update_task(task_id: UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    service = TaskService(db)
    updated = service.update_task(task_id, task_update)
    return StandardResponse(status=200, message="Tarefa atualizada com sucesso", data=updated)


@router.delete(
    "/{task_id}",
    response_model=MessageResponse,
    summary="Remover tarefa",
    description="Remove uma tarefa pelo seu ID.",
    response_description="Tarefa removida com sucesso",
    responses={
        404: {"description": "Tarefa não encontrada"},
    },
)
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    service = TaskService(db)
    service.delete_task(task_id)
    return MessageResponse(status=200, message="Tarefa removida com sucesso")
