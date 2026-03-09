"""
FGS V8 Pulse Check - Snapshot Rápido
Captura a estética do Masterpiece V8 sem interromper a produção do vídeo.
"""
import bpy
import os
import sys

BASE_DIR = r"D:\Blender\blenderscripts"
V8_SCRIPT = os.path.join(BASE_DIR, "scripts", "commercials", "nike_art_motion_v8_painterly.py")
OUTPUT_PULSE = os.path.join(BASE_DIR, "renders", "drafts", "V8_PULSE_CHECK.png")

# Carregar funções do V8 injetando-as no escopo global
with open(V8_SCRIPT, 'r', encoding='utf-8') as f:
    code = f.read()
    local_scope = {"__name__": "v8_snapshot"}
    exec(code, globals(), local_scope)
    globals().update(local_scope)

print("🔍 [Global Architect] Realizando Pulse Check da V8...")

# 1. Setup base
reset_scene()
setup_art_studio()

# 2. Importar o Nike
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "props")
blend_path = os.path.join(ASSETS_DIR, "nike.blend")
with bpy.data.libraries.load(blend_path) as (data_from, data_to):
    data_to.objects = data_from.objects

nike = None
for obj in data_to.objects:
    if obj and obj.type == 'MESH' and "Plane" not in obj.name:
        bpy.context.collection.objects.link(obj)
        nike = obj
        break

if nike:
    bpy.context.view_layer.objects.active = nike
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    nike.location = (0, 0, 0)
    
    # 3. Aplicar estilo e preparar um frame de impacto (Frame 30)
    apply_art_materials(nike)
    setup_art_production(nike)
    
    bpy.context.scene.frame_set(30)
    bpy.context.scene.render.filepath = OUTPUT_PULSE
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    
    # RENDER RÁPIDO: 32 samples para não pesar no GPU que já está renderizando o vídeo
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 32
    bpy.context.scene.cycles.use_denoising = True
    
    print(f"🚀 Capturando Pulse em: {OUTPUT_PULSE}")
    bpy.ops.render.render(write_still=True)
    print(f"✅ PULSE CHECK COMPLETE!")
else:
    print("❌ Erro: Nike não encontrado.")
