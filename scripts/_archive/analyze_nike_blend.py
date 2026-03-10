import bpy
import os

BLEND_FILE = r"D:\Blender\blenderscripts\assets\props\nike.blend"

print("\n--- FGS: ANALISANDO NIKE.BLEND ---")
try:
    with bpy.data.libraries.load(BLEND_FILE) as (data_from, data_to):
        print(f"Objetos encontrados: {data_from.objects}")
        print(f"Coleções encontradas: {data_from.collections}")
        print(f"Meshes encontrados: {data_from.meshes}")
except Exception as e:
    print(f"❌ Erro ao ler arquivo: {e}")
print("--- FGS: FIM DA ANÁLISE ---\n")
