# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: broll_orchestrator.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Ghost Automations                 ║
║   Script: broll_orchestrator.py                             ║
║   Função: Gerenciamento e Escalonamento de B-Rolls           ║
║           Geração em background baseada em tags/metadados    ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import json
import time
import subprocess
import sys
from pathlib import Path

# Setup paths
BASE_DIR = Path("D:/Blender/blenderscripts")
sys.path.append(str(BASE_DIR / "scripts" / "utils"))

BROLL_SCRIPT = BASE_DIR / "scripts/social/broll_generator.py"
OUTPUT_DIR = BASE_DIR / "renders/brolls"
QUEUE_FILE = BASE_DIR / "scripts/social/broll_queue.json"

# Configuração do executável do Blender (Pode ser alterado pelo usuário)
BLENDER_PATH = os.environ.get("BLENDER_PATH", "blender")

try:
    from notify_user import notify
except ImportError:
    notify = None

class BRollOrchestrator:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.blender_path = BLENDER_PATH
        self._init_queue()

    def _init_queue(self):
        """Inicializa arquivo de fila se não existir."""
        if not QUEUE_FILE.exists():
            with open(QUEUE_FILE, 'w') as f:
                json.dump([], f)

    def add_to_queue(self, conceito, prioridade="medium"):
        """Adiciona um novo conceito à fila de geração."""
        with open(QUEUE_FILE, 'r') as f:
            queue = json.load(f)
        
        # Evitar duplicados pendentes
        if any(item["conceito"] == conceito and item["status"] == "pending" for item in queue):
            print(f"⚠️ Conceito '{conceito}' já está na fila.")
            return

        queue.append({
            "conceito": conceito,
            "prioridade": prioridade,
            "status": "pending",
            "timestamp": time.time()
        })
        
        with open(QUEUE_FILE, 'w') as f:
            json.dump(queue, f, indent=4)
        print(f"✅ Conceito '{conceito}' adicionado à fila.")

    def run_next(self):
        """Executa o próximo item pendente da fila."""
        with open(QUEUE_FILE, 'r') as f:
            queue = json.load(f)
        
        pending = [item for item in queue if item["status"] == "pending"]
        if not pending:
            print("📭 Fila vazia ou nenhum item pendente.")
            return

        # Prioridade simples: ordena por prioridade (high > medium > low)
        priority_map = {"high": 0, "medium": 1, "low": 2}
        pending.sort(key=lambda x: priority_map.get(x["prioridade"], 1))
        
        item = pending[0]
        conceito = item["conceito"]
        
        print(f"🚀 Iniciando geração Ghost: {conceito.upper()}")
        item["status"] = "processing"
        item["start_time"] = time.time()
        
        # Salvar status antes de rodar
        with open(QUEUE_FILE, 'w') as f:
            json.dump(queue, f, indent=4)

        try:
            cmd = [
                self.blender_path,
                "--background",
                "--python", str(BROLL_SCRIPT),
                "--", conceito
            ]
            
            # Log de saída para auditoria
            log_dir = BASE_DIR / "renders" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"log_broll_{conceito}.txt"
            
            with open(log_file, 'w') as log:
                result = subprocess.run(cmd, stdout=log, stderr=log, text=True)
            
            if result.returncode == 0:
                item["status"] = "completed"
                print(f"✅ B-Roll '{conceito}' gerado com sucesso.")
                if notify:
                    notify(f"B-Roll '{conceito}' concluído!", "Ghost Automation")
            else:
                item["status"] = "failed"
                print(f"❌ Falha ao gerar B-Roll '{conceito}'. Verifique {log_file}")
                
        except Exception as e:
            item["status"] = "error"
            item["error_msg"] = str(e)
            print(f"💥 Erro crítico no orquestrador: {e}")
        
        item["end_time"] = time.time()
        with open(QUEUE_FILE, 'w') as f:
            json.dump(queue, f, indent=4)

if __name__ == "__main__":
    orchestrator = BRollOrchestrator()
    # Se rodado sem argumentos, processa o próximo
    if len(sys.argv) == 1:
        orchestrator.run_next()
    elif sys.argv[1] == "--add" and len(sys.argv) > 2:
        orchestrator.add_to_queue(sys.argv[2])
