from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi_pagination import Page, Params

from app.database import get_db
from app.services.project_service import ProjectService
from app.schemas.project import Project, ProjectCreate, ProjectUpdate, ProjectWithTasks, ProjectSummary
from app.schemas.base import StandardResponse, MessageResponse

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    service = ProjectService(db)
    service.create_project(project)
    return MessageResponse(status=201, message="Projeto criado com sucesso")

@router.get("/", response_model=StandardResponse[Page[ProjectSummary]])
def list_projects(params: Params = Depends(), db: Session = Depends(get_db)):
    service = ProjectService(db)
    result = service.list_projects(params)
    return StandardResponse(status=200, message="Projetos listados com sucesso", data=result)

@router.get("/{project_id}", response_model=StandardResponse[ProjectWithTasks])
def get_by_id_project(project_id: UUID, db: Session = Depends(get_db)):
    service = ProjectService(db)
    result = service.get_by_id_project(project_id)
    return StandardResponse(status=200, message="Projeto recuperado com sucesso", data=result)

@router.put("/{project_id}", response_model=MessageResponse)
def update_project(project_id: UUID, project_update: ProjectUpdate, db: Session = Depends(get_db)):
    service = ProjectService(db)
    service.update_project(project_id, project_update)
    return MessageResponse(status=200, message="Projeto atualizado com sucesso")

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: UUID, db: Session = Depends(get_db)):
    service = ProjectService(db)
    service.delete_project(project_id)
    return None