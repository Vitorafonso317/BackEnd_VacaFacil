def test_create_vaca(client, test_user):
    # Registrar e fazer login
    client.post("/auth/register", json=test_user)
    login_response = client.post("/auth/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Criar vaca
    vaca_data = {
        "nome": "Mimosa",
        "raca": "Holandesa",
        "idade": 3,
        "peso": 550.5,
        "producao_media": 25.0
    }
    
    response = client.post("/vacas/", 
        json=vaca_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == vaca_data["nome"]
    assert data["raca"] == vaca_data["raca"]

def test_list_vacas(client, test_user):
    # Registrar e fazer login
    client.post("/auth/register", json=test_user)
    login_response = client.post("/auth/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Listar vacas
    response = client.get("/vacas/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)