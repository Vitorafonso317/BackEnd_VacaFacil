#!/usr/bin/env python3
"""
Script para testar se o servidor inicia corretamente
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Iniciando servidor VacaFacil...")
    print("Acesse: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)