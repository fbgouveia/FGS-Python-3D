# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: nike_global_architect_v3.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   THE GLOBAL CREATIVE ARCHITECT — Felipe Gouveia Studio     ║
║   Script: nike_international_standard_v3.py                 ║
║   Standard: Nike Global (Sport/Heroic/Dynamic)               ║
║   Versão: 3.0.0 (Unlimited Autonomy Protocol)               ║
╚══════════════════════════════════════════════════════════════╝

Este script implementa o protocolo 'Global Creative Architect'.
É um sistema autônomo de produção que garante enquadramento 
matemático, iluminação heróica e renderização Apple-level.
"""

import bpy
import os
import sys
import math

# --- 1. GESTÃO E INFRAESTRUTURA AUTÔNOMA ---
BASE_DIR = r"D:\Blender\blenderscripts"
UTILS_DIR = os.path.join(BASE_DIR, "scripts", "utils")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "props")
OUTPUT_DIR = os.path.join(BASE_DIR, "renders", "finals")

# Garantir existência de diretórios
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Adiciona utilitários ao path
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# --- 2. PROTOCOLO DE NORMALIZAÇÃO E LIMPEZA (Cena Virgem) ---
def reset_scene():
    print("🧹 [Architect] Iniciando Auto-Cleanup: Resetando para cena virgem...")
    if bpy.context.active_object and bpy.context.active_object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # Deletar tudo
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Limpar órfãos
    for block in bpy.data.meshes: bpy.data.meshes.remove(block)
    for block in bpy.data.materials: bpy.data.materials.remove(block)
    for block in bpy.data.cameras: bpy.data.cameras.remove(block)
    for block in bpy.data.lights: bpy.data.lights.remove(block)

# --- 3. IMPORTAÇÃO E VALIDAÇÃO DE ASSETS ---
def import_validate_asset(path):
    print(f"📦 [Architect] Validando Asset: {path}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ CRITICAL ERROR: Asset não encontrado em {path}")

    with bpy.data.libraries.load(path) as (data_from, data_to):
        data_to.collections = data_from.collections
        data_to.objects = data_from.objects

    main_obj = None
    
    # Smart Link
    if data_to.collections:
        for coll in data_to.collections:
            if coll and coll.name != "RigidBodyWorld":
                bpy.context.scene.collection.children.link(coll)
                for obj in coll.all_objects:
                    if obj.type == 'MESH':
                        main_obj = obj
                        break
    
    if not main_obj and data_to.objects:
        for obj in data_to.objects:
            if obj and obj.type == 'MESH':
                bpy.context.collection.objects.link(obj)
                main_obj = obj
                break

    if not main_obj:
        raise ValueError("❌ CRITICAL ERROR: Nenhum Mesh válido encontrado no arquivo .blend")

    # Protocolo Anti-Erro do Objeto
    bpy.context.view_layer.objects.active = main_obj
    main_obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    main_obj.location = (0, 0, 0)
    main_obj.rotation_euler = (0, 0, 0)
    main_obj.scale = (1, 1, 1)
    
    return main_obj

# --- 4. AUTO-FRAMING MATEMÁTICO (Newtonian Camera) ---
def setup_smart_camera(target):
    print("📷 [Architect] Calculando enquadramento matemático (85mm Prime)...")
    
    # FOV Ultra-limpo (85mm)
    cam_data = bpy.data.cameras.new("SmartCam")
    cam_data.lens = 85
    cam_data.sensor_width = 36
    cam_obj = bpy.data.objects.new("SmartCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    # Cálculo de distância baseado no Bounding Box (Enquadramento Heróico)
    bbox = [target.matrix_world @ Vector(corner) for corner in target.bound_box]
    dim = target.dimensions
    max_dim = max(dim.x, dim.y, dim.z)
    
    # Posicionamento Dinâmico (Newtonian Orbit)
    dist = max_dim * 5  # Ajuste para 85mm
    cam_obj.location = (dist, -dist, max_dim * 1.5)
    
    # Track To Constrain
    constraint = cam_obj.constraints.new(type='TRACK_TO')
    constraint.target = target
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    
    return cam_obj

# --- 5. ILUMINAÇÃO DE ELITE (Sport/Heroic DNA) ---
def setup_international_lighting():
    print("💡 [Architect] Calibrando Iluminação DNA Nike (Sport/Heroic)...")
    
    # Key Light (Dramática)
    bpy.ops.object.light_add(type='AREA', location=(-3, 3, 5))
    key = bpy.context.active_object
    key.data.energy = 800
    key.data.size = 3
    key.data.color = (1, 0.95, 0.9) # Quente suave
    key.rotation_euler = (0.7, 0, -0.7)

    # Rim Light (Silhueta Heron)
    bpy.ops.object.light_add(type='AREA', location=(2, -4, 2))
    rim = bpy.context.active_object
    rim.data.energy = 1200
    rim.data.size = 0.5
    rim.data.color = (0.9, 0.95, 1) # Frio para contraste
    
    # Kick Light (Highlight Tátil)
    bpy.ops.object.light_add(type='SPOT', location=(0, 0, 3))
    kick = bpy.context.active_object
    kick.data.energy = 500
    kick.data.spot_size = math.radians(25)

# --- 6. RENDER ENGINE & OUTPUT (AgX International Standard) ---
def configure_render_engine(output_path):
    print("⚙️ [Architect] Configurando Motor de Saída (EEVEE Next + AgX)...")
    scene = bpy.context.scene
    
    # Motor e Opticas
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.view_settings.view_transform = 'AgX' # Padrão Cinema
    scene.view_settings.look = 'High Contrast'
    
    # Qualidade
    scene.eevee.shadow_ray_count = 64
    scene.render.film_transparent = False
    
    # FFMPEG H264
    scene.render.filepath = output_path
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    
    # Resolução
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920 # Vertical Social Standard
    scene.render.resolution_percentage = 100
    scene.frame_start = 1
    scene.frame_end = 180 # 6 segundos @ 30fps

# --- 7. EXECUÇÃO ORQUESTRADA ---
def run_production():
    try:
        reset_scene()
        
        target_obj = import_validate_asset(os.path.join(ASSETS_DIR, "nike.blend"))
        
        setup_international_lighting()
        
        camera = setup_smart_camera(target_obj)
        
        configure_render_engine(os.path.join(OUTPUT_DIR, "nike_global_standard_v3.mp4"))
        
        # Módulos de Pós-Produção (Opcional, mas Ninja)
        scene = bpy.context.scene
        scene.use_nodes = True
        
        print("\n🚀 [Architect] Sistema Pronto. Iniciando Renderização de Elite...")
        bpy.ops.render.render(animation=True, write_still=True)
        print(f"\n✨ [Architect] Entrega Finalizada: {scene.render.filepath}")
        
    except Exception as e:
        print(f"\n❌ [Architect] FALHA NO PROTOCOLO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    from mathutils import Vector # Garantir import
    run_production()
