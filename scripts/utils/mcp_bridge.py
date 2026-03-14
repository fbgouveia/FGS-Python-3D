# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: mcp_bridge.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import socket
import json
import time

class BlenderBridge:
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port

    def send(self, command_type, params=None):
        payload = {"type": command_type, "params": params or {}}
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10)
                s.connect((self.host, self.port))
                s.sendall(json.dumps(payload).encode('utf-8'))
                
                # Receive response (handle large buffers)
                response_data = b''
                while True:
                    chunk = s.recv(16384)
                    if not chunk:
                        break
                    response_data += chunk
                    if len(chunk) < 16384: # Simple termination check for JSON
                        break
                
                return json.loads(response_data.decode('utf-8'))
        except Exception as e:
            return {"status": "error", "message": f"Bridge Error: {str(e)}"}

    def get_info(self):
        return self.send("get_scene_info")

    def execute(self, code):
        return self.send("execute_code", {"code": code})

if __name__ == "__main__":
    bridge = BlenderBridge()
    # 1. Check Scene
    print("--- SCENE INFO ---")
    info = bridge.get_info()
    print(json.dumps(info, indent=2))
    
    # 2. Try to move the cube (if it exists) to verify interaction
    print("\n--- TEST INTERACTION ---")
    res = bridge.execute("import bpy; obj = bpy.data.objects.get('Cube'); if obj: obj.location.x += 1.0; print('Moved Cube')")
    print(json.dumps(res, indent=2))
