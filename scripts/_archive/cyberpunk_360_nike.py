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

cyberpunk_360_code = """
import bpy
import math

# 1. Setup do Fundo Cyberpunk Ultra Realista (HDR + Emissivos)
world = bpy.context.scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
nodes.clear()
node_output = nodes.new(type='ShaderNodeOutputWorld')
node_bg = nodes.new(type='ShaderNodeBackground')
# Cor de fundo: Roxo profundo para ambiente cyberpunk
node_bg.inputs['Color'].default_value = (0.01, 0.0, 0.02, 1)
world.node_tree.links.new(node_bg.outputs['Background'], node_output.inputs['Surface'])

# Adicionar "Neblina de Neon" para realismo
bpy.ops.mesh.primitive_cube_add(size=30)
fog = bpy.context.active_object
fog.name = "Cyber_Fog"
fog_mat = bpy.data.materials.new(name="Cyber_Fog_Mat")
fog_mat.use_nodes = True
f_nodes = fog_mat.node_tree.nodes
f_nodes.clear()
f_principled = f_nodes.new(type='ShaderNodeVolumePrincipled')
f_output = f_nodes.new(type='ShaderNodeOutputMaterial')
f_principled.inputs['Density'].default_value = 0.03
f_principled.inputs['Emission Color'].default_value = (0.1, 0.0, 0.2, 1) # Brilho roxo na neblina
f_principled.inputs['Emission Strength'].default_value = 0.01
fog_mat.node_tree.links.new(f_principled.outputs['Volume'], f_output.inputs['Volume'])
fog.data.materials.append(fog_mat)

# 2. Luzes Neon Dinâmicas
# Luz Azul de um lado
light_data_a = bpy.data.lights.new(name="Neon_Blue", type='AREA')
light_data_a.energy = 20000
light_data_a.color = (0, 0.5, 1)
light_a = bpy.data.objects.new(name="Neon_Blue", object_data=light_data_a)
bpy.context.collection.objects.link(light_a)
light_a.location = (5, 0, 3)
light_a.rotation_euler = (0, math.radians(90), 0)

# Luz Rosa do outro
light_data_p = bpy.data.lights.new(name="Neon_Pink", type='AREA')
light_data_p.energy = 25000
light_data_p.color = (1, 0, 0.5)
light_p = bpy.data.objects.new(name="Neon_Pink", object_data=light_data_p)
bpy.context.collection.objects.link(light_p)
light_p.location = (-5, 0, 3)
light_p.rotation_euler = (0, math.radians(-90), 0)

# 3. Animação 360 Graus (Câmera Orbital)
# Criar um Empty no centro para a câmera girar ao redor
if "CAM_TARGET" not in bpy.data.objects:
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0,0))
    target = bpy.context.active_object
    target.name = "CAM_TARGET"
else:
    target = bpy.data.objects["CAM_TARGET"]

cam = bpy.data.objects.get("PRO_CAM") or bpy.context.scene.camera
if cam:
    cam.parent = target
    cam.location = (0, -12, 3) # Distância do tênis
    
    # Animar a rotação do TARGET (o Empty) para fazer a câmera girar
    target.animation_data_clear()
    target.rotation_mode = 'XYZ'
    target.keyframe_insert(data_path="rotation_euler", frame=1)
    target.rotation_euler[2] = math.radians(360)
    target.keyframe_insert(data_path="rotation_euler", frame=300) # 300 frames para ser "bem devagar"

    # Linear interpolation para loop perfeito
    for fcurve in target.animation_data.action.fcurves:
        for kp in fcurve.keyframe_points:
            kp.interpolation = 'LINEAR'

# 4. Configurar Viewport para Realismo Máximo
bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.use_gtao = True
bpy.context.scene.eevee.use_ssr = True
bpy.context.scene.eevee.use_volumetric_lights = True

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'RENDERED'
                space.overlay.show_overlays = False

print("Cyberpunk 360 sequence initialized!")
"""

cmd = {
    "type": "execute_code",
    "params": {
        "code": cyberpunk_360_code
    }
}

response = send_blender_command(cmd)
print(json.dumps(response, indent=2))
