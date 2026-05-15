"""
Testes para os endpoints de Tarefas (/tasks/)

Coberturas:
- POST /tasks/  → criação com sucesso (projeto válido)
- POST /tasks/  → falha: projeto não existe (404)
- POST /tasks/  → falha: dados inválidos (422)
- GET  /tasks/  → listagem retorna status 200
- GET  /tasks/{id} → detalhe com sucesso
- GET  /tasks/{id} → não encontrado (404)
- PUT  /tasks/{id} → atualização (marcar como concluída)
- PUT  /tasks/{id} → não encontrado (404)
- DELETE /tasks/{id} → remoção com sucesso
- DELETE /tasks/{id} → não encontrado (404)
"""

import pytest

@pytest.fixture
def projeto_criado(client):
    resp = client.post("/projects/", json={"name": "Projeto Base para Tasks"})
    assert resp.status_code == 201
    return resp.json()["data"]["id"]

def test_create_task_success(client, projeto_criado):
    payload = {
        "title": "Minha Task",
        "description": "Descrição da task",
        "project_id": projeto_criado,
    }
    response = client.post("/tasks/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == 201
    assert data["message"] == "Tarefa criada com sucesso"


def test_create_task_with_invalid_project(client):
    payload = {
        "title": "Minha Task",
        "project_id": "550e8400-e29b-41d4-a716-446655440000",
    }
    response = client.post("/tasks/", json=payload)

    assert response.status_code == 404
    assert "Projeto associado não encontrado" in response.json()["message"]


def test_create_task_missing_title(client, projeto_criado):
    payload = {"project_id": projeto_criado}
    response = client.post("/tasks/", json=payload)

    assert response.status_code == 422


def test_list_tasks(client, projeto_criado):
    client.post("/tasks/", json={"title": "Task Lista", "project_id": projeto_criado})

    response = client.get("/tasks/")
    assert response.status_code == 200


def test_get_task_by_id_success(client, projeto_criado):
    create_resp = client.post("/tasks/", json={"title": "Task Detalhe", "project_id": projeto_criado})
    assert create_resp.status_code == 201

    task_id = create_resp.json()["data"]["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200

    data = response.json()["data"]
    assert data["id"] == task_id
    assert data["title"] == "Task Detalhe"


def test_get_task_not_found(client):
    response = client.get("/tasks/550e8400-e29b-41d4-a716-446655440000")
    assert response.status_code == 404


def test_update_task_complete(client, projeto_criado):
    create_resp = client.post("/tasks/", json={"title": "Task Incompleta", "project_id": projeto_criado})
    task_id = create_resp.json()["data"]["id"]

    response = client.put(f"/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200

    data = response.json()["data"]
    assert data["completed"] is True


def test_update_task_not_found(client):
    response = client.put(
        "/tasks/550e8400-e29b-41d4-a716-446655440000",
        json={"title": "Qualquer"}
    )
    assert response.status_code == 404


def test_delete_task_success(client, projeto_criado):
    create_resp = client.post("/tasks/", json={"title": "Task Deletável", "project_id": projeto_criado})
    task_id = create_resp.json()["data"]["id"]

    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200

    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/tasks/550e8400-e29b-41d4-a716-446655440000")
    assert response.status_code == 404