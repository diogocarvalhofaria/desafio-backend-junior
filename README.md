# API de Projetos e Tarefas

API RESTful desenvolvida com **FastAPI** e **PostgreSQL** para gestão de projetos e tarefas, com paginação, testes automatizados e documentação interativa via Swagger.

---

## Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.11+ | Linguagem principal |
| FastAPI | Framework web |
| SQLAlchemy | ORM |
| Alembic | Migrations |
| PostgreSQL 15 | Banco de dados |
| Pydantic v2 | Validação e schemas |
| Uvicorn | Servidor ASGI |
| fastapi-pagination | Paginação de resultados |
| Pytest | Testes automatizados |
| Docker / Docker Compose | Infraestrutura |

---

## Estrutura do projeto

```
.
├── app/
│   ├── models/
│   │   ├── __init__.py          # Re-exporta Project e Task
│   │   ├── project.py           # Modelo ORM de Project
│   │   └── task.py              # Modelo ORM de Task
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── base.py              # StandardResponse[T] e MessageResponse
│   │   ├── project.py           # Schemas de Project (Create, Update, Response, WithTasks)
│   │   └── task.py              # Schemas de Task (Create, Update, Response)
│   ├── routers/
│   │   ├── __init__.py          # Re-exporta os routers
│   │   ├── projects.py          # Endpoints de projetos
│   │   └── task.py              # Endpoints de tarefas
│   ├── services/
│   │   ├── __init__.py          # Re-exporta ProjectService e TaskService
│   │   ├── project_service.py   # Regras de negócio de projetos
│   │   └── task_service.py      # Regras de negócio de tarefas
│   ├── __init__.py
│   ├── database.py              # Engine, sessão e dependência get_db
│   └── main.py                  # Entrada da aplicação, middlewares, handlers de erro
├── migration/
│   ├── versions/                # Migrations geradas pelo Alembic
│   ├── env.py                   # Configuração do ambiente Alembic
│   └── script.py.mako           # Template de migrations
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Fixtures: banco SQLite in-memory, client, reset_db
│   ├── test_projects.py         # Testes de CRUD de projetos
│   └── test_tasks.py            # Testes de CRUD de tarefas
├── .env.example                 # Exemplo de variáveis de ambiente
├── alembic.ini                  # Configuração do Alembic
├── docker-compose.yml           # PostgreSQL + API via Docker
├── Dockerfile                   # Imagem da aplicação
├── requirements.txt             # Dependências do projeto
└── README.md
```

---

## Instalação e execução

### Opção 1: Docker (Recomendado) 🐳

Sobe o banco de dados **e** a API com um único comando. As migrations são aplicadas automaticamente.

**Pré-requisito:** Docker e Docker Compose instalados.

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/desafio-backend-junior.git
cd desafio-backend-junior

# 2. Subir todos os serviços
docker-compose up --build
```

A API estará disponível em `http://localhost:8000`.

> Para rodar em background: `docker-compose up --build -d`  
> Para parar: `docker-compose down`  
> Para parar e apagar os dados: `docker-compose down -v`

---

### Opção 2: Execução local

**Pré-requisitos:** Python 3.10+ e Docker (para o banco).

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/desafio-backend-junior.git
cd desafio-backend-junior

# 2. Criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Edite o .env com sua DATABASE_URL

# 5. Subir apenas o banco de dados
docker-compose up -d postgres

# 6. Rodar as migrations
alembic upgrade head

# 7. Iniciar o servidor
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

---

## Documentação interativa

| Interface | URL |
|---|---|
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Health Check | http://localhost:8000/health |

---

## Endpoints

### Projetos

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/projects/` | Criar um novo projeto |
| `GET` | `/projects/` | Listar projetos (paginado) |
| `GET` | `/projects/{project_id}` | Detalhar projeto com suas tarefas |
| `PUT` | `/projects/{project_id}` | Atualizar projeto |
| `DELETE` | `/projects/{project_id}` | Remover projeto e suas tarefas (cascade) |

### Tarefas

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/tasks/` | Criar tarefa vinculada a um projeto |
| `GET` | `/tasks/` | Listar tarefas (paginado) |
| `GET` | `/tasks/{task_id}` | Detalhar tarefa |
| `PUT` | `/tasks/{task_id}` | Atualizar tarefa |
| `DELETE` | `/tasks/{task_id}` | Remover tarefa |

### Formato padrão de resposta

Todas as respostas seguem o envelope `StandardResponse[T]`:

```json
{
  "status": 200,
  "message": "Operação realizada com sucesso",
  "data": {}
}
```

---

## Exemplos de uso

### Criar um projeto

```bash
curl -X POST "http://localhost:8000/projects/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Meu Projeto", "description": "Descrição opcional"}'
```

### Criar uma tarefa

```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Minha Tarefa", "description": "Descrição opcional", "project_id": "uuid-do-projeto"}'
```

### Listar projetos com paginação

```bash
curl "http://localhost:8000/projects/?page=1&size=10"
```

### Marcar tarefa como concluída

```bash
curl -X PUT "http://localhost:8000/tasks/{task_id}" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
```

---

## Testes

Os testes utilizam **SQLite em memória** — não é necessária nenhuma configuração adicional.

```bash
# Rodar todos os testes
pytest

# Com saída detalhada
pytest -v

# Com relatório de cobertura
pytest --cov=app --cov-report=term-missing
```

### O que é testado

- `test_projects.py`: criação, listagem, busca por ID, atualização, remoção e casos de erro (404, 422)
- `test_tasks.py`: criação com projeto válido/inválido, listagem, busca, atualização, remoção e casos de erro

---

## Migrations

```bash
# Criar nova migration
alembic revision --autogenerate -m "descrição da mudança"

# Aplicar migrations pendentes
alembic upgrade head

# Reverter última migration
alembic downgrade -1

# Ver histórico
alembic history
```
