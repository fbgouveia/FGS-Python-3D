# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: mission_control.py                                ║
║   Status: CEO ORCHESTRATOR | BLINDADO                      ║
╚══════════════════════════════════════════════════════════════╝

Gerenciador de Fila de Missões (Rendering Queue).
Garante que a GPU não seja sobrecarregada e prioriza Tiers Pagos.
"""

import time
import json
import os
import sys
import sqlite3

# Append utils path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
try:
    from license_manager import LicenseManager, ImperialTier
except ImportError:
    LicenseManager = None

class MissionControl:
    def __init__(self):
        self.db_path = r"d:\Blender\blenderscripts\manifests\imperial_missions.db"
        self._conn = None
        self._init_db()

    def _get_connection(self):
        """Retorna uma conexão otimizada (Soberania SQLite)."""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path, timeout=10)
            self._conn.execute('PRAGMA journal_mode=WAL')
            self._conn.execute('PRAGMA synchronous=NORMAL')
            self._conn.execute('PRAGMA busy_timeout=5000')
        return self._conn

    def _init_db(self):
        """Inicializa o banco de dados imperial se não existir com otimizações WAL."""
        conn = self._get_connection()
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS missions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mission_id TEXT UNIQUE,
                    user_id TEXT,
                    priority INTEGER,
                    project_id TEXT,
                    status TEXT,
                    params TEXT,
                    created_at REAL
                )
            ''')
            conn.commit()

    def add_mission(self, user_id, license_key, project_id, params):
        """Adiciona uma nova missão à fila com prioridade (Atomic Write)."""
        priority = 10 # Default Basic
        if LicenseManager:
            lm = LicenseManager(license_key)
            if lm.tier == ImperialTier.ENTERPRISE: priority = 1
            elif lm.tier == ImperialTier.PRO: priority = 5
            
        mission_id = f"MSG_{int(time.time())}_{os.urandom(2).hex()}"
        
        conn = self._get_connection()
        try:
            with conn:
                conn.execute('''
                    INSERT INTO missions (mission_id, user_id, priority, project_id, status, params, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (mission_id, user_id, priority, project_id, 'QUEUED', json.dumps(params), time.time()))
            print(f"🚀 [Mission Control] Missão {mission_id} blindada (WAL Active).")
            return mission_id
        except sqlite3.OperationalError as e:
            print(f"🚨 [ERRO] Conflito de Lock no Banco: {e}")
            return None

    def process_next(self):
        """Recupera e marca o próximo trabalho da fila (Atomic Operation)."""
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        
        try:
            with conn:
                cursor = conn.cursor()
                # Buscar a missão de maior prioridade usando ORDER BY
                cursor.execute('''
                    SELECT * FROM missions 
                    WHERE status = 'QUEUED' 
                    ORDER BY priority ASC, created_at ASC 
                    LIMIT 1
                ''')
                row = cursor.fetchone()
                
                if not row:
                    return None
                
                mission = dict(row)
                # Marcar como processando imediatamente
                cursor.execute('UPDATE missions SET status = ? WHERE id = ?', ('PROCESSING', mission['id']))
                
            print(f"🎬 [Mission Control] SQLite → Iniciando Missão: {mission['mission_id']}")
            return mission
        except sqlite3.OperationalError as e:
            print(f"🚨 [ERRO] Falha no process_next: {e}")
            return None

    def clean_finished(self):
        """Remove missões finalizadas para economizar espaço."""
        conn = self._get_connection()
        with conn:
            conn.execute("DELETE FROM missions WHERE status = 'FINISHED'")

if __name__ == "__main__":
    mc = MissionControl()
    # Teste de adição de missões com prioridades diferentes
    mc.add_mission("user_01", "BASIC_KEY", "product-spin", {"samples": 32})
    time.sleep(1)
    mc.add_mission("user_02", "ENT_GOUVEIA", "luxury-reveal", {"samples": 512})
    mc.add_mission("CEO_GOUVEIA", "ENT_GOUVEIA", "f1-tunnel", {"quality": "ULTRA"})

    # Verificando a fila
    mc.process_next()
