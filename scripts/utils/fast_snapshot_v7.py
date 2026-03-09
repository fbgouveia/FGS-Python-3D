import bpy
import os
import sys

# Protocolo FGS - Snapshot Ultra-Rápido (Cycles)
BASE_DIR = r"D:\Blender\blenderscripts"
V7_SCRIPT_PATH = os.path.join(BASE_DIR, "scripts", "commercials", "nike_multiverse_v7_sales_power.py")
OUTPUT_PATH = os.path.join(BASE_DIR, "renders", "drafts", "V7_SNAPSHOT_FRAME_70.png")

# Adicionar caminhos para os utilitários
UTILS_DIR = os.path.join(BASE_DIR, "scripts", "utils")
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# Importar o script V7 como um módulo ou executar suas definições
# Vamos usar o exec para carregar as funções sem rodar o main
with open(V7_SCRIPT_PATH, 'r', encoding='utf-8') as f:
    code = f.read()
    exec(code, globals())

print("🎬 [Director] Iniciando Snapshot de Elite - Frame 70...")

# 1. Setup da cena conforme o V7
reset_scene()
setup_multiverse_world()

# 2. Importar o Herói
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
    apply_premium_materials(nike)
    
    # 3. Elementos e Luz
    create_multiverse_elements()
    setup_sales_lighting()
    
    # 4. Câmera
    cam = setup_sales_camera(nike)
    
    # 5. Renderizar apenas o Frame 70
    bpy.context.scene.frame_set(70)
    bpy.context.scene.render.filepath = OUTPUT_PATH
    
    # Otimização para Snapshot rápido (Samples reduzidos para visualização)
    bpy.context.scene.cycles.samples = 128 
    
    print(f"🚀 Renderizando Frame 70 em: {OUTPUT_PATH}")
    bpy.ops.render.render(write_still=True)
    print(f"✅ SNAPSHOT CONCLUÍDO!")
else:
    print("❌ Erro: Nike não encontrado.")
