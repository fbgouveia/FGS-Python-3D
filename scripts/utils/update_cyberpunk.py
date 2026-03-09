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

cyberpunk_update = """
import bpy

# 1. Mudar Luzes para Cyberpunk (Azul e Rosa)
key = bpy.data.objects.get('Key_Light')
if key:
    key.data.color = (0.0, 0.5, 1.0) # Azul Neon
    key.data.energy = 8000

rim = bpy.data.objects.get('Rim_Light')
if rim:
    rim.data.color = (1.0, 0.0, 0.5) # Rosa/Magenta Neon
    rim.data.energy = 10000

# 2. Mudar Material para Ouro Escovado (Brilha mais com as luzes)
mat = bpy.data.materials.get('FGS_Premium_Metal')
if mat:
    node_principled = mat.node_tree.nodes.get('Principled BSDF')
    if node_principled:
        node_principled.inputs['Base Color'].default_value = (1.0, 0.6, 0.1, 1) # Ouro
        node_principled.inputs['Metallic'].default_value = 1.0
        node_principled.inputs['Roughness'].default_value = 0.2

# 3. Forçar o Viewport para modo RENDERED (importante para o usuário ver)
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'RENDERED'
                space.shading.use_composite = True
"""

cmd = {
    "type": "execute_code",
    "params": {
        "code": cyberpunk_update
    }
}

response = send_blender_command(cmd)
print(json.dumps(response, indent=2))
