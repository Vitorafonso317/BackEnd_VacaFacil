#!/usr/bin/env python3
"""
Script de verificação de segurança do VacaFácil
"""
import os
import sys
from pathlib import Path

def check_env_file():
    """Verificar se arquivo .env existe e está configurado"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Arquivo .env não encontrado")
        print("   Copie .env.example para .env e configure as variáveis")
        return False
    
    print("✅ Arquivo .env encontrado")
    return True

def check_secret_key():
    """Verificar se SECRET_KEY está configurada"""
    secret_key = os.getenv("SECRET_KEY")
    
    if not secret_key:
        print("❌ SECRET_KEY não configurada")
        return False
    
    if secret_key == "CHANGE_ME_IN_PRODUCTION":
        print("❌ SECRET_KEY usando valor padrão inseguro")
        return False
    
    if len(secret_key) < 32:
        print("❌ SECRET_KEY muito curta (mínimo 32 caracteres)")
        return False
    
    print("✅ SECRET_KEY configurada corretamente")
    return True

def check_database_url():
    """Verificar configuração do banco"""
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("❌ DATABASE_URL não configurada")
        return False
    
    # Verificar se não tem credenciais expostas em arquivos
    dangerous_files = [
        "alembic.ini",
        "docker-compose.yml",
        "README.md"
    ]
    
    for file_path in dangerous_files:
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "password" in content.lower() and "@" in content:
                    # Verificar se não é apenas exemplo
                    if "example" not in content.lower() and "your_" not in content.lower():
                        print(f"⚠️  Possível credencial exposta em {file_path}")
    
    print("✅ DATABASE_URL configurada")
    return True

def check_dependencies():
    """Verificar dependências de segurança"""
    try:
        import bcrypt
        import jose
        print("✅ Dependências de segurança instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        return False

def main():
    """Executar verificações de segurança"""
    print("🔒 Verificação de Segurança - VacaFácil")
    print("=" * 40)
    
    checks = [
        check_env_file,
        check_secret_key,
        check_database_url,
        check_dependencies
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Resultado: {passed}/{total} verificações passaram")
    
    if passed == total:
        print("🎉 Todas as verificações de segurança passaram!")
        return 0
    else:
        print("⚠️  Algumas verificações falharam. Corrija antes de usar em produção.")
        return 1

if __name__ == "__main__":
    sys.exit(main())