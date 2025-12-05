#!/usr/bin/env python3
"""
Script para verificar integridade dos anúncios do marketplace
"""
import sqlite3
import os

DB_PATH = "vacafacil.db"

def verificar_marketplace():
    if not os.path.exists(DB_PATH):
        print(f"[ERRO] Banco de dados não encontrado: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Total de anúncios
        cursor.execute("SELECT COUNT(*) FROM anuncios")
        total = cursor.fetchone()[0]
        print(f"Total de anúncios: {total}")
        
        # Anúncios ativos
        cursor.execute("SELECT COUNT(*) FROM anuncios WHERE ativo = 1")
        ativos = cursor.fetchone()[0]
        print(f"Anúncios ativos: {ativos}")
        
        # Anúncios inativos
        print(f"Anúncios inativos: {total - ativos}")
        
        # Anúncios por usuário
        cursor.execute("""
            SELECT u.nome, u.email, COUNT(a.id) as total
            FROM users u
            LEFT JOIN anuncios a ON u.id = a.user_id
            GROUP BY u.id
            HAVING total > 0
            ORDER BY total DESC
        """)
        usuarios = cursor.fetchall()
        
        if usuarios:
            print("\nAnúncios por usuário:")
            for nome, email, qtd in usuarios:
                print(f"  - {nome} ({email}): {qtd} anúncio(s)")
        else:
            print("\nNenhum anúncio cadastrado por usuários")
        
        # Verificar anúncios órfãos
        cursor.execute("""
            SELECT COUNT(*) FROM anuncios 
            WHERE user_id IS NULL OR user_id NOT IN (SELECT id FROM users)
        """)
        orfaos = cursor.fetchone()[0]
        
        if orfaos > 0:
            print(f"\n[AVISO] {orfaos} anúncio(s) órfão(s) encontrado(s)")
            print("Execute: python limpar_anuncios_mockados.py")
        else:
            print("\n[OK] Nenhum anúncio órfão encontrado")
        
    except Exception as e:
        print(f"[ERRO] {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("  VERIFICAÇÃO DO MARKETPLACE")
    print("=" * 60)
    print()
    verificar_marketplace()
    print()
    print("=" * 60)
