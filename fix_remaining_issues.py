#!/usr/bin/env python3
"""
Script para corrigir problemas restantes automaticamente
"""
import os
import re

def fix_file_issues():
    """Corrigir problemas comuns em arquivos"""
    
    # Adicionar índices em modelos
    models_to_fix = [
        "app/models/user_model.py",
        "app/models/cattle_model.py", 
        "app/models/production_model.py",
        "app/models/reproduction_model.py"
    ]
    
    for model_file in models_to_fix:
        if os.path.exists(model_file):
            with open(model_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Adicionar índices em ForeignKey se não existir
            content = re.sub(
                r'ForeignKey\("([^"]+)"\)',
                r'ForeignKey("\1", ondelete="CASCADE")',
                content
            )
            
            # Adicionar index=True em colunas importantes
            content = re.sub(
                r'Column\(Integer, ForeignKey\("([^"]+)"(?:, ondelete="CASCADE")?\)\)',
                r'Column(Integer, ForeignKey("\1", ondelete="CASCADE"), index=True)',
                content
            )
            
            with open(model_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Fixed: {model_file}")

def add_error_handling():
    """Adicionar tratamento de erro básico em rotas"""
    
    routes_to_fix = [
        "app/routers/auth_routes.py",
        "app/routers/user_routes.py", 
        "app/routers/production_routes.py",
        "app/routers/financial_routes.py",
        "app/routers/marketplace_routes.py"
    ]
    
    for route_file in routes_to_fix:
        if os.path.exists(route_file):
            with open(route_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Adicionar import HTTPException se não existir
            if "from fastapi import" in content and "HTTPException" not in content:
                content = content.replace(
                    "from fastapi import",
                    "from fastapi import HTTPException,"
                )
            
            with open(route_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Fixed imports: {route_file}")

if __name__ == "__main__":
    print("Corrigindo problemas restantes...")
    fix_file_issues()
    add_error_handling()
    print("Correções aplicadas!")