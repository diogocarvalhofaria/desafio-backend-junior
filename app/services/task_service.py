from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from uuid import UUID
from typing import Optional
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.task import Task as TaskModel
from app.models.project import Project as ProjectModel
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_in: TaskCreate):
        project_exists = self.db.execute(select(ProjectModel).filter(ProjectModel.id == task_in.project_id)).scalars().first()
        if not project_exists:
            raise HTTPException(status_code=404, detail="Projeto associado não encontrado")

        db_task = TaskModel(**task_in.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def list_tasks(
        self,
        params: Params = Params(),
        project_id: Optional[UUID] = None,
        completed: Optional[bool] = None,
        title: Optional[str] = None,
    ):
        query = select(TaskModel)

        if project_id:
            query = query.where(TaskModel.project_id == project_id)

        if completed is not None:
            query = query.where(TaskModel.completed == completed)

        if title:
            query = query.where(TaskModel.title.ilike(f"%{title}%"))

        return paginate(self.db, query, params)

    def get_task(self, task_id: UUID):
        task = self.db.execute(select(TaskModel).filter(TaskModel.id == task_id)).scalars().first()
        if not task:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        return task

    def update_task(self, task_id: UUID, task_update: TaskUpdate):
        db_task = self.get_task(task_id)

        update_data = task_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)

        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete_task(self, task_id: UUID):
        db_task = self.get_task(task_id)
        self.db.delete(db_task)
        self.db.commit()
        return True