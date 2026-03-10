import bpy
import os

BLEND_FILE = r"D:\Blender\blenderscripts\assets\props\nike.blend"

print("\n--- FGS ARCHITECT: DEEP ANALYSIS OF NIKE.BLEND ---")
try:
    with bpy.data.libraries.load(BLEND_FILE) as (data_from, data_to):
        print(f"Collections: {data_from.collections}")
        print(f"Objects: {data_from.objects}")

    # Temporary Link to inspect details
    with bpy.data.libraries.load(BLEND_FILE, link=False) as (data_from, data_to):
        data_to.objects = data_from.objects

    for obj in data_to.objects:
        if obj is not None:
            print(f"Object Found: '{obj.name}' | Type: {obj.type} | Dimensions: {obj.dimensions}")
            # Do not link to scene, just inspect data
            
except Exception as e:
    print(f"❌ Error: {e}")
print("--- END ANALYSIS ---\n")
