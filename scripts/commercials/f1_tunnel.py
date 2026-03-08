import bpy
import math
import os

# ==============================================================================
# FELIPE GOUVEIA STUDIO - PYTHON 3D
# Projeto: F1 Tunnel Transition
# Versão: 1.0 (WOW Factor Hero)
# Descrição: Um carro de F1 atravessando uma pista iluminada para um túnel 
#            futurista neon em alta velocidade.
# ==============================================================================

def setup_f1_scene():
    # Limpeza
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Render Settings (Longo, 250 frames para drama)
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.frame_end = 250
    scene.render.fps = 30
    
    # --- PISTA E TÚNEL ---
    # Create a long floor
    bpy.ops.mesh.primitive_plane_add(size=100, location=(0, 40, 0))
    pista = bpy.context.active_object
    pista.scale[0] = 0.2 # Estreita
    
    # Material Asfalto Dark
    mat_pista = bpy.data.materials.new(name="Asfalto_Dark")
    mat_pista.use_nodes = True
    bsdf = mat_pista.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1)
    bsdf.inputs['Roughness'].default_value = 0.4
    pista.data.materials.append(mat_pista)
    
    # --- O TÚNEL (Começa no frame 100) ---
    bpy.ops.mesh.primitive_cylinder_add(radius=5, depth=100, location=(0, 100, 0))
    tunel = bpy.context.active_object
    tunel.rotation_euler[0] = math.radians(90)
    tunel.scale[0] = 0.8 # Oval
    
    # Material Túnel (Holográfico/Neon)
    mat_tunel = bpy.data.materials.new(name="Tunel_Neon")
    mat_tunel.use_nodes = True
    nodes = mat_tunel.node_tree.nodes
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (0.0, 0.0, 1.0, 1) # Azul Neon FGS
    emission.inputs['Strength'].default_value = 5.0
    
    # Wave stripes for neon lines
    wave = nodes.new('ShaderNodeTexWave')
    wave.inputs['Scale'].default_value = 20
    
    links = mat_tunel.node_tree.links
    links.new(wave.outputs['Color'], emission.inputs['Strength'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    tunel.data.materials.append(mat_tunel)

    # --- CARRO F1 (Representação) ---
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
    carro = bpy.context.active_object
    carro.name = "F1_Car"
    carro.scale = (0.8, 2.5, 0.4)
    
    # Material Carro (Vermelho Brilhante)
    mat_carro = bpy.data.materials.new(name="F1_Red")
    mat_carro.use_nodes = True
    bsdf_c = mat_carro.node_tree.nodes.get('Principled BSDF')
    bsdf_c.inputs['Base Color'].default_value = (1.0, 0.0, 0.1, 1)
    bsdf_c.inputs['Metallic'].default_value = 0.9
    bsdf_c.inputs['Roughness'].default_value = 0.1
    carro.data.materials.append(mat_carro)
    
    # --- ANIMAÇÃO VELOCIDADE ---
    carro.location[1] = -10
    carro.keyframe_insert(data_path="location", frame=1, index=1)
    
    carro.location[1] = 180
    carro.keyframe_insert(data_path="location", frame=250, index=1)
    
    # --- CÂMERA DINÂMICA (Atrás do carro com tremor) ---
    bpy.ops.object.camera_add(location=(0, -20, 2))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(85), 0, 0)
    bpy.context.scene.camera = cam
    cam.data.lens = 18 # Grande angular para velocidade
    
    # Parent camera to car
    cam.parent = carro
    
    # Motion Blur & Depth of Field
    cam.data.dof.use_dof = True
    cam.data.dof.focus_distance = 10
    cam.data.dof.aperture_fstop = 1.4
    
    # Render Settings for Output
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(base_dir, "renders", "finals")
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    
    scene.render.filepath = os.path.join(out_dir, "f1_tunnel_wow.mp4")
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    
    print(f"FGS Studio: Cena F1 configurada. Renderizando 250 frames para: {scene.render.filepath}")
    bpy.ops.render.render(animation=True)
    print("FGS Studio: Render Concluído!")

if __name__ == "__main__":
    setup_f1_scene()
