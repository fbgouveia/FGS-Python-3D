# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: nike_auto_render_v2.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: nike_auto_render_v2.py (PRODUÇÃO)                 ║
║   Função: Automação Total Nike - O Coração do Projeto       ║
║   Versão: 2.1.0 (Smart Import + AU)                         ║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import os
import sys

# --- CONFIGURAÇÃO DE CAMINHOS ---
BASE_DIR = r"D:\Blender\blenderscripts"
UTILS_DIR = os.path.join(BASE_DIR, "scripts", "utils")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "props")
OUTPUT_DIR = os.path.join(BASE_DIR, "renders", "finals")

# Adiciona o diretório de utilitários ao path do Python
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# --- IMPORTAÇÃO DOS MÓDULOS UNIVERSAIS (AU) ---
try:
    from scene_setup import limpar_cena, setup_scene
    from lighting_system import LightingSystem
    from camera_system import CameraSystem
    from materials_library import MaterialLibrary
    from render_manager import RenderManager
    print("✅ FGS: Módulos AU carregados.")
except ImportError as e:
    print(f"❌ FGS: Erro de Import: {e}")
    # Fallback to local import if path fails
    print("🔍 Tentando carregar via manual path...")
    
# --- PARÂMETROS DO PROJETO ---
MODEL_PATH = os.path.join(ASSETS_DIR, "nike.blend")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "nike_automation_final.mp4")

def execute_pipeline():
    print(f"\n🚀 FGS: Iniciando Pipeline Nike V2.1")
    
    # 1. Setup de Cena
    limpar_cena()
    scene = setup_scene(fps=30, duracao_segundos=6, cor_fundo=(0,0,0,1))
    
    # 2. Importação do Ativo (Nike) - MODO SMART
    print(f"📦 FGS: Importando de {MODEL_PATH}...")
    
    with bpy.data.libraries.load(MODEL_PATH) as (data_from, data_to):
        # Tentamos objetos primeiro, se não houver coleções
        data_to.objects = data_from.objects
        data_to.collections = data_from.collections

    nike_main_obj = None

    # Linkar coleções (geralmente melhor para modelos complexos)
    for coll in data_to.collections:
        if coll is not None and coll.name != "RigidBodyWorld":
            bpy.context.scene.collection.children.link(coll)
            print(f"✅ FGS: Coleção '{coll.name}' importada.")
            # Buscar o primeiro mesh na coleção para ser o alvo da câmera
            for obj in coll.all_objects:
                if obj.type == 'MESH':
                    nike_main_obj = obj
                    break

    # Se não houver coleções úteis, linkar objetos soltos
    if not nike_main_obj:
        for obj in data_to.objects:
            if obj is not None and obj.type == 'MESH':
                bpy.context.collection.objects.link(obj)
                nike_main_obj = obj
                print(f"✅ FGS: Objeto '{obj.name}' importado.")
                break

    if not nike_main_obj:
        print("❌ FGS: Não consegui encontrar um Tênis (Mesh) no arquivo.")
        # Criar mockup para não sair tela preta se tudo falhar
        bpy.ops.mesh.primitive_cube_add(size=1)
        nike_main_obj = bpy.context.active_object
        nike_main_obj.name = "DEBUG_CUBE"

    # Centralizar o "Nike"
    nike_main_obj.location = (0, 0, 0)
    
    # 3. Iluminação Cinemática
    luzes = LightingSystem()
    luzes.preset("luxo")
    luzes.rim("Logo_Spot", posicao=(0, -2, 2.5), energia=150)

    # 4. Câmera Dinâmica
    cam_sys = CameraSystem(scene)
    cam = cam_sys.product_orbit("CAM_AUTOMATED", raio=5.5, altura=1.6, fov=42)
    
    # Orbit Completa
    cam_sys.orbit(cam, alvo=(0,0,0), raio=5.5, altura=1.6, frame_fim=scene.frame_end)
    # Suave Zoom In
    cam_sys.dolly(cam, inicio=(0,-5.5,1.6), fim=(0,-4.5,1.2), frames=(1, 180))
    
    scene.camera = cam

    # 5. Render Express
    render = RenderManager()
    render.preset("youtube", output=OUTPUT_FILE) # Youtube é melhor que comercial p/ EEVEE rápido
    render.ativar_compositing(estilo="cinematico")
    render.ativar_motion_blur(shutter=0.5)

    # 6. EXECUTAR
    print(f"🎬 FGS: Renderizando Coração do Projeto...")
    bpy.ops.render.render(animation=True)
    print(f"\n✨ FGS: Processo Finalizado: {OUTPUT_FILE}")

if __name__ == "__main__":
    execute_pipeline()
