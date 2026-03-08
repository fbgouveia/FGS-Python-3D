import bpy

def test_engine():
    print("Engine:", bpy.context.scene.render.engine)
    
    # Renderizar teste
    bpy.ops.mesh.primitive_monkey_add(location=(0,0,0))
    bpy.ops.object.light_add(type='POINT', location=(2, -2, 2))
    bpy.context.active_object.data.energy = 1000
    
    bpy.ops.object.camera_add(location=(0, -5, 0))
    cam = bpy.context.active_object
    cam.rotation_euler = (1.57, 0, 0)
    bpy.context.scene.camera = cam
    
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    bpy.context.scene.render.filepath = 'D:/Blender/blenderscripts/renders/finals/test_monkey.png'
    bpy.ops.render.render(write_still=True)

test_engine()
