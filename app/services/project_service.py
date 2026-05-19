from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from uuid import UUID
from typing import Optional
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.project import Project as ProjectModel
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(self, db: Session):
        self.db = db

    def create_project(self, project_in: ProjectCreate):
        db_project = ProjectModel(**project_in.model_dump())
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def list_projects(self, params: Params = Params(), name: Optional[str] = None):
        query = select(ProjectModel)

        if name:
            query = query.where(ProjectModel.name.ilike(f"%{name}%"))

        return paginate(self.db, query, params)

    def get_by_id_project(self, project_id: UUID):
        project = self.db.execute(select(ProjectModel).filter(ProjectModel.id == project_id)).scalars().first()
        if not project:
            raise HTTPException(status_code=404, detail="Projeto não encontrado")
        return project

    def update_project(self, project_id: UUID, project_update: ProjectUpdate):
        db_project = self.get_by_id_project(project_id)

        update_data = project_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)

        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def delete_project(self, project_id: UUID):
        db_project = self.get_by_id_project(project_id)
        self.db.delete(db_project)
        self.db.commit()
        return True