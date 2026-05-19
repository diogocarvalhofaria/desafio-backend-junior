from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import projects_router, tasks_router
from app.schemas.base import StandardResponse
from fastapi_pagination import add_pagination

app = FastAPI(
    title="API de Projetos e Tarefas",
    description="API RESTful para gestão de projetos e tarefas",
    version="1.0.0"
)

#Tratamento de erro
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "message": exc.detail
        }
    )

@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "status": 422,
            "message": "Dados inválidos enviados na requisição",
            "errors": str(exc)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": 500,
            "message": "Ocorreu um erro interno inesperado no servidor",
            "details": str(exc) if app.debug else "Contate o suporte"
        }
    )

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Endpoint raiz da API"""
    return {
        "message": "Bem-vindo à API de Projetos e Tarefas",
        "version": "v1",
        "docs": "/docs",
        "redoc": "/redoc",
        "api": "/api/v1"
    }

@app.get("/health", response_model=StandardResponse)
def health_check():
    """Endpoint para verificar a saúde da API"""
    return StandardResponse(
        message="API está operando normalmente",
        data={"status": "healthy"}
    )

app.include_router(projects_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")

add_pagination(app)