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

pro_scene_fix = """
import bpy
import math

# 1. Limpeza Radical
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 2. Criação da Escultura Orgânica (Geometria Abstrata)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=2)
obj = bpy.context.active_object
obj.name = 'Abstract_Sculpture'

# Modificador Deslocamento para textura orgânica
mod = obj.modifiers.new(name="Displace", type='DISPLACE')
tex = bpy.data.textures.new(name="OrganicNoise", type='CLOUDS')
tex.noise_scale = 1.0
mod.texture = tex
mod.strength = 0.5
bpy.ops.object.shade_smooth()

# 3. Materiais AAA (Vidro Negro / Obsidian)
mat = bpy.data.materials.new(name="FGS_Obsidian")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()

node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
node_output = nodes.new(type='ShaderNodeOutputMaterial')

# Configuração para Blender 4.0+ (Nomes dos inputs mudaram levemente)
# Metallic, Roughness, etc.
node_principled.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1)
node_principled.inputs['Metallic'].default_value = 0.9
node_principled.inputs['Roughness'].default_value = 0.05

mat.node_tree.links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])
obj.data.materials.append(mat)

# 4. Atmosfera e Iluminação (Shadow Play)
# Criar Volume (Névoa Cinematográfica)
bpy.ops.mesh.primitive_cube_add(size=30)
vol_box = bpy.context.active_object
vol_mat = bpy.data.materials.new(name="FGS_Volumetric")
vol_mat.use_nodes = True
v_nodes = vol_mat.node_tree.nodes
v_nodes.clear()
v_principled = v_nodes.new(type='ShaderNodeVolumePrincipled')
v_output = v_nodes.new(type='ShaderNodeOutputMaterial')
v_principled.inputs['Density'].default_value = 0.05
vol_mat.node_tree.links.new(v_principled.outputs['Volume'], v_output.inputs['Volume'])
vol_box.data.materials.append(vol_mat)

# Luz Spot Dramática (Luz de Deus / God Rays)
light_data = bpy.data.lights.new(name="Dramatic_Spot", type='SPOT')
light_data.energy = 100000
light_data.spot_size = math.radians(35)
light_obj = bpy.data.objects.new(name="Dramatic_Spot", object_data=light_data)
bpy.context.collection.objects.link(light_obj)
light_obj.location = (8, -8, 12)
track = light_obj.constraints.new(type='TRACK_TO')
track.target = obj
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

# 5. Câmera Cinematográfica
cam_data = bpy.data.cameras.new(name="Main_Cam")
cam_data.lens = 50
cam_obj = bpy.data.objects.new(name="Main_Cam", object_data=cam_data)
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj
cam_obj.location = (12, -12, 5)
cam_track = cam_obj.constraints.new(type='TRACK_TO')
cam_track.target = obj
cam_track.track_axis = 'TRACK_NEGATIVE_Z'
cam_track.up_axis = 'UP_Y'

# DOF
cam_data.dof.use_dof = True
cam_data.dof.focus_object = obj
cam_data.dof.aperture_fstop = 0.5 # Fundo muito desfocado

# 6. Viewport Final
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'RENDERED'
                space.overlay.show_overlays = False
"""

cmd = {
    "type": "execute_code",
    "params": {
        "code": pro_scene_fix
    }
}

response = send_blender_command(cmd)
print(json.dumps(response, indent=2))
