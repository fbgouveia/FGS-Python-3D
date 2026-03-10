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

pro_scene_code = """
import bpy
import math
import random

# 1. Limpeza Radical
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 2. Criação da Escultura Orgânica (Geometria Abstrata)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=2)
obj = bpy.context.active_object
obj.name = 'Abstract_Sculpture'
obj.display_type = 'TEXTURED'

# Adicionar Modificador de Deslocamento para forma orgânica
mod = obj.modifiers.new(name="Displace", type='DISPLACE')
tex = bpy.data.textures.new(name="OrganicNoise", type='CLOUDS')
tex.noise_scale = 1.5
mod.texture = tex
mod.strength = 0.8

# Animar a escultura (Pulsação)
obj.scale = (1, 1, 1)
obj.keyframe_insert(data_path="scale", frame=1)
obj.scale = (1.2, 0.9, 1.1)
obj.keyframe_insert(data_path="scale", frame=125)
obj.scale = (1, 1, 1)
obj.keyframe_insert(data_path="scale", frame=250)

# 3. Materiais AAA (Iridescente / Vidro Negro)
mat = bpy.data.materials.new(name="FGS_Obsidian_Edge")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()

node_principled = nodes.new(type='ShaderNodeBsdfPrincipled')
node_output = nodes.new(type='ShaderNodeOutputMaterial')
node_fresnel = nodes.new(type='ShaderNodeFresnel')
node_mix = nodes.new(type='ShaderNodeMixRGB')

# Configurar Fresnel para brilho nas bordas
node_fresnel.inputs['IOR'].default_value = 1.45
node_mix.inputs['Color1'].default_value = (0.01, 0.01, 0.01, 1) # Base preta
node_mix.inputs['Color2'].default_value = (0.0, 0.8, 1.0, 1)   # Brilho ciano nas bordas

mat.node_tree.links.new(node_fresnel.outputs['Fac'], node_mix.inputs['Fac'])
mat.node_tree.links.new(node_mix.outputs['Color'], node_principled.inputs['Base Color'])
node_principled.inputs['Metallic'].default_value = 0.9
node_principled.inputs['Roughness'].default_value = 0.1
node_principled.inputs['Clearcoat'].default_value = 1.0

mat.node_tree.links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])
obj.data.materials.append(mat)

# 4. Iluminação Cinematográfica (God Rays Setup)
# Criar uma caixa de volume para a fumaça/névoa
bpy.ops.mesh.primitive_cube_add(size=20)
vol_box = bpy.context.active_object
vol_box.name = 'Volume_Container'
vol_mat = bpy.data.materials.new(name="FGS_Atmosphere")
vol_mat.use_nodes = True
v_nodes = vol_mat.node_tree.nodes
v_nodes.clear()
node_vol = v_nodes.new(type='ShaderNodeVolumePrincipled')
node_vol_out = v_nodes.new(type='ShaderNodeOutputMaterial')
node_vol.inputs['Density'].default_value = 0.02
vol_mat.node_tree.links.new(node_vol.outputs['Volume'], node_vol_out.inputs['Volume'])
vol_box.data.materials.append(vol_mat)

# Key Light (Luz de Destaque)
light_data = bpy.data.lights.new(name="Main_Spot", type='SPOT')
light_data.energy = 50000
light_data.spot_size = math.radians(45)
light_data.spot_blend = 1.0
light_obj = bpy.data.objects.new(name="Main_Spot", object_data=light_data)
bpy.context.collection.objects.link(light_obj)
light_obj.location = (5, -5, 10)
# Apontar para o centro
constraint = light_obj.constraints.new(type='TRACK_TO')
constraint.target = obj
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# 5. Câmera Orbital (Sweeping Shot)
cam_data = bpy.data.cameras.new(name="Cinematic_Master")
cam_data.lens = 50
cam_obj = bpy.data.objects.new(name="Cinematic_Master", object_data=cam_data)
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Animar câmera orbitando
cam_obj.location = (15, -15, 8)
cam_obj.keyframe_insert(data_path="location", frame=1)
cam_obj.location = (-15, -10, 5)
cam_obj.keyframe_insert(data_path="location", frame=250)

cam_constraint = cam_obj.constraints.new(type='TRACK_TO')
cam_constraint.target = obj
cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
cam_constraint.up_axis = 'UP_Y'

# Depth of Field
cam_data.dof.use_dof = True
cam_data.dof.focus_object = obj
cam_data.dof.aperture_fstop = 0.8

# 6. Finalização de Viewport
bpy.context.scene.render.engine = 'CYCLES' if bpy.context.scene.render.engine == 'EEVEE' else 'EEVEE' # Toggle para garantir refresh
bpy.context.scene.render.engine = 'EEVEE' # Voltando para EEVEE para performance
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'RENDERED'
                space.overlay.show_overlays = False # Esconde as linhas para look limpo
"""

cmd = {
    "type": "execute_code",
    "params": {
        "code": pro_scene_code
    }
}

response = send_blender_command(cmd)
print(json.dumps(response, indent=2))
