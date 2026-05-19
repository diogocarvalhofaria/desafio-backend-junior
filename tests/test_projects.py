def test_create_project_success(client):
    response = client.post("/api/v1/projects/", json={"name": "Projeto Alpha", "description": "Teste"})

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == 201
    assert data["message"] == "Projeto criado com sucesso"


def test_create_project_without_description(client):
    response = client.post("/api/v1/projects/", json={"name": "Projeto Sem Descrição"})

    assert response.status_code == 201


def test_create_project_missing_name(client):
    response = client.post("/api/v1/projects/", json={"description": "Sem nome"})

    assert response.status_code == 422


def test_list_projects(client):
    client.post("/api/v1/projects/", json={"name": "Projeto Lista"})

    response = client.get("/api/v1/projects/")
    assert response.status_code == 200


def test_get_project_by_id_success(client):
    create_resp = client.post("/api/v1/projects/", json={"name": "Projeto Detalhe", "description": "Desc"})
    assert create_resp.status_code == 201

    project_id = create_resp.json()["data"]["id"]

    response = client.get(f"/api/v1/projects/{project_id}")
    assert response.status_code == 200

    data = response.json()["data"]
    assert data["id"] == project_id
    assert data["name"] == "Projeto Detalhe"


def test_get_project_not_found(client):
    response = client.get("/api/v1/projects/550e8400-e29b-41d4-a716-446655440000")

    assert response.status_code == 404
    assert response.json()["message"] == "Projeto não encontrado"


def test_update_project_success(client):
    create_resp = client.post("/api/v1/projects/", json={"name": "Nome Original"})
    project_id = create_resp.json()["data"]["id"]

    response = client.put(f"/api/v1/projects/{project_id}", json={"name": "Nome Atualizado"})
    assert response.status_code == 200

    data = response.json()["data"]
    assert data["name"] == "Nome Atualizado"


def test_update_project_not_found(client):
    response = client.put(
        "/api/v1/projects/550e8400-e29b-41d4-a716-446655440000",
        json={"name": "Qualquer"}
    )
    assert response.status_code == 404


def test_delete_project_success(client):
    create_resp = client.post("/api/v1/projects/", json={"name": "Projeto Para Deletar"})
    project_id = create_resp.json()["data"]["id"]

    delete_resp = client.delete(f"/api/v1/projects/{project_id}")
    assert delete_resp.status_code == 200

    get_resp = client.get(f"/api/v1/projects/{project_id}")
    assert get_resp.status_code == 404


def test_delete_project_not_found(client):
    response = client.delete("/api/v1/projects/550e8400-e29b-41d4-a716-446655440000")
    assert response.status_code == 404