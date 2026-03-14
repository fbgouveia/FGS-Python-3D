# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: notify_user.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import subprocess

def notify(message="Operação Concluída!", title="FGS Studio Status", sound=True):
    """Gera notificação sonora e visual no Windows."""
    # 1. Som via PowerShell
    if sound:
        sound_cmd = "powershell [console]::beep(1000, 300); [console]::beep(1200, 300)"
        subprocess.run(sound_cmd, shell=True)

    # 2. Notificação via PowerShell (Message Box)
    msg_cmd = f'powershell -Command "[System.Reflection.Assembly]::LoadWithPartialName(\'System.Windows.Forms\'); [System.Windows.Forms.MessageBox]::Show(\'{message}\', \'{title}\')"'
    subprocess.Popen(msg_cmd, shell=True)

if __name__ == "__main__":
    notify("Teste de notificação flexível", "FGS Debug")
