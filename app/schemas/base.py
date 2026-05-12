from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    status: int = 200
    message: str = "Operação realizada com sucesso"
    data: Optional[T] = None

class MessageResponse(BaseModel):
    status: int = 200
    message: str = "Operação realizada com sucesso"