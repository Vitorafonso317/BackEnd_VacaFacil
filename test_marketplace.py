#!/usr/bin/env python3
"""
Teste dos novos endpoints de Marketplace e Contato
"""
import requests
import time

BASE_URL = "http://localhost:5000"

def test_contact():
    """Testa endpoint de contato"""
    print("=== TESTANDO CONTATO ===")
    
    contact_data = {
        "name": "João Silva",
        "email": "joao@example.com",
        "message": "Gostaria de saber mais sobre o sistema VacaFacil"
    }
    response = requests.post(f"{BASE_URL}/contact/", json=contact_data)
    print(f"POST /contact/: {response.status_code}")
    if response.status_code == 201:
        print(f"[OK] Contato criado: {response.json()}")
    else:
        print(f"[ERRO] {response.text}")
    print()

def test_marketplace(token):
    """Testa endpoints de marketplace"""
    print("=== TESTANDO MARKETPLACE ===")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Criar anuncio
    anuncio_data = {
        "titulo": "Vaca Holandesa de Alta Producao",
        "descricao": "Excelente produtora de leite, muito saudavel e bem cuidada",
        "tipo": "venda",
        "categoria": "vaca",
        "raca": "Holandesa",
        "idade": 36,
        "producao_diaria": 25.0,
        "preco": 8000.00,
        "contato": "11999999999",
        "localizacao": "Sao Paulo, SP"
    }
    response = requests.post(f"{BASE_URL}/marketplace/", json=anuncio_data, headers=headers)
    print(f"POST /marketplace/: {response.status_code}")
    
    anuncio_id = None
    if response.status_code == 200:
        anuncio_id = response.json()["id"]
        print(f"[OK] Anuncio criado: ID {anuncio_id}")
    else:
        print(f"[ERRO] {response.text}")
    
    # Listar anuncios
    response = requests.get(f"{BASE_URL}/marketplace/")
    print(f"GET /marketplace/: {response.status_code}")
    
    # Filtrar por tipo
    response = requests.get(f"{BASE_URL}/marketplace/?tipo=venda")
    print(f"GET /marketplace/?tipo=venda: {response.status_code}")
    
    # Filtrar por raca
    response = requests.get(f"{BASE_URL}/marketplace/?raca=Holandesa")
    print(f"GET /marketplace/?raca=Holandesa: {response.status_code}")
    
    # Filtrar por preco
    response = requests.get(f"{BASE_URL}/marketplace/?preco_min=5000&preco_max=10000")
    print(f"GET /marketplace/?preco_min=5000&preco_max=10000: {response.status_code}")
    
    if anuncio_id:
        # Buscar anuncio especifico
        response = requests.get(f"{BASE_URL}/marketplace/{anuncio_id}")
        print(f"GET /marketplace/{anuncio_id}: {response.status_code}")
        
        # Meus anuncios
        response = requests.get(f"{BASE_URL}/marketplace/me/anuncios", headers=headers)
        print(f"GET /marketplace/me/anuncios: {response.status_code}")
        
        # Atualizar anuncio
        update_data = {"preco": 7500.00}
        response = requests.put(f"{BASE_URL}/marketplace/{anuncio_id}", json=update_data, headers=headers)
        print(f"PUT /marketplace/{anuncio_id}: {response.status_code}")
        
        # Deletar anuncio
        response = requests.delete(f"{BASE_URL}/marketplace/{anuncio_id}", headers=headers)
        print(f"DELETE /marketplace/{anuncio_id}: {response.status_code}")
    
    print()

def get_token():
    """Obtem token de autenticacao"""
    print("=== AUTENTICACAO ===")
    
    # Registro
    user_data = {
        "email": f"teste_{int(time.time())}@example.com",
        "nome": "Usuario Teste",
        "password": "Senha123",
        "telefone": "11999999999",
        "fazenda": "Fazenda Teste"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    print(f"POST /auth/register: {response.status_code}")
    
    # Login
    login_data = {"username": user_data["email"], "password": user_data["password"]}
    response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    print(f"POST /auth/login: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"[OK] Token obtido\n")
        return token
    
    print(f"[ERRO] Login falhou\n")
    return None

def main():
    print("=" * 60)
    print("  TESTE - MARKETPLACE E CONTATO")
    print("=" * 60)
    print()
    
    # Testar contato (publico)
    test_contact()
    
    # Obter token
    token = get_token()
    if not token:
        print("[ERRO] Nao foi possivel obter token")
        return
    
    # Testar marketplace
    test_marketplace(token)
    
    print("=" * 60)
    print("  TESTES CONCLUIDOS")
    print("=" * 60)

if __name__ == "__main__":
    main()
