#!/usr/bin/env python3
"""
Teste essencial da API VacaFacil
"""
import requests
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("Testando API VacaFacil...")
    
    # Aguardar inicialização da API
    print("Aguardando API inicializar...")
    time.sleep(3)
    
    try:
        # Health check
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"Health: {response.status_code}")
        
        if response.status_code != 200:
            print("API não está respondendo corretamente")
            return
        
        # Registro
        user_data = {
            "email": "teste@example.com",
            "nome": "Test User",
            "password": "test_password_123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"Registro: {response.status_code}")
        
        # Login
        login_data = {"username": "teste@example.com", "password": "test_password_123"}
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data, timeout=10)
        
        if response.status_code == 200:
            try:
                token_data = response.json()
                if "access_token" in token_data:
                    token = token_data["access_token"]
                    print("Login: OK")
                else:
                    print("Erro: Token não encontrado")
                    return
            except Exception:
                print("Erro ao processar resposta do login")
                return
        else:
            print(f"Erro no login: {response.status_code}")
            return
        
        # Criar vaca
        vaca_data = {"nome": "Teste", "raca": "Holandesa"}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/vacas/", json=vaca_data, headers=headers, timeout=10)
        print(f"Criar vaca: {response.status_code}")
            
        print("Teste concluido!")
        
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_api()