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
            response = s.recv(65536)
            return json.loads(response.decode('utf-8'))
    except Exception as e:
        return {"status": "error", "message": str(e)}

nike_path = r"D:\Blender\blenderscripts\assets\props\nike.fbx"

# Script simplificado para estabilizar a conexão
master_script = r'''
import bpy
import os

# 1. Limpeza
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 2. Importar Nike
path = r"''' + nike_path + r'''"
if os.path.exists(path):
    bpy.ops.import_scene.fbx(filepath=path)
    
# 3. Listar nomes (Crucial para o usuario dirigir)
mesh_names = [o.name for o in bpy.data.objects if o.type == 'MESH']
print(f"NIKE_PARTS: {mesh_names}")

# 4. Forçar Rendered Mode (Sem poll error)
for window in bpy.context.window_manager.windows:
    for area in window.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'
                    space.overlay.show_overlays = False

# 5. Aplicar Vermelho Riley em algo obvio
target = bpy.data.objects.get('Circle.001') or bpy.data.objects.get('Nike') # Exemplos
if not target:
    mesh_objs = [o for o in bpy.data.objects if o.type == 'MESH']
    if mesh_objs: target = mesh_objs[0]

if target:
    mat = bpy.data.materials.new(name="FGS_DIRECT")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (1.0, 0, 0, 1) # Red
    if target.data.materials:
        target.data.materials[0] = mat
    else:
        target.data.materials.append(mat)
    print(f"COLORED: {target.name}")
'''

cmd = {
    "type": "execute_code",
    "params": {
        "code": master_script
    }
}

response = send_blender_command(cmd)
print(json.dumps(response, indent=2))
