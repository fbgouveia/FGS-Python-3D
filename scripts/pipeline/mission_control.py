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

# Append utils path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
try:
    from license_manager import LicenseManager, ImperialTier
except ImportError:
    LicenseManager = None

class MissionControl:
    def __init__(self):
        self.queue_file = r"d:\Blender\blenderscripts\manifests\mission_queue.json"
        self.active_rendering = False
        
        if not os.path.exists(self.queue_file):
            self._save_queue([])

    def _save_queue(self, queue):
        with open(self.queue_file, 'w', encoding='utf-8') as f:
            json.dump(queue, f, indent=4)

    def _load_queue(self):
        with open(self.queue_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def add_mission(self, user_id, license_key, project_id, params):
        """Adiciona uma nova missão à fila com prioridade baseada no Tier."""
        queue = self._load_queue()
        
        # Determinar prioridade
        priority = 10 # Default Basic
        if LicenseManager:
            lm = LicenseManager(license_key)
            if lm.tier == ImperialTier.ENTERPRISE: priority = 1
            elif lm.tier == ImperialTier.PRO: priority = 5
            
        mission = {
            "mission_id": f"MSG_{int(time.time())}",
            "user_id": user_id,
            "priority": priority,
            "project_id": project_id,
            "status": "QUEUED",
            "params": params,
            "created_at": time.time()
        }
        
        queue.append(mission)
        # Ordenar por prioridade (menor número = maior prioridade) e depois por tempo
        queue.sort(key=lambda x: (x['priority'], x['created_at']))
        
        self._save_queue(queue)
        print(f"🚀 [Mission Control] Missão {mission['mission_id']} adicionada à fila (Prioridade {priority}).")
        return mission['mission_id']

    def process_next(self):
        """Processa a próxima missão da fila (Single Threaded to protect VRAM)."""
        queue = self._load_queue()
        
        if not queue:
            print("📭 [Mission Control] Fila vazia. Aguardando novos comandos...")
            return None
            
        # Pegar a missão com maior prioridade que não foi iniciada
        next_mission = None
        for m in queue:
            if m['status'] == "QUEUED":
                next_mission = m
                break
                
        if not next_mission:
            return None
            
        print(f"🎬 [Mission Control] Iniciando Missão: {next_mission['mission_id']} para Usuário {next_mission['user_id']}")
        
        # Atualizar status
        next_mission['status'] = "PROCESSING"
        self._save_queue(queue)
        
        # Aqui o Broker (Node.js) ou um Worker Python chamaria o Blender
        # Simulando execução...
        return next_mission

if __name__ == "__main__":
    mc = MissionControl()
    # Teste de adição de missões com prioridades diferentes
    mc.add_mission("user_01", "BASIC_KEY", "product-spin", {"samples": 32})
    time.sleep(1)
    mc.add_mission("user_02", "ENT_GOUVEIA", "luxury-reveal", {"samples": 512})
    
    # Verificando a fila
    mc.process_next()
