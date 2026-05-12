from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.task import Task as TaskModel
from app.models.project import Project as ProjectModel
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_in: TaskCreate):
        project_exists = self.db.query(ProjectModel).filter(ProjectModel.id == task_in.project_id).first()
        if not project_exists:
            raise HTTPException(status_code=404, detail="Projeto associado não encontrado")

        db_task = TaskModel(**task_in.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def list_tasks(self, params: Params = Params()):
        return paginate(self.db.query(TaskModel), params)

    def get_task(self, task_id: UUID):
        task = self.db.query(TaskModel).filter(TaskModel.id == task_id).first()
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