#!/usr/bin/env python3
import requests
import json
import time
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

def test_ml_endpoints():
    print("Testando Endpoints de Machine Learning")
    print("=" * 50)
    
    # 1. Login para obter token
    print("\n1. Fazendo login...")
    login_data = {
        "username": "teste@vacafacil.com",
        "password": "senha123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("OK - Token obtido")
        else:
            print("ERRO - Precisa registrar usuario primeiro")
            return
    except Exception as e:
        print(f"ERRO: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Criar dados de teste (vaca + producoes)
    print("\n2. Criando dados de teste...")
    
    # Criar vaca
    vaca_data = {
        "nome": "Vaca ML Test",
        "raca": "Holandesa",
        "idade": 4,
        "peso": 600.0,
        "producao_media": 22.0
    }
    
    try:
        response = requests.post(f"{BASE_URL}/vacas/", json=vaca_data, headers=headers)
        if response.status_code == 200:
            vaca_id = response.json()["id"]
            print(f"OK - Vaca criada ID: {vaca_id}")
        else:
            print("Usando vaca existente ID: 1")
            vaca_id = 1
    except Exception as e:
        print(f"ERRO: {e}")
        vaca_id = 1
    
    # Criar algumas producoes para teste
    print("\n3. Criando producoes de teste...")
    for i in range(10):
        producao_data = {
            "vaca_id": vaca_id,
            "data": (date.today() - timedelta(days=i)).isoformat(),
            "quantidade_manha": 10 + (i % 3),
            "quantidade_tarde": 12 + (i % 2),
        }
        
        try:
            requests.post(f"{BASE_URL}/producao/", json=producao_data, headers=headers)
        except:
            pass
    
    print("OK - Producoes criadas")
    
    # 4. Testar predicao de producao
    print("\n4. Testando predicao de producao...")
    try:
        pred_data = {"vaca_id": vaca_id, "days_ahead": 5}
        response = requests.post(f"{BASE_URL}/ml/predict-production", json=pred_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"OK - {len(result['predicoes'])} predicoes geradas")
            print(f"Confiabilidade: {result['confiabilidade']}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"ERRO: {e}")
    
    # 5. Testar analise de performance
    print("\n5. Testando analise de performance...")
    try:
        response = requests.get(f"{BASE_URL}/ml/analyze-performance", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"OK - {result['total_vacas']} vacas analisadas")
            print(f"Media geral: {result['media_geral']}L")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"ERRO: {e}")
    
    # 6. Testar deteccao de anomalias
    print("\n6. Testando deteccao de anomalias...")
    try:
        response = requests.get(f"{BASE_URL}/ml/detect-anomalies", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"OK - {result['total_anomalias']} anomalias detectadas")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"ERRO: {e}")
    
    # 7. Testar recomendacoes
    print("\n7. Testando recomendacoes inteligentes...")
    try:
        response = requests.get(f"{BASE_URL}/ml/recommendations", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"OK - {result['total_recomendacoes']} recomendacoes geradas")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"ERRO: {e}")
    
    # 8. Testar previsao financeira
    print("\n8. Testando previsao financeira...")
    try:
        response = requests.get(f"{BASE_URL}/ml/financial-forecast?price_per_liter=2.80", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"OK - Receita mensal prevista: R$ {result['projecoes']['mensal']['receita']}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"ERRO: {e}")
    
    # 9. Testar dashboard de insights
    print("\n9. Testando dashboard de insights...")
    try:
        response = requests.get(f"{BASE_URL}/ml/insights", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("OK - Dashboard de insights funcionando")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"ERRO: {e}")
    
    print("\n" + "=" * 50)
    print("Testes de ML concluidos!")
    print("Acesse http://localhost:8000/docs#/machine-learning para mais detalhes")

if __name__ == "__main__":
    print("Aguardando servidor...")
    time.sleep(2)
    test_ml_endpoints()