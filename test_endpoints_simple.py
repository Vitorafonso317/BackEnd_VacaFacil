#!/usr/bin/env python3
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoints():
    print("Testando Endpoints VacaFacil API")
    print("=" * 50)
    
    # 1. Health Check
    print("\n1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"ERRO: {e}")
        return
    
    # 2. Registro de usuario
    print("\n2. Registro de Usuario")
    user_data = {
        "email": "teste@vacafacil.com",
        "nome": "Joao Fazendeiro",
        "telefone": "(11) 99999-9999",
        "fazenda": "Fazenda Teste",
        "password": "senha123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("OK - Usuario registrado")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"ERRO: {e}")
    
    # 3. Login
    print("\n3. Login")
    login_data = {
        "username": "teste@vacafacil.com",
        "password": "senha123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            token = token_data["access_token"]
            print("OK - Login realizado")
            print(f"Token: {token[:20]}...")
        else:
            print(f"ERRO no login: {response.json()}")
            return
    except Exception as e:
        print(f"ERRO: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 4. Criar vaca
    print("\n4. Criar Vaca")
    vaca_data = {
        "nome": "Mimosa",
        "raca": "Holandesa",
        "idade": 3,
        "peso": 550.5,
        "producao_media": 25.0,
        "status": "ativa"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/vacas/", json=vaca_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            vaca = response.json()
            print(f"OK - Vaca criada - ID: {vaca['id']}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"ERRO: {e}")
    
    # 5. Listar vacas
    print("\n5. Listar Vacas")
    try:
        response = requests.get(f"{BASE_URL}/vacas/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            vacas = response.json()
            print(f"OK - {len(vacas)} vaca(s) encontrada(s)")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"ERRO: {e}")
    
    print("\n" + "=" * 50)
    print("Testes concluidos!")
    print("Acesse http://localhost:8000/docs para mais testes")

if __name__ == "__main__":
    print("Aguardando servidor...")
    time.sleep(2)
    test_endpoints()