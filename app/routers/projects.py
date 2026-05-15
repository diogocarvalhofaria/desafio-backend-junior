from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi_pagination import Page, Params

from app.database import get_db
from app.services.project_service import ProjectService
from app.schemas.project import Project, ProjectCreate, ProjectUpdate, ProjectWithTasks, ProjectSummary
from app.schemas.base import StandardResponse, MessageResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "/",
    response_model=StandardResponse[Project],
    status_code=status.HTTP_201_CREATED,
    summary="Criar projeto",
    description="Cria um novo projeto. Retorna o projeto criado com seu ID gerado.",
    response_description="Projeto criado com sucesso",
)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    service = ProjectService(db)
    created = service.create_project(project)
    return StandardResponse(status=201, message="Projeto criado com sucesso", data=created)


@router.get(
    "/",
    response_model=StandardResponse[Page[ProjectSummary]],
    summary="Listar projetos",
    description="Retorna a lista paginada de todos os projetos. Use os parâmetros `page` e `size` para controlar a paginação.",
    response_description="Lista de projetos paginada",
)
def list_projects(params: Params = Depends(), db: Session = Depends(get_db)):
    service = ProjectService(db)
    result = service.list_projects(params)
    return StandardResponse(status=200, message="Projetos listados com sucesso", data=result)


@router.get(
    "/{project_id}",
    response_model=StandardResponse[ProjectWithTasks],
    summary="Detalhar projeto",
    description="Retorna os dados completos de um projeto, incluindo a lista de tarefas vinculadas.",
    response_description="Dados do projeto com suas tarefas",
    responses={
        404: {"description": "Projeto não encontrado"},
    },
)
def get_by_id_project(project_id: UUID, db: Session = Depends(get_db)):
    service = ProjectService(db)
    result = service.get_by_id_project(project_id)
    return StandardResponse(status=200, message="Projeto recuperado com sucesso", data=result)


@router.put(
    "/{project_id}",
    response_model=StandardResponse[Project],
    summary="Atualizar projeto",
    description="Atualiza os dados de um projeto existente. Apenas os campos enviados serão alterados (PATCH semântico).",
    response_description="Projeto atualizado com sucesso",
    responses={
        404: {"description": "Projeto não encontrado"},
    },
)
def update_project(project_id: UUID, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    service = ProjectService(db)
    updated = service.update_project(project_id, project_update)
    return StandardResponse(status=200, message="Projeto atualizado com sucesso", data=updated)


@router.delete(
    "/{project_id}",
    response_model=MessageResponse,
    summary="Remover projeto",
    description="Remove um projeto e todas as suas tarefas associadas (cascade delete).",
    response_description="Projeto removido com sucesso",
    responses={
        404: {"description": "Projeto não encontrado"},
    },
)
def delete_project(project_id: UUID, db: Session = Depends(get_db)):
    service = ProjectService(db)
    service.delete_project(project_id)
    return MessageResponse(status=200, message="Projeto removido com sucesso")