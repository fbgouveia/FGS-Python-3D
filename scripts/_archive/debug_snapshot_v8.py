import bpy
import os

print("\n--- DEBUG CENA SNAPSHOT ---")
blend_path = r"D:\Blender\blenderscripts\assets\props\nike.blend"

# Importar o Nike
with bpy.data.libraries.load(blend_path) as (data_from, data_to):
    data_to.objects = data_from.objects

hero = None
for obj in data_to.objects:
    if obj and obj.type == 'MESH' and "Plane" not in obj.name:
        bpy.context.collection.objects.link(obj)
        hero = obj
        break

if hero:
    print(f"Objeto Herói: {hero.name}")
    print(f"Localização: {hero.location}")
    print(f"Dimensões: {hero.dimensions}")
    print(f"Escala: {hero.scale}")
    
    # Criar câmera de segurança (Olhando de longe)
    cam_data = bpy.data.cameras.new("DebugCam")
    cam = bpy.data.objects.new("DebugCam", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = (15, 15, 15)
    
    # Track to hero
    track = cam.constraints.new(type='TRACK_TO')
    track.target = hero
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'
    
    bpy.context.scene.camera = cam
    bpy.context.scene.render.filepath = r"D:\Blender\blenderscripts\renders\drafts\DEBUG_V8_LOCATION.png"
    
    # Luz Solar para ver tudo
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 10))
    
    print("Renderizando frame de debug...")
    bpy.ops.render.render(write_still=True)
    print("Concluído!")
else:
    print("Nike não encontrado no blend.")
