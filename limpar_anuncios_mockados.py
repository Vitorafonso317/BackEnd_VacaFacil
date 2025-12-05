#!/usr/bin/env python3
"""
Script para remover anúncios mockados do marketplace
Remove todos os anúncios que não foram criados por usuários reais
"""
import sqlite3
import os

DB_PATH = "vacafacil.db"

def limpar_anuncios_mockados():
    if not os.path.exists(DB_PATH):
        print(f"[ERRO] Banco de dados não encontrado: {DB_PATH}")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verificar anúncios existentes
        cursor.execute("SELECT COUNT(*) FROM anuncios")
        total_antes = cursor.fetchone()[0]
        print(f"Total de anúncios antes: {total_antes}")
        
        # Verificar anúncios sem user_id válido
        cursor.execute("""
            SELECT COUNT(*) FROM anuncios 
            WHERE user_id IS NULL OR user_id NOT IN (SELECT id FROM users)
        """)
        mockados = cursor.fetchone()[0]
        print(f"Anúncios mockados (sem usuário válido): {mockados}")
        
        if mockados > 0:
            # Remover anúncios mockados
            cursor.execute("""
                DELETE FROM anuncios 
                WHERE user_id IS NULL OR user_id NOT IN (SELECT id FROM users)
            """)
            conn.commit()
            print(f"[OK] {mockados} anúncios mockados removidos")
        else:
            print("[OK] Nenhum anúncio mockado encontrado")
        
        # Verificar total após limpeza
        cursor.execute("SELECT COUNT(*) FROM anuncios")
        total_depois = cursor.fetchone()[0]
        print(f"Total de anúncios depois: {total_depois}")
        
    except Exception as e:
        print(f"[ERRO] {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("  LIMPEZA DE ANÚNCIOS MOCKADOS")
    print("=" * 60)
    print()
    limpar_anuncios_mockados()
    print()
    print("=" * 60)
