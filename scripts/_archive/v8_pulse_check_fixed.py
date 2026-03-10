import bpy
import os
import sys

# Protocolo FGS - V8 Pulse Check - REVISÃO FINAL CAMERA
BASE_DIR = r"D:\Blender\blenderscripts"
V8_SCRIPT = os.path.join(BASE_DIR, "scripts", "commercials", "nike_art_motion_v8_painterly.py")
OUTPUT_PULSE = os.path.join(BASE_DIR, "renders", "drafts", "V8_PULSE_CHECK.png")

# Importar o script V7/V8
with open(V8_SCRIPT, 'r', encoding='utf-8') as f:
    code = f.read()
    exec(code, globals(), {"__name__": "v8_snapshot"})

print("🔍 [Global Architect] Corrigindo Mira da Câmera para o Tênis...")

reset_scene()
setup_art_studio()

# Importar Nike
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
    # 1. Preparar Objeto
    bpy.context.view_layer.objects.active = nike
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    nike.location = (0, 0, 0)
    apply_art_materials(nike)
    
    # 2. Arrumar Câmera (FGS Track Mode)
    cam_data = bpy.data.cameras.new("PulseCam")
    cam_data.lens = 85
    cam = bpy.data.objects.new("PulseCam", cam_data)
    bpy.context.collection.objects.link(cam)
    
    # Posicionamento lateral dinâmico
    cam.location = (4, -4, 2)
    track = cam.constraints.new(type='TRACK_TO')
    track.target = nike
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    bpy.context.scene.camera = cam
    
    # 3. Luz heróica
    bpy.ops.object.light_add(type='AREA', location=(2, -2, 4))
    light = bpy.context.active_object
    light.data.energy = 5000
    light.data.color = (1, 1, 1)
    
    # 4. Render Setup
    bpy.context.scene.frame_set(30)
    bpy.context.scene.render.filepath = OUTPUT_PULSE
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 64
    
    print(f"🚀 Renderizando Snapshot V8 Real em: {OUTPUT_PULSE}")
    bpy.ops.render.render(write_still=True)
    print("✅ PREVIA VISIVEL GERADA!")
else:
    print("❌ Falha crítica: Nike não localizado.")
