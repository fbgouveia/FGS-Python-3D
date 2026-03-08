import bpy
import math
import os

# ==============================================================================
# FELIPE GOUVEIA STUDIO - PYTHON 3D
# Projeto: Comercial (Produto Girando 360 Graus)
# Versão: 1.0
# Descrição: Template cinematográfico de um objeto central girando lentamente,
#            com fundo infinito (backdrop) curvo, iluminação dramática de 
#            estúdio (3 pontos) e profundidade de campo (DoF).
# ==============================================================================

def clean_scene():
    """Limpa todos os objetos, materiais, luzes e câmeras da cena atual."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Limpa dados residuais soltos na memória
    for block in [bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights, bpy.data.curves]:
        for item in block:
            block.remove(item)

def setup_render_settings():
    """Configurações otimizadas para o Blender Eevee Next (4.2 LTS)."""
    scene = bpy.context.scene
    
    # Resolução (1920x1080 - Full HD)
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    
    # Taxa de quadros (30 fps para suavidade em redes sociais)
    scene.render.fps = 30
    
    # Duração (150 frames = 5 segundos)
    scene.frame_start = 1
    scene.frame_end = 150
    
    # Motor de Renderização (Eevee Next)
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    
    # Configurações de Luxo (Eevee Next / 4.2)
    scene.eevee.use_shadows = True
    scene.eevee.use_raytracing = True # Raytracing obrigatório para materiais premium
    scene.eevee.ray_tracing_method = 'SCREEN'
    scene.eevee.use_bloom = True # Reativando Bloom (ainda presente na API 4.2 local)
    scene.display_settings.display_device = 'sRGB'
    scene.view_settings.view_transform = 'AgX' # Melhor gerenciamento de cor moderno
    # scene.view_settings.look = 'High Contrast'
    
    # Cor de Fundo do Mundo (Preto Profundo para destacar a luz)
    world = scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get('Background')
    if bg_node:
        bg_node.inputs[0].default_value = (0.01, 0.01, 0.01, 1) # Quase preto
        bg_node.inputs[1].default_value = 1.0 # Intensidade

    # --- Configurações de Output (Exportação MP4) ---
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(base_dir, "renders", "finals")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    scene.render.filepath = os.path.join(out_dir, "comercial_360_auto.mp4")
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'

def create_backdrop():
    """Cria um fundo fotográfico infinito (Sweep Backdrop)."""
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 2, -1))
    backdrop = bpy.context.active_object
    backdrop.name = "Studio_Backdrop"
    
    # Entra no modo de edição para curvar a parede do fundo
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Seleciona as bordas traseiras do plano e as levanta
    backdrop.data.vertices[2].co[2] = 10
    backdrop.data.vertices[3].co[2] = 10
    
    # Adicionamos um Bevel Modifer para curvar a junção entre o chão e a parede
    bevel = backdrop.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 20
    bevel.width = 3.0
    
    # Aplica sombreamento suave
    bpy.ops.object.shade_smooth()
    
    # Material do Fundo (Cinza Fosco)
    mat = bpy.data.materials.new(name="Material_Backdrop")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if bsdf:
        bsdf.inputs['Base Color'].default_value = (0.05, 0.05, 0.057, 1) # Dark Slate Gray
        bsdf.inputs['Roughness'].default_value = 0.9 # Fosco
    backdrop.data.materials.append(mat)

def create_premium_material():
    """Gera um material Ouro premium/Vidro Fosco para o nosso objeto."""
    mat = bpy.data.materials.new(name="Premium_Gold")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    
    if bsdf:
        # Configurações de Ouro Metálico Cinematográfico
        bsdf.inputs['Base Color'].default_value = (1.0, 0.766, 0.336, 1) # Ouro rico
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = 0.15 # Levemente reflexivo, mas não um espelho perfeito
    return mat

def create_product():
    """Cria o objeto principal (O nosso 'Produto') e o anima."""
    # Produto centralizado e com escala corrigida para o "Golden Ratio"
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=0.8, depth=2.5, location=(0, 0, 0))
    product = bpy.context.active_object
    product.name = "Produto_Principal"
    
    # Adicionamos um Bevel para as bordas brilharem melhor na luz
    bevel = product.modifiers.new(name="Bevel", type='BEVEL')
    bevel.segments = 5
    bevel.width = 0.05
    
    # Aplica o material Premium
    mat_gold = create_premium_material()
    product.data.materials.append(mat_gold)
    
    bpy.ops.object.shade_smooth()
    
    # ---> ANIMAÇÃO: 360 Graus <---
    # Keyframe no frame 1 (rotação Z = 0)
    product.rotation_euler[2] = 0
    product.keyframe_insert(data_path="rotation_euler", frame=1, index=2)
    
    # Keyframe no frame 150 (rotação Z = 360 graus / 2*Pi em radianos)
    product.rotation_euler[2] = math.radians(360)
    product.keyframe_insert(data_path="rotation_euler", frame=150, index=2)
    
    # Transição Linear (para giro constante como num display comercial)
    fcurves = product.animation_data.action.fcurves
    for curve in fcurves:
        for keyframe in curve.keyframe_points:
            keyframe.interpolation = 'LINEAR'

def setup_cinematic_lighting():
    """Configura a iluminação de 3 pontos para looks de luxo."""
    
    # 1. Key Light (Luz Principal) - Destaca o produto
    bpy.ops.object.light_add(type='AREA', radius=2, align='WORLD', location=(4, -3, 3))
    key_light = bpy.context.active_object
    key_light.name = "Light_Key"
    key_light.data.energy = 2000  # Watts - Muito mais forte para garantir luz em background
    key_light.data.color = (1.0, 0.9, 0.8) # Quente suave
    # Direcionar a luz para o centro (0,0,1)
    track_to = key_light.constraints.new(type='TRACK_TO')
    
    # Criamos um "Alvo vazio" no centro para as luzes mirarem sempre
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 1))
    target = bpy.context.active_object
    target.name = "Light_Target"
    track_to.target = target
    
    # 2. Fill Light (Luz de Preenchimento) - Suaviza as sombras
    bpy.ops.object.light_add(type='AREA', radius=3, align='WORLD', location=(-3, -4, 2))
    fill_light = bpy.context.active_object
    fill_light.name = "Light_Fill"
    fill_light.data.energy = 800
    fill_light.data.color = (0.8, 0.9, 1.0) # Azul Frio FGS
    track = fill_light.constraints.new(type='TRACK_TO')
    track.target = target
    
    # 3. Rim / Back Light (Luz de Recorte) - O mais importante, separa o modelo do fundo
    bpy.ops.object.light_add(type='AREA', radius=1.5, align='WORLD', location=(0, 4, 3))
    rim_light = bpy.context.active_object
    rim_light.name = "Light_Rim"
    rim_light.data.energy = 3000 # Super forte para o WOW factor nas bordas gold
    track2 = rim_light.constraints.new(type='TRACK_TO')
    track2.target = target

def setup_camera():
    """Adiciona a câmera cinematográfica com Profundidade de Campo e anima um micro-tracking."""
    # Afastamos um pouco mais para garantir que o topo não seja cortado
    bpy.ops.object.camera_add(location=(0, -10, 1.2))
    cam = bpy.context.active_object
    cam.name = "Camera_Principal"
    bpy.context.scene.camera = cam
    
    # Lente de Estúdio (85mm)
    cam.data.lens = 85
    
    # Depth of Field (DoF) para desfocar o fundo
    cam.data.dof.use_dof = True
    cam.data.dof.aperture_fstop = 2.8 # Desfoque cinemático
    
    # Focar no nosso produto principal
    product = bpy.data.objects.get("Produto_Principal")
    if product:
        cam.data.dof.focus_object = product
        
        # Apontar a câmera sempre para o produto
        track = cam.constraints.new(type='TRACK_TO')
        track.target = product
        track.track_axis = 'TRACK_NEGATIVE_Z'
        track.up_axis = 'UP_Y'
        
    # Animação suave de Zoom-In na Câmera (Fator Retenção de Audiência)
    cam.location[1] = -10 # Começa com enquadramento de segurança
    cam.keyframe_insert(data_path="location", frame=1, index=1)
    
    cam.location[1] = -8.5 # Zoom-in dramático constante
    cam.keyframe_insert(data_path="location", frame=150, index=1)

def main():
    print("\n[========================================================]")
    print("FGS Studio: Iniciando Arquitetura do 'Comercial 360'...")
    clean_scene()
    setup_render_settings()
    create_backdrop()
    create_product()
    setup_cinematic_lighting()
    setup_camera()
    
    # --- MÁGICA: FORÇAR VIEWPORT RENDERIZADO ---
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'
                    space.region_3d.view_perspective = 'CAMERA' # Já entra na visão da câmera
    
    print("FGS Studio: Cena configurada com sucesso!")
    print("FGS Studio: Iniciando Render Mágico em Background... Aguarde.")
    print("[========================================================]\n")
    
    # RENDER AUTÔNOMO (ATIVADO: ENTREGA FINAL)
    bpy.ops.render.render(animation=True)
    
    print("\n[========================================================]")
    print("FGS Studio: Cena Pronta! Salvando arquivo .blend para inspeção...")
    
    # Recalcula o diretório de saída para salvar o .blend
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    out_dir = os.path.join(base_dir, "renders", "finals")
    blend_file = os.path.join(out_dir, "inspecao_comercial_360.blend")
    
    bpy.ops.wm.save_as_mainfile(filepath=blend_file)
    print(f"Arquivo salvo em: {blend_file}")
    print("[========================================================]\n")

if __name__ == "__main__":
    main()
