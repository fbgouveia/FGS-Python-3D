import bpy
import os
import sys
import math

# Protocolo FGS - V8 Pulse Check - FIXED v3 (Standalone Functions)
BASE_DIR = r"D:\Blender\blenderscripts"
OUTPUT_PULSE = os.path.join(BASE_DIR, "renders", "drafts", "V8_PULSE_CHECK.png")

def reset_scene():
    if bpy.context.active_object: bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for b in [bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights, bpy.data.images]:
        for i in b: b.remove(i)

def setup_art_studio():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    world = bpy.data.worlds.new("PulseWorld")
    scene.world = world
    world.use_nodes = True
    node_bg = world.node_tree.nodes.new('ShaderNodeBackground')
    node_bg.inputs['Color'].default_value = (0.35, 0.75, 1.0, 1) # Azul Sky
    node_out = world.node_tree.nodes.new('ShaderNodeOutputWorld')
    world.node_tree.links.new(node_bg.outputs['Background'], node_out.inputs['Surface'])

def apply_simple_art(obj):
    mat = bpy.data.materials.new(name="ArtMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (1, 1, 1, 1)
    if not obj.data.materials:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

print("🔍 [Global Architect] Snapshot Tático V8 em alta visibilidade...")

reset_scene()
setup_art_studio()

blend_path = os.path.join(BASE_DIR, "assets", "props", "nike.blend")
with bpy.data.libraries.load(blend_path) as (data_from, data_to):
    data_to.objects = data_from.objects

nike = None
for obj in data_to.objects:
    if obj and obj.type == 'MESH' and "Plane" not in obj.name:
        bpy.context.collection.objects.link(obj)
        nike = obj
        break

if nike:
    # 1. Objeto no Centro
    bpy.context.view_layer.objects.active = nike
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    nike.location = (0, 0, 0)
    apply_simple_art(nike)

    # 2. Câmera Próxima (Macro Portrait)
    cam_data = bpy.data.cameras.new("MacroCam")
    cam_data.lens = 85
    cam = bpy.data.objects.new("MacroCam", cam_data)
    bpy.context.collection.objects.link(cam)
    
    # Posicionar câmera em uma visada clássica
    cam.location = (3, -2, 1)
    track = cam.constraints.new(type='TRACK_TO')
    track.target = nike
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    bpy.context.scene.camera = cam
    
    # 3. Luz Forte
    bpy.ops.object.light_add(type='AREA', location=(2, -2, 4))
    light = bpy.context.active_object
    light.data.energy = 5000
    
    # 4. Render
    bpy.context.scene.render.filepath = OUTPUT_PULSE
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.cycles.samples = 64
    
    print(f"🚀 Renderizando em: {OUTPUT_PULSE}")
    bpy.ops.render.render(write_still=True)
    print("✅ PREVIA VISIVEL GERADA!")
else:
    print("❌ Erro: Nike não encontrado.")
