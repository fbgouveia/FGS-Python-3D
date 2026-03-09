import socket
import json

def send_blender_command(command):
    host = 'localhost'
    port = 9876
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(json.dumps(command).encode('utf-8'))
            response = s.recv(16384)
            return json.loads(response.decode('utf-8'))
    except Exception as e:
        return {"status": "error", "message": str(e)}

cyberpunk_fix = """
import bpy

# 1. Mudar Luzes para Cyberpunk (Azul e Rosa)
key = bpy.data.objects.get('Key_Light')
if key:
    key.data.color = (0.0, 0.5, 1.0) # Azul Neon
    key.data.energy = 8000

rim = bpy.data.objects.get('Rim_Light')
if rim:
    rim.data.color = (1.0, 0.0, 0.5) # Rosa/Magenta Neon
    rim.data.energy = 12000

# 2. Mudar Material para Ouro Escovado
mat = bpy.data.materials.get('FGS_Premium_Metal')
if mat:
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (1.0, 0.45, 0.05, 1) # Gold/Copper
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = 0.15

# 3. Forçar o Viewport para modo RENDERED corretamente
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'RENDERED'
"""

cmd = {
    "type": "execute_code",
    "params": {
        "code": cyberpunk_fix
    }
}

response = send_blender_command(cmd)
print(json.dumps(response, indent=2))
