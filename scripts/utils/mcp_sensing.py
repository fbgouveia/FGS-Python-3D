# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: mcp_sensing.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import socket
import json
import os

def send_blender_command(command):
    host = 'localhost'
    port = 9876
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(json.dumps(command).encode('utf-8'))
            
            response_data = b''
            while True:
                chunk = s.recv(65536)
                if not chunk:
                    break
                response_data += chunk
                try:
                    # Test if we have a valid JSON
                    json.loads(response_data.decode('utf-8'))
                    break
                except:
                    continue
            return json.loads(response_data.decode('utf-8'))
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 1. Definir o caminho do screenshot
screenshot_path = r"D:\Blender\blenderscripts\renders\agent_view_check.png"
os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

# 2. Comando para capturar screenshot
print("Sensing Viewport...")
cmd_screenshot = {
    "type": "get_viewport_screenshot",
    "params": {
        "filepath": screenshot_path,
        "max_size": 1024
    }
}

response = send_blender_command(cmd_screenshot)

if response.get("status") == "success":
    print(f"SUCCESS: Screenshot salvo em {screenshot_path}")
    # O arquivo já está no disco, não precisamos de base64 aqui
else:
    print(f"FAIL: {response.get('message')}")

# 3. Sensing Scene Info
print("\nSensing Scene Info...")
info_resp = send_blender_command({"type": "get_scene_info"})
print(json.dumps(info_resp, indent=2))
