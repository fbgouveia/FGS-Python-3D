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

visibility_fix = r'''
import bpy

# 1. Remover Névoa (Estava atrapalhando a visão inicial)
if "Cyber_Fog_Volume" in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects["Cyber_Fog_Volume"], do_unlink=True)

# 2. Ajustar Material (Tornar o tênis visível - Branco Brilhante)
mesh = bpy.data.objects.get("Mesh_0")
if mesh:
    mat = bpy.data.materials.get("FGS_Cyber_Nike")
    if mat and mat.use_nodes:
        bsdf = mat.node_tree.nodes.get('Principled BSDF')
        # Mudar para um cinza claro metálico para refletir os neons
        bsdf.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1)
        bsdf.inputs['Roughness'].default_value = 0.1 # Mais brilho

# 3. Trazer Câmera para perto (Close-up)
cam = bpy.data.objects.get("Master_Cinematic_Cam")
if cam:
    cam.location = (0, -8, 2) # Muito mais perto do tênis

# 4. Forçar Viewport Refresh e Foco
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        with bpy.context.temp_override(area=area):
            bpy.ops.view3d.view_all(center=True)
'''

send_blender_command({"type": "execute_code", "params": {"code": visibility_fix}})

# 5. Capturar novo screenshot para confirmar
screenshot_path = r"D:\Blender\blenderscripts\renders\agent_view_fix_check.png"
send_blender_command({
    "type": "get_viewport_screenshot", 
    "params": {"filepath": screenshot_path, "max_size": 1024}
})

print(f"Fix executed. Checking screenshot at {screenshot_path}")
