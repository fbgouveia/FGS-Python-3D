"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Módulo: scene_setup.py                                     ║
║   Versão: 1.0.0                                             ║
║   Descrição: Funções base para configurar qualquer cena      ║
║   Blender: 4.0+                                             ║
╚══════════════════════════════════════════════════════════════╝

COMO USAR:
  Este arquivo é um MÓDULO UTILITÁRIO — não execute diretamente.
  Importe suas funções no início dos outros scripts:
  
  Exemplo:
    exec(open("D:/Blender/blenderscripts/scripts/utils/scene_setup.py").read())
    setup_scene(fps=30, resolucao_x=1920, resolucao_y=1080)
"""

import bpy
import math
from mathutils import Vector


# ═══════════════════════════════════════════════════════════════
# PARÂMETROS PADRÃO — Modifique conforme necessário
# ═══════════════════════════════════════════════════════════════
FPS_PADRAO = 24                  # 24=cinema, 30=YouTube, 60=smooth
RESOLUCAO_X_PADRAO = 1920       # Largura em pixels
RESOLUCAO_Y_PADRAO = 1080       # Altura em pixels
DURACAO_SEGUNDOS_PADRAO = 10    # Duração padrão da animação


def limpar_cena():
    """
    Remove TODOS os objetos da cena atual.
    Essencial chamar antes de criar qualquer coisa nova.
    """
    # Selecionar todos os objetos
    bpy.ops.object.select_all(action='SELECT')
    # Deletar selecionados
    bpy.ops.object.delete(use_global=False)
    
    # Limpar dados órfãos (meshes, materiais, etc. sem uso)
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.lights:
        if block.users == 0:
            bpy.data.lights.remove(block)
    
    print("✅ Cena limpa com sucesso!")


def setup_scene(
    fps=FPS_PADRAO,
    resolucao_x=RESOLUCAO_X_PADRAO,
    resolucao_y=RESOLUCAO_Y_PADRAO,
    duracao_segundos=DURACAO_SEGUNDOS_PADRAO,
    cor_fundo=(0.05, 0.05, 0.05, 1.0)  # Quase preto por padrão
):
    """
    Configura a cena base — SEMPRE chamar primeiro em qualquer script.
    
    Parâmetros:
        fps: Frames por segundo (24=cinema, 30=YouTube, 60=smooth)
        resolucao_x: Largura em pixels (1920 para HD)
        resolucao_y: Altura em pixels (1080 para HD, 1920 para shorts verticais)
        duracao_segundos: Duração total da animação
        cor_fundo: Cor do background (R, G, B, A) entre 0.0 e 1.0
    
    Retorna:
        scene: Objeto de cena do Blender
    """
    scene = bpy.context.scene
    
    # --- Configurações de Render ---
    scene.render.fps = fps
    scene.render.resolution_x = resolucao_x
    scene.render.resolution_y = resolucao_y
    scene.render.resolution_percentage = 100
    
    # --- Frame Range ---
    scene.frame_start = 1
    scene.frame_end = fps * duracao_segundos
    scene.frame_current = 1
    
    # --- Unidades Métricas (padrão internacional) ---
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.length_unit = 'METERS'
    scene.unit_settings.scale_length = 1.0
    
    # --- Cor do fundo (World) ---
    if scene.world is None:
        scene.world = bpy.data.worlds.new("FGS_World")
    
    scene.world.use_nodes = True
    world_nodes = scene.world.node_tree.nodes
    world_links = scene.world.node_tree.links
    
    # Limpar nós do world
    world_nodes.clear()
    
    # Background simples com a cor escolhida
    background_node = world_nodes.new(type='ShaderNodeBackground')
    background_node.inputs['Color'].default_value = cor_fundo
    background_node.inputs['Strength'].default_value = 1.0
    
    output_node = world_nodes.new(type='ShaderNodeOutputWorld')
    world_links.new(background_node.outputs['Background'], output_node.inputs['Surface'])
    
    print(f"✅ Cena configurada: {resolucao_x}x{resolucao_y} @ {fps}fps | {duracao_segundos}s")
    return scene


def setup_scene_youtube():
    """Layout padrão para vídeos YouTube (paisagem HD)."""
    return setup_scene(fps=30, resolucao_x=1920, resolucao_y=1080, duracao_segundos=60)


def setup_scene_short():
    """Layout padrão para Shorts/Reels (vertical)."""
    return setup_scene(fps=30, resolucao_x=1080, resolucao_y=1920, duracao_segundos=30)


def setup_scene_comercial():
    """Layout padrão para comerciais (HD cinema)."""
    return setup_scene(fps=24, resolucao_x=1920, resolucao_y=1080, duracao_segundos=15)


def setup_scene_animatic():
    """Layout para animatic/aprovação (resolução menor para rapidez)."""
    return setup_scene(fps=24, resolucao_x=960, resolucao_y=540, duracao_segundos=30)


def adicionar_luz_sol(intensidade=3.0, angulo_graus=45, rotacao_graus=(45, 0, 45)):
    """
    Adiciona uma luz solar (direcional) na cena.
    
    Parâmetros:
        intensidade: Força da luz (1.0 = padrão, 3.0 = forte)
        angulo_graus: Ângulo do sol (simula tamanho da fonte)
        rotacao_graus: Direção da luz (X, Y, Z) em graus
    """
    import math
    
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sol = bpy.context.active_object
    sol.name = "FGS_Luz_Sol"
    
    luz = sol.data
    luz.energy = intensidade
    luz.angle = math.radians(angulo_graus)
    
    sol.rotation_euler = tuple(math.radians(a) for a in rotacao_graus)
    
    print(f"☀️ Luz solar adicionada com intensidade {intensidade}")
    return sol


def adicionar_luz_ambiente(intensidade=0.5):
    """
    Adiciona iluminação ambiente suave (simula luz do céu).
    
    Parâmetros:
        intensidade: Força da luz ambiente (0.1 a 1.0)
    """
    scene = bpy.context.scene
    world_nodes = scene.world.node_tree.nodes
    
    # Procurar node de background existente
    for node in world_nodes:
        if node.type == 'BACKGROUND':
            node.inputs['Strength'].default_value = intensidade
            print(f"🌤️ Luz ambiente configurada em {intensidade}")
            return
    
    print("⚠️ World não configurado. Chame setup_scene() primeiro.")


def adicionar_iluminacao_3_pontos(posicao_centro=(0, 0, 0)):
    """
    Adiciona setup clássico de iluminação de 3 pontos:
    - Key Light: Luz principal (mais forte)
    - Fill Light: Luz de preenchimento (mais suave)
    - Back Light: Contraluz (destaque de contorno)
    
    Ideal para comerciais e entrevistas.
    """
    cx, cy, cz = posicao_centro
    
    # Key Light (principal — frente-esquerda-acima)
    bpy.ops.object.light_add(type='AREA', location=(cx - 3, cy - 3, cz + 4))
    key = bpy.context.active_object
    key.name = "FGS_Key_Light"
    key.data.energy = 500
    key.data.size = 2.0
    key.rotation_euler = (math.radians(45), 0, math.radians(-45))
    
    # Fill Light (preenchimento — frente-direita, mais suave)
    bpy.ops.object.light_add(type='AREA', location=(cx + 4, cy - 2, cz + 2))
    fill = bpy.context.active_object
    fill.name = "FGS_Fill_Light"
    fill.data.energy = 150
    fill.data.size = 3.0
    fill.rotation_euler = (math.radians(30), 0, math.radians(45))
    
    # Back Light (contraluz — atrás-acima)
    bpy.ops.object.light_add(type='AREA', location=(cx, cy + 5, cz + 3))
    back = bpy.context.active_object
    back.name = "FGS_Back_Light"
    back.data.energy = 300
    back.data.size = 1.5
    back.rotation_euler = (math.radians(-60), 0, math.radians(180))
    
    print("💡 Iluminação 3 pontos criada: Key + Fill + Back Light")
    return {"key": key, "fill": fill, "back": back}


def configurar_camera_padrao(posicao=(0, -7, 2), alvo=(0, 0, 1), fov_graus=50):
    """
    Cria e configura a câmera principal da cena.
    
    Parâmetros:
        posicao: Posição XYZ da câmera
        alvo: Ponto para onde a câmera aponta (XYZ)
        fov_graus: Campo de visão em graus (50=humano, 24=telefoto, 90=grande angular)
    
    Retorna:
        camera: Objeto de câmera criado
    """
    # Criar câmera
    bpy.ops.object.camera_add(location=posicao)
    camera = bpy.context.active_object
    camera.name = "FGS_Camera_Principal"
    
    # Apontar câmera para o alvo usando Track To
    constraint = camera.constraints.new(type='TRACK_TO')
    
    # Criar objeto alvo vazio
    bpy.ops.object.empty_add(type='SPHERE', location=alvo)
    alvo_obj = bpy.context.active_object
    alvo_obj.name = "FGS_Camera_Alvo"
    alvo_obj.scale = (0.1, 0.1, 0.1)
    
    constraint.target = alvo_obj
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    
    # Configurar FOV
    camera.data.lens_unit = 'FOV'
    camera.data.angle = math.radians(fov_graus)
    
    # Ativar como câmera da cena
    bpy.context.scene.camera = camera
    
    print(f"📷 Câmera configurada: FOV={fov_graus}° | Posição={posicao}")
    return camera, alvo_obj


# ═══════════════════════════════════════════════════════════════
# EXECUÇÃO DIRETA (TESTE)
# Descomente o bloco abaixo para testar este módulo isolado
# ═══════════════════════════════════════════════════════════════
"""
if __name__ == "__main__" or True:
    limpar_cena()
    scene = setup_scene(fps=24, resolucao_x=1920, resolucao_y=1080, duracao_segundos=10)
    adicionar_iluminacao_3_pontos()
    camera, alvo = configurar_camera_padrao()
    print("✅ scene_setup.py executado com sucesso!")
"""
