# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: lorena_system_guardian.py                         ║
║   Status: MONITORAMENTO DE SOBERANIA | LORENA               ║
╚══════════════════════════════════════════════════════════════╝

Guardião da Infraestrutura Imperial.
Monitora a integridade do banco de dados SQLite e a saúde da fila de render.
"""

import sqlite3
import os
import sys
import time

DB_PATH = r"d:\Blender\blenderscripts\manifests\imperial_missions.db"

def check_sovereignty():
    """Realiza uma auditoria de saúde no sistema central."""
    print("🛡️ [LORENA] Iniciando Inspeção de Soberania...")
    
    # 1. Verificar existência do banco
    if not os.path.exists(DB_PATH):
        print("🚨 [CRÍTICO] Banco de dados MISSIONS não encontrado! Sistema offline.")
        return False
        
    # 2. Auditar integridade e volume
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check integrity
        cursor.execute("PRAGMA integrity_check")
        res = cursor.fetchone()[0]
        if res != "ok":
            print(f"🚨 [ALERTA] Falha na integridade do banco: {res}")
            return False
            
        # Stats
        cursor.execute("SELECT COUNT(*) FROM missions WHERE status = 'QUEUED'")
        queued = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM missions WHERE status = 'PROCESSING'")
        processing = cursor.fetchone()[0]
        
        print(f"📊 [PRODUTIVIDADE] Fila: {queued} missões aguardando | Ativos: {processing}")
        
        if queued > 15:
            print("⚠️ [OTIMIZAÇÃO] Fila acima da capacidade ideal. Sugerindo expansão de workers.")
            
        conn.close()
        print("✅ [LORENA] Sistema íntegro e operacional sob as Leis Universais.")
        return True
        
    except Exception as e:
        print(f"❌ [LORENA] Falha na auditoria de governança: {e}")
        return False

if __name__ == "__main__":
    check_sovereignty()
