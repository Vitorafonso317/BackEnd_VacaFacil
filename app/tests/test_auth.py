def test_register_user(client, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["nome"] == test_user["nome"]

def test_login_user(client, test_user):
    # Registrar usuário
    client.post("/auth/register", json=test_user)
    
    # Login
    response = client.post("/auth/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"