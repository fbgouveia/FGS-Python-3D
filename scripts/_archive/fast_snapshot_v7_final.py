import bpy
import os
import sys

# Protocolo FGS - Snapshot Ultra-Rápido (Cycles) - FIXED v2
BASE_DIR = r"D:\Blender\blenderscripts"
V7_SCRIPT_PATH = os.path.join(BASE_DIR, "scripts", "commercials", "nike_multiverse_v7_sales_power.py")
OUTPUT_PATH = os.path.join(BASE_DIR, "renders", "drafts", "V7_SNAPSHOT_FRAME_70.png")

# Adicionar caminhos para os utilitários
UTILS_DIR = os.path.join(BASE_DIR, "scripts", "utils")
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

# Carregar as funções do V7 injetando-as no escopo global
with open(V7_SCRIPT_PATH, 'r', encoding='utf-8') as f:
    code = f.read()
    # Executar o código no contexto global para que as funções fiquem disponíveis
    # Mas definindo __name__ fora de __main__ para evitar execução do produce_v7()
    local_scope = {"__name__": "v7_module"}
    exec(code, globals(), local_scope)
    # Atualizar o escopo global com o que foi definido (funções, etc)
    globals().update(local_scope)

print("🎬 [Director] Iniciando Snapshot de Elite...")

# Verificar se as funções foram carregadas
if 'reset_scene' not in globals():
    print("❌ Erro ao carregar funções do script V7.")
    sys.exit(1)

# Executar Setup
reset_scene()
setup_multiverse_world()

# Importar o Herói
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
    create_multiverse_elements()
    setup_sales_lighting()
    setup_sales_camera(nike)
    
    # Configurar Frame 70
    bpy.context.scene.frame_set(70)
    bpy.context.scene.render.filepath = OUTPUT_PATH
    
    # Cycles 64 samples para rapidez
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 64
    
    print(f"🚀 Renderizando Frame 70 em: {OUTPUT_PATH}")
    bpy.ops.render.render(write_still=True)
    print(f"✅ SNAPSHOT SALVO!")
else:
    print("❌ Nike não encontrado.")
