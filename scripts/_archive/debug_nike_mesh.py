import bpy
import os

print("\n--- ANALISE DE OBJETO ACURADA ---")
blend_path = r"D:\Blender\blenderscripts\assets\props\nike.blend"

if os.path.exists(blend_path):
    with bpy.data.libraries.load(blend_path) as (data_from, data_to):
        print(f"Objetos no arquivo: {data_from.objects}")
        
    bpy.ops.wm.open_mainfile(filepath=blend_path)
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            print(f"MESH: {obj.name}")
            print(f" - Polígonos: {len(obj.data.polygons)}")
            print(f" - Materiais: {[m.name for m in obj.data.materials if m]}")
            # Verificar se tem modificadores ativos (como Multires ou Sculpt)
            print(f" - Modificadores: {[m.type for m in obj.modifiers]}")
else:
    print("Arquivo não encontrado.")
