import bpy
import math
import random
import os

# ==============================================================================
# FELIPE GOUVEIA STUDIO - PYTHON 3D
# Projeto: Samurai Duel Sparks
# Versão: 1.0 (WOW Factor Hero)
# Descrição: Dois samurais colidindo espadas com explosão de faíscas neon 
#            e câmera lenta dramática.
# ==============================================================================

def setup_samurai_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.frame_end = 150
    
    # --- CHÃO (Dark Mirror) ---
    bpy.ops.mesh.primitive_plane_add(size=50)
    floor = bpy.context.active_object
    mat_floor = bpy.data.materials.new(name="MirrorFloor")
    mat_floor.use_nodes = True
    bsdf = mat_floor.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1)
    bsdf.inputs['Metallic'].default_value = 1.0
    bsdf.inputs['Roughness'].default_value = 0.05
    floor.data.materials.append(mat_floor)

    # --- SAMURAIS (Silhuetas) ---
    def create_samurai(name, pos, color):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(pos, 0, 1.5))
        s = bpy.context.active_object
        s.name = name
        s.scale = (0.5, 0.3, 1.5)
        
        mat = bpy.data.materials.new(name=f"Mat_{name}")
        mat.use_nodes = True
        bsdf_s = mat.node_tree.nodes.get('Principled BSDF')
        bsdf_s.inputs['Base Color'].default_value = color
        s.data.materials.append(mat)
        
        # Espada
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=2, location=(pos, 1, 2))
        sword = bpy.context.active_object
        sword.rotation_euler[0] = math.radians(45 if pos < 0 else -45)
        sword.parent = s
        
        return s

    samurai1 = create_samurai("Samurai_Blue", -5, (0, 0.2, 1, 1))
    samurai2 = create_samurai("Samurai_White", 5, (1, 1, 1, 1))
    
    # --- ANIMAÇÃO IMPACTO ---
    samurai1.location[0] = -5
    samurai1.keyframe_insert(data_path="location", frame=1, index=0)
    samurai1.location[0] = -0.6
    samurai1.keyframe_insert(data_path="location", frame=60, index=0) # Impacto no frame 60
    
    samurai2.location[0] = 5
    samurai2.keyframe_insert(data_path="location", frame=1, index=0)
    samurai2.location[0] = 0.6
    samurai2.keyframe_insert(data_path="location", frame=60, index=0)
    
    # --- SISTEMA DE PARTÍCULAS (FAÍSCAS NO IMPACTO) ---
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0, 0.5, 2))
    emitter = bpy.context.active_object
    emitter.name = "Spark_Emitter"
    
    part = emitter.modifiers.new(name="Sparks", type='PARTICLE_SYSTEM')
    psys = part.particle_system
    pconf = psys.settings
    pconf.count = 500
    pconf.frame_start = 58
    pconf.frame_end = 65
    pconf.lifetime = 20
    pconf.velocity_normal = 10
    
    # Objeto da faísca (neon)
    bpy.ops.mesh.primitive_cube_add(size=0.05, location=(0,0,0))
    spark_obj = bpy.context.active_object
    spark_obj.name = "Spark_Particle"
    mat_spark = bpy.data.materials.new(name="Spark_Neon")
    mat_spark.use_nodes = True
    nodes = mat_spark.node_tree.nodes
    nodes.clear()
    out = nodes.new('ShaderNodeOutputMaterial')
    em = nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = (1, 0.8, 0.1, 1) # Yellow spark
    em.inputs['Strength'].default_value = 50
    mat_spark.node_tree.links.new(em.outputs['Emission'], out.inputs['Surface'])
    spark_obj.data.materials.append(mat_spark)
    
    pconf.render_type = 'OBJECT'
    pconf.instance_object = spark_obj
    
    # --- CÂMERA (Corte dramático / Slow Motion visual) ---
    bpy.ops.object.camera_add(location=(0, -8, 2))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.camera = cam
    
    # Animação de rotação da câmera no impacto
    cam.rotation_euler[2] = 0
    cam.keyframe_insert(data_path="rotation_euler", frame=50, index=2)
    cam.rotation_euler[2] = math.radians(10)
    cam.keyframe_insert(data_path="rotation_euler", frame=100, index=2)

    # Output
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(base_dir, "renders", "finals")
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    scene.render.filepath = os.path.join(out_dir, "samurai_duel_wow.mp4")
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'

    print(f"FGS Studio: Cena Samurai configurada. Renderizando para: {scene.render.filepath}")
    bpy.ops.render.render(animation=True)
    print("FGS Studio: Render Concluído!")

if __name__ == "__main__":
    setup_samurai_scene()
