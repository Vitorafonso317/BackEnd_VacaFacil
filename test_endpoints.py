#!/usr/bin/env python3
"""
Script para testar endpoints automaticamente
"""
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
        print(f"❌ Erro: {e}")
        return
    
    # 2. Registro de usuário
    print("\n2. 👤 Registro de Usuário")
    user_data = {
        "email": "teste@vacafacil.com",
        "nome": "João Fazendeiro",
        "telefone": "(11) 99999-9999",
        "fazenda": "Fazenda Teste",
        "password": "senha123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Usuário registrado com sucesso")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 3. Login
    print("\n3. 🔐 Login")
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
            print("✅ Login realizado com sucesso")
            print(f"Token: {token[:20]}...")
        else:
            print(f"❌ Erro no login: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Erro: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 4. Perfil do usuário
    print("\n4. 👤 Perfil do Usuário")
    try:
        response = requests.get(f"{BASE_URL}/users/me", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Perfil obtido com sucesso")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 5. Criar vaca
    print("\n5. 🐄 Criar Vaca")
    vaca_data = {
        "nome": "Mimosa",
        "raca": "Holandesa",
        "idade": 3,
        "peso": 550.5,
        "producao_media": 25.0,
        "status": "ativa",
        "observacoes": "Vaca muito produtiva"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/vacas/", json=vaca_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            vaca = response.json()
            vaca_id = vaca["id"]
            print(f"✅ Vaca criada com sucesso - ID: {vaca_id}")
        else:
            print(f"Response: {response.json()}")
            vaca_id = None
    except Exception as e:
        print(f"❌ Erro: {e}")
        vaca_id = None
    
    # 6. Listar vacas
    print("\n6. 📋 Listar Vacas")
    try:
        response = requests.get(f"{BASE_URL}/vacas/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            vacas = response.json()
            print(f"✅ {len(vacas)} vaca(s) encontrada(s)")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 7. Planos de assinatura
    print("\n7. 💳 Planos de Assinatura")
    try:
        response = requests.get(f"{BASE_URL}/subscriptions/plans")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Planos obtidos com sucesso")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 8. Status da assinatura
    print("\n8. 📊 Status da Assinatura")
    try:
        response = requests.get(f"{BASE_URL}/subscriptions/status", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            subscription = response.json()
            print(f"✅ Plano atual: {subscription['plan_type']}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # 9. Teste de validação (senha fraca)
    print("\n9. 🧪 Teste de Validação - Senha Fraca")
    weak_user = {
        "email": "teste2@vacafacil.com",
        "nome": "Teste",
        "password": "123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=weak_user)
        print(f"Status: {response.status_code}")
        if response.status_code == 422:
            print("✅ Validação funcionando - senha rejeitada")
        else:
            print(f"❌ Validação falhou: {response.json()}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testes concluídos!")
    print("📚 Acesse http://localhost:8000/docs para mais testes")

if __name__ == "__main__":
    # Aguardar servidor iniciar
    print("⏳ Aguardando servidor iniciar...")
    time.sleep(3)
    
    test_endpoints()