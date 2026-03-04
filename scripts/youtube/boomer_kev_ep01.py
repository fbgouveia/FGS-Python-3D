"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Projeto: Boomer & Kev — Episódio 1: "Esse Negócio de IA" ║
║   Tipo: YouTube Short + Reel                                 ║
║   Duração: 30s | 24fps | 720 frames                         ║
║   Render: EEVEE Next | ~5 min com GPU                        ║
║   Output: /renders/boomer_kev_ep01.mp4                       ║
║                                                             ║
║   STORYTELLING:                                             ║
║   Hook: Estúdio acende, os dois aparecem (0-3s)             ║
║   Desenvolvimento: Debate sobre IA (3-22s)                  ║
║   Clímax: Os dois explodem de rir (22-27s)                  ║
║   Resolução: Encerramento com gancho (27-30s)               ║
║                                                             ║
║   PERSONAGENS: Boomer (Urso) + Kev (Raposa)                 ║
║   CENÁRIO: Podcast Studio "The Den"                         ║
╚══════════════════════════════════════════════════════════════╝

COMO USAR NO BLENDER:
  1. Abrir Blender → Aba "Scripting"
  2. Clicar em "New"
  3. Colar TODO este script
  4. Clicar em ▶ Run Script (ou Alt+P)
  5. Aguardar criação da cena (~30 segundos)
  6. Render → Render Animation (Ctrl+F12) para renderizar
  7. Arquivo salvo em: D:/Blender/blenderscripts/renders/drafts/
"""

import bpy
import math
import random
from mathutils import Vector, Euler


# ═══════════════════════════════════════════════════════════════
# PARÂMETROS AJUSTÁVEIS — Modifique aqui sem mexer no resto
# ═══════════════════════════════════════════════════════════════
OUTPUT_PATH = "D:/Blender/blenderscripts/renders/drafts/boomer_kev_ep01_"
FPS = 24
DURACAO_SEGUNDOS = 30
QUALIDADE_RENDER = "medium"   # "preview" | "medium" | "high"
RENDER_ENGINE = "EEVEE"       # "EEVEE" | "CYCLES"

# --- Cores dos Personagens ---
COR_BOOMER_CORPO = (0.45, 0.28, 0.15, 1.0)       # Marrom urso
COR_BOOMER_FOCINHO = (0.65, 0.45, 0.28, 1.0)     # Bege focinho
COR_KEV_CORPO = (0.85, 0.35, 0.08, 1.0)           # Laranja raposa
COR_KEV_FOCINHO = (0.95, 0.85, 0.75, 1.0)         # Creme focinho

# --- Cores do Estúdio ---
COR_PAREDE = (0.07, 0.05, 0.04, 1.0)              # Quase preto
COR_MESA = (0.25, 0.15, 0.08, 1.0)                # Madeira escura
COR_RING_LIGHT_BOOMER = (0.9, 0.85, 0.7, 1.0)    # Quente (Boomer)
COR_RING_LIGHT_KEV = (0.7, 0.85, 0.9, 1.0)       # Fria (Kev)
COR_SIGN_ON_AIR = (0.9, 0.05, 0.0, 1.0)           # Vermelho neon


# ═══════════════════════════════════════════════════════════════
# BLOCO 1: SETUP DA CENA
# ═══════════════════════════════════════════════════════════════

def setup_cena():
    """Inicializa e configura a cena base para o Boomer & Kev."""
    
    # Limpar cena existente
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Limpar dados órfãos
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    
    scene = bpy.context.scene
    
    # Configurações de render
    scene.render.fps = FPS
    scene.render.resolution_x = 1280       # 720p para draft rápido
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.frame_start = 1
    scene.frame_end = FPS * DURACAO_SEGUNDOS  # 720 frames
    scene.frame_current = 1
    
    # Unidades métricas
    scene.unit_settings.system = 'METRIC'
    scene.unit_settings.scale_length = 1.0
    
    # Background escuro (tom do estúdio)
    if not scene.world:
        scene.world = bpy.data.worlds.new("FGS_World")
    scene.world.use_nodes = True
    world_bg = scene.world.node_tree.nodes.get("Background")
    if world_bg:
        world_bg.inputs['Color'].default_value = (0.02, 0.02, 0.03, 1.0)
        world_bg.inputs['Strength'].default_value = 0.3
    
    print("✅ BLOCO 1: Cena configurada — 30s | 720 frames | 1280x720")
    return scene


# ═══════════════════════════════════════════════════════════════
# BLOCO 2: CRIAÇÃO DO MATERIAL (Função utilitária)
# ═══════════════════════════════════════════════════════════════

def criar_material(nome, cor, roughness=0.7, metallic=0.0, emission=None, emission_strength=0.0):
    """Cria um material PBR completo via nós."""
    
    # Reutilizar material se já existir
    if nome in bpy.data.materials:
        return bpy.data.materials[nome]
    
    mat = bpy.data.materials.new(name=nome)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = cor
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Metallic'].default_value = metallic
    
    if emission:
        bsdf.inputs['Emission Color'].default_value = emission
        bsdf.inputs['Emission Strength'].default_value = emission_strength
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat


def aplicar_material(obj, mat):
    """Aplica material a um objeto."""
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)


# ═══════════════════════════════════════════════════════════════
# BLOCO 3: CRIAÇÃO DO CENÁRIO — PODCAST STUDIO "THE DEN"
# ═══════════════════════════════════════════════════════════════

def criar_cenario():
    """Cria o estúdio de podcast completo."""
    
    objetos = {}
    
    # --- CHÃO ---
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
    chao = bpy.context.active_object
    chao.name = "Studio_Chao"
    mat_chao = criar_material("Mat_Chao", (0.06, 0.05, 0.04, 1.0), roughness=0.95)
    aplicar_material(chao, mat_chao)
    objetos['chao'] = chao
    
    # --- PAREDE DE FUNDO ---
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 2.5, 2.5))
    parede = bpy.context.active_object
    parede.name = "Studio_Parede"
    parede.rotation_euler = (math.radians(90), 0, 0)
    mat_parede = criar_material("Mat_Parede", COR_PAREDE, roughness=0.85)
    aplicar_material(parede, mat_parede)
    objetos['parede'] = parede
    
    # --- MESA PRINCIPAL ---
    bpy.ops.mesh.primitive_cube_add(location=(0, 0.5, 0.45))
    mesa = bpy.context.active_object
    mesa.name = "Studio_Mesa"
    mesa.scale = (2.2, 0.6, 0.05)
    bpy.ops.object.transform_apply(scale=True)
    mat_mesa = criar_material("Mat_Mesa", COR_MESA, roughness=0.6)
    aplicar_material(mesa, mat_mesa)
    objetos['mesa'] = mesa
    
    # Pés da mesa
    for x_pos in [-1.8, 1.8, -1.8, 1.8]:
        for y_pos, z_pos in [(-0.1, 0.22), (1.1, 0.22)]:
            break  # Simplificado para o draft
    
    # --- SIGN "ON AIR" ---
    bpy.ops.mesh.primitive_cube_add(location=(0, 2.3, 2.8))
    sign = bpy.context.active_object
    sign.name = "Studio_OnAir_Sign"
    sign.scale = (0.6, 0.05, 0.12)
    bpy.ops.object.transform_apply(scale=True)
    mat_sign = criar_material(
        "Mat_OnAir", 
        COR_SIGN_ON_AIR,
        emission=COR_SIGN_ON_AIR,
        emission_strength=5.0
    )
    aplicar_material(sign, mat_sign)
    objetos['sign_on_air'] = sign
    
    # --- MICROFONE BOOMER (esquerda) ---
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(-0.75, 0.2, 0.85))
    mic_boomer = bpy.context.active_object
    mic_boomer.name = "Mic_Boomer"
    mat_mic = criar_material("Mat_Microfone", (0.05, 0.05, 0.05, 1.0), roughness=0.3, metallic=0.7)
    aplicar_material(mic_boomer, mat_mic)
    
    # Braço do microfone
    bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.4, location=(-0.75, 0.2, 0.65))
    braco_mic_b = bpy.context.active_object
    braco_mic_b.name = "Mic_Boomer_Braco"
    aplicar_material(braco_mic_b, mat_mic)
    objetos['mic_boomer'] = mic_boomer
    
    # --- MICROFONE KEV (direita) ---
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(0.75, 0.2, 0.85))
    mic_kev = bpy.context.active_object
    mic_kev.name = "Mic_Kev"
    aplicar_material(mic_kev, mat_mic)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.01, depth=0.4, location=(0.75, 0.2, 0.65))
    braco_mic_k = bpy.context.active_object
    braco_mic_k.name = "Mic_Kev_Braco"
    aplicar_material(braco_mic_k, mat_mic)
    objetos['mic_kev'] = mic_kev
    
    print("✅ BLOCO 3: Cenário 'The Den' criado — mesa, paredes, microfones, sign ON AIR")
    return objetos


# ═══════════════════════════════════════════════════════════════
# BLOCO 4: PERSONAGEM BOOMER (Urso Estilizado)
# ═══════════════════════════════════════════════════════════════

def criar_boomer(posicao=(-1.0, 0.8, 0.5)):
    """
    Cria o personagem Boomer — Urso estilizado humanizado.
    Posição padrão: esquerda da mesa.
    """
    
    x, y, z = posicao
    objetos = {}
    
    mat_corpo = criar_material("Mat_Boomer_Corpo", COR_BOOMER_CORPO, roughness=0.8)
    mat_focinho = criar_material("Mat_Boomer_Focinho", COR_BOOMER_FOCINHO, roughness=0.75)
    mat_olho = criar_material("Mat_Olho_Escuro", (0.05, 0.02, 0.01, 1.0), roughness=0.1)
    mat_nariz = criar_material("Mat_Nariz", (0.08, 0.05, 0.04, 1.0), roughness=0.3)
    
    # --- CORPO (sentado, acima da mesa) ---
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.32, location=(x, y, z + 0.32))
    torso = bpy.context.active_object
    torso.name = "Boomer_Torso"
    torso.scale = (1.0, 0.75, 1.15)
    bpy.ops.object.transform_apply(scale=True)
    aplicar_material(torso, mat_corpo)
    objetos['torso'] = torso
    
    # --- CABEÇA ---
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28, location=(x, y, z + 0.95))
    cabeca = bpy.context.active_object
    cabeca.name = "Boomer_Cabeca"
    cabeca.scale = (1.0, 0.9, 1.05)
    bpy.ops.object.transform_apply(scale=True)
    aplicar_material(cabeca, mat_corpo)
    objetos['cabeca'] = cabeca
    
    # --- FOCINHO ---
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(x, y - 0.22, z + 0.88))
    focinho = bpy.context.active_object
    focinho.name = "Boomer_Focinho"
    focinho.scale = (1.0, 0.7, 0.65)
    bpy.ops.object.transform_apply(scale=True)
    aplicar_material(focinho, mat_focinho)
    objetos['focinho'] = focinho
    
    # --- NARIZ ---
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.04, location=(x, y - 0.32, z + 0.93))
    nariz = bpy.context.active_object
    nariz.name = "Boomer_Nariz"
    nariz.scale = (1.0, 0.6, 0.8)
    bpy.ops.object.transform_apply(scale=True)
    aplicar_material(nariz, mat_nariz)
    
    # --- OLHOS ---
    for dx, lado in [(-0.09, "Dir"), (0.09, "Esq")]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.055, location=(x + dx, y - 0.18, z + 1.01))
        olho = bpy.context.active_object
        olho.name = f"Boomer_Olho_{lado}"
        olho.scale = (1.0, 0.6, 1.0)
        bpy.ops.object.transform_apply(scale=True)
        aplicar_material(olho, mat_olho)
        
        # Brilho do olho
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.018, location=(x + dx - 0.02, y - 0.23, z + 1.04))
        brilho = bpy.context.active_object
        brilho.name = f"Boomer_Olho_Brilho_{lado}"
        mat_brilho = criar_material("Mat_Brilho_Olho", (1.0, 1.0, 1.0, 1.0), roughness=0.0)
        aplicar_material(brilho, mat_brilho)
    
    # --- ORELHAS ---
    for dx, lado in [(-0.26, "Esq"), (0.26, "Dir")]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(x + dx, y, z + 1.15))
        orelha = bpy.context.active_object
        orelha.name = f"Boomer_Orelha_{lado}"
        orelha.scale = (0.75, 0.55, 1.0)
        bpy.ops.object.transform_apply(scale=True)
        aplicar_material(orelha, mat_corpo)
    
    # --- BRAÇOS (posição podcast — cotovelos na mesa) ---
    for dx, lado in [(-0.28, "Esq"), (0.28, "Dir")]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.14, location=(x + dx, y + 0.1, z + 0.45))
        braco = bpy.context.active_object
        braco.name = f"Boomer_Braco_{lado}"
        braco.scale = (0.65, 1.4, 0.55)
        bpy.ops.object.transform_apply(scale=True)
        aplicar_material(braco, mat_corpo)
    
    print("✅ BLOCO 4: Boomer criado — urso marrom, posição podcast esquerda")
    return objetos


# ═══════════════════════════════════════════════════════════════
# BLOCO 5: PERSONAGEM KEV (Raposa Estilizada)
# ═══════════════════════════════════════════════════════════════

def criar_kev(posicao=(1.0, 0.8, 0.5)):
    """
    Cria o personagem Kev — Raposa estilizada humanizada.
    Posição padrão: direita da mesa.
    """
    
    x, y, z = posicao
    objetos = {}
    
    mat_corpo = criar_material("Mat_Kev_Corpo", COR_KEV_CORPO, roughness=0.75)
    mat_focinho = criar_material("Mat_Kev_Focinho", COR_KEV_FOCINHO, roughness=0.7)
    mat_olho = criar_material("Mat_Olho_Verde", (0.05, 0.4, 0.1, 1.0), roughness=0.1)
    mat_nariz = criar_material("Mat_Nariz_Kev", (0.06, 0.04, 0.03, 1.0), roughness=0.3)
    mat_ponta_orelha = criar_material("Mat_Ponta_Orelha", (0.03, 0.03, 0.03, 1.0), roughness=0.7)
    
    # --- CORPO (mais esbelto que Boomer) ---
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.26, location=(x, y, z + 0.26))
    torso = bpy.context.active_object
    torso.name = "Kev_Torso"
    torso.scale = (0.85, 0.65, 1.2)
    bpy.ops.object.transform_apply(scale=True)
    aplicar_material(torso, mat_corpo)
    objetos['torso'] = torso
    
    # --- CABEÇA (mais triangular/raposa) ---
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.24, location=(x, y, z + 0.86))
    cabeca = bpy.context.active_object
    cabeca.name = "Kev_Cabeca"
    cabeca.scale = (0.92, 0.85, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    aplicar_material(cabeca, mat_corpo)
    objetos['cabeca'] = cabeca
    
    # --- FOCINHO ALONGADO (característico de raposa) ---
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.13, location=(x, y - 0.25, z + 0.78))
    focinho = bpy.context.active_object
    focinho.name = "Kev_Focinho"
    focinho.scale = (0.75, 1.1, 0.55)  # Mais alongado na frente
    bpy.ops.object.transform_apply(scale=True)
    aplicar_material(focinho, mat_focinho)
    objetos['focinho'] = focinho
    
    # --- NARIZ ---
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(x, y - 0.35, z + 0.83))
    nariz = bpy.context.active_object
    nariz.name = "Kev_Nariz"
    nariz.scale = (1.0, 0.5, 0.7)
    bpy.ops.object.transform_apply(scale=True)
    aplicar_material(nariz, mat_nariz)
    
    # --- OLHOS (amendoados) ---
    for dx, lado in [(-0.08, "Dir"), (0.08, "Esq")]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.048, location=(x + dx, y - 0.17, z + 0.94))
        olho = bpy.context.active_object
        olho.name = f"Kev_Olho_{lado}"
        olho.scale = (1.1, 0.55, 0.85)  # Amendoado
        bpy.ops.object.transform_apply(scale=True)
        aplicar_material(olho, mat_olho)
        
        # Brilho
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.015, location=(x + dx - 0.015, y - 0.22, z + 0.96))
        brilho = bpy.context.active_object
        brilho.name = f"Kev_Olho_Brilho_{lado}"
        aplicar_material(brilho, criar_material("Mat_Brilho_Kev", (1.0, 1.0, 1.0, 1.0), roughness=0.0))
    
    # --- ORELHAS PONTUDAS (característico de raposa) ---
    for dx, lado in [(-0.22, "Esq"), (0.22, "Dir")]:
        bpy.ops.mesh.primitive_cone_add(radius1=0.1, depth=0.25, location=(x + dx, y, z + 1.08))
        orelha = bpy.context.active_object
        orelha.name = f"Kev_Orelha_{lado}"
        aplicar_material(orelha, mat_corpo)
        
        # Ponta preta das orelhas
        bpy.ops.mesh.primitive_cone_add(radius1=0.04, depth=0.08, location=(x + dx, y, z + 1.2))
        ponta = bpy.context.active_object
        ponta.name = f"Kev_Orelha_Ponta_{lado}"
        aplicar_material(ponta, mat_ponta_orelha)
    
    # --- BRAÇOS (gestuais, inclinados para frente) ---
    for dx, lado in [(-0.24, "Esq"), (0.24, "Dir")]:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.11, location=(x + dx, y + 0.05, z + 0.38))
        braco = bpy.context.active_object
        braco.name = f"Kev_Braco_{lado}"
        braco.scale = (0.6, 1.3, 0.5)
        bpy.ops.object.transform_apply(scale=True)
        aplicar_material(braco, mat_corpo)
    
    print("✅ BLOCO 5: Kev criado — raposa laranja, posição podcast direita")
    return objetos


# ═══════════════════════════════════════════════════════════════
# BLOCO 6: ILUMINAÇÃO DO ESTÚDIO
# ═══════════════════════════════════════════════════════════════

def criar_iluminacao():
    """
    Cria a iluminação do Podcast Studio The Den.
    Ring lights + luz de preenchimento + destaque no sign ON AIR.
    """
    
    # --- RING LIGHT BOOMER (quente — lado esquerdo) ---
    bpy.ops.object.light_add(type='AREA', location=(-1.0, 2.2, 1.5))
    ring_boomer = bpy.context.active_object
    ring_boomer.name = "RingLight_Boomer"
    ring_boomer.data.energy = 60
    ring_boomer.data.color = (0.9, 0.85, 0.7)
    ring_boomer.data.size = 0.8
    ring_boomer.rotation_euler = (math.radians(-25), 0, 0)
    
    # --- RING LIGHT KEV (fria — lado direito) ---
    bpy.ops.object.light_add(type='AREA', location=(1.0, 2.2, 1.5))
    ring_kev = bpy.context.active_object
    ring_kev.name = "RingLight_Kev"
    ring_kev.data.energy = 60
    ring_kev.data.color = (0.7, 0.85, 0.9)
    ring_kev.data.size = 0.8
    ring_kev.rotation_euler = (math.radians(-25), 0, 0)
    
    # --- LUZ DE PREENCHIMENTO GERAL ---
    bpy.ops.object.light_add(type='AREA', location=(0, -4, 3.5))
    fill = bpy.context.active_object
    fill.name = "Fill_Light"
    fill.data.energy = 15
    fill.data.color = (0.85, 0.88, 1.0)
    fill.data.size = 4.0
    fill.rotation_euler = (math.radians(50), 0, 0)
    
    # --- LUZ DE FUNDO / MOOD AZUL ---
    bpy.ops.object.light_add(type='AREA', location=(0, 2.8, 1.0))
    mood = bpy.context.active_object
    mood.name = "Mood_Light_BG"
    mood.data.energy = 8
    mood.data.color = (0.1, 0.25, 0.8)
    mood.data.size = 5.0
    mood.rotation_euler = (math.radians(-80), 0, 0)
    
    # --- DESTAQUE NO SIGN ON AIR ---
    bpy.ops.object.light_add(type='POINT', location=(0, 2.0, 2.8))
    sign_light = bpy.context.active_object
    sign_light.name = "OnAir_Sign_Light"
    sign_light.data.energy = 5
    sign_light.data.color = (1.0, 0.1, 0.0)
    sign_light.data.shadow_soft_size = 0.1
    
    print("✅ BLOCO 6: Iluminação criada — Ring Lights (quente+fria) + Mood azul + ON AIR")


# ═══════════════════════════════════════════════════════════════
# BLOCO 7: ANIMAÇÃO DAS CENAS (Shot List Implementation)
# ═══════════════════════════════════════════════════════════════

def criar_cameras_e_animacao():
    """
    Cria todas as câmeras do episódio e define animação básica.
    Baseado na Shot List do Episódio 1.
    """
    
    scene = bpy.context.scene
    cameras = {}
    
    # --- FUNÇÃO AUXILIAR: Criar câmera com animação ---
    def add_camera(nome, posicao, alvo, fov=50, use_dof=True, foco_dist=2.0):
        bpy.ops.object.camera_add(location=posicao)
        cam = bpy.context.active_object
        cam.name = nome
        cam.data.lens_unit = 'FOV'
        cam.data.angle = math.radians(fov)
        cam.data.dof.use_dof = use_dof
        cam.data.dof.focus_distance = foco_dist
        cam.data.dof.aperture_fstop = 2.8
        
        # Track To para o alvo
        constraint = cam.constraints.new(type='TRACK_TO')
        bpy.ops.object.empty_add(type='SPHERE', location=alvo)
        alvo_obj = bpy.context.active_object
        alvo_obj.name = f"{nome}_Alvo"
        alvo_obj.scale = (0.05, 0.05, 0.05)
        constraint.target = alvo_obj
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'
        
        return cam, alvo_obj
    
    # --- CÂMERAS (conforme shot list) ---
    
    # CAM 1: Wide Shot (Establishing) — Cenas 1, 9, 11
    cam_ws, _ = add_camera("CAM_WS", (0, -5.5, 1.8), (0, 0, 1.2), fov=62, foco_dist=5.5)
    
    # CAM 2: MCU Boomer — Cenas 2, 5, 8
    cam_mcu_boomer, _ = add_camera("CAM_MCU_Boomer", (-1.8, -2.0, 1.75), (-0.9, 0, 1.55), fov=38, foco_dist=2.2)
    
    # CAM 3: MCU Kev — Cenas 3, 7, 10
    cam_mcu_kev, _ = add_camera("CAM_MCU_Kev", (1.8, -2.0, 1.75), (0.9, 0, 1.55), fov=38, foco_dist=2.2)
    
    # CAM 4: OTS Boomer (Kev falando) — Cena 4
    cam_ots_boomer, _ = add_camera("CAM_OTS_Boomer", (-1.6, -3.2, 1.85), (1.0, 0, 1.5), fov=44, foco_dist=2.8)
    
    # CAM 5: OTS Kev (Boomer falando) — Cena 6
    cam_ots_kev, _ = add_camera("CAM_OTS_Kev", (1.6, -3.2, 1.85), (-1.0, 0, 1.5), fov=44, foco_dist=2.8)
    
    # CAM 6: Cutaway (mesa/microfone/objeto) — Cena 7
    cam_cutaway, _ = add_camera("CAM_Cutaway", (0.3, -0.8, 0.65), (0, 0.3, 0.5), fov=42, foco_dist=1.0)
    
    cameras = {
        'ws': cam_ws,
        'mcu_boomer': cam_mcu_boomer,
        'mcu_kev': cam_mcu_kev,
        'ots_boomer': cam_ots_boomer,
        'ots_kev': cam_ots_kev,
        'cutaway': cam_cutaway
    }
    
    # --- ANIMATION MARKERS (troca de câmeras = cortes) ---
    # Estrutura: [frame_inicio, câmera_ativa]
    shot_list = [
        (1,   cam_ws),          # Cena 01: WS Establishing (0-3s)
        (73,  cam_mcu_boomer),  # Cena 02: MCU Boomer fala (3-6s)
        (145, cam_mcu_kev),     # Cena 03: REACT Kev (6-8s)
        (193, cam_ots_boomer),  # Cena 04: OTS Kev falando (8-12s)
        (289, cam_mcu_boomer),  # Cena 05: MCU Boomer cético (12-15s)
        (361, cam_ots_kev),     # Cena 06: OTS Boomer fala (15-18s)
        (433, cam_cutaway),     # Cena 07: Cutaway cômico (18-20s)
        (481, cam_mcu_boomer),  # Cena 08: ECU Boomer ri (20-22s)
        (529, cam_ws),          # Cena 09: WS ambos rindo (22-25s)
        (601, cam_mcu_kev),     # Cena 10: MCU Kev encerra (25-27s)
        (649, cam_ws),          # Cena 11: WS Outro/Encerramento (27-30s)
    ]
    
    # Criar markers para cada corte
    for frame, cam in shot_list:
        marker = scene.timeline_markers.new(f"Corte_F{frame}", frame=frame)
        marker.camera = cam
    
    # Ativar câmera inicial
    scene.camera = cam_ws
    
    print(f"✅ BLOCO 7: {len(cameras)} câmeras criadas | {len(shot_list)} cortes marcados na timeline")
    return cameras


# ═══════════════════════════════════════════════════════════════
# BLOCO 8: ANIMAÇÃO DOS PERSONAGENS (Movimentos básicos)
# ═══════════════════════════════════════════════════════════════

def animar_personagens():
    """
    Anima os personagens com movimentos expressivos básicos.
    Keyframes para head bobbing, inclinações e expressões.
    """
    
    # Animação de "head bob" (respiração/fala) para personagens
    def head_bob(obj_name, frame_start, frame_end, amplitude=0.03, frequencia=8):
        """Cria animação de balanço suave de cabeça (simula fala)."""
        obj = bpy.data.objects.get(obj_name)
        if not obj:
            return
        
        pos_base = obj.location.z
        
        for frame in range(frame_start, frame_end, frequencia):
            bpy.context.scene.frame_set(frame)
            obj.location.z = pos_base
            obj.keyframe_insert(data_path="location", index=2)
            
            bpy.context.scene.frame_set(frame + frequencia // 2)
            obj.location.z = pos_base + amplitude
            obj.keyframe_insert(data_path="location", index=2)
        
        # Suavizar interpolação
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                for kp in fcurve.keyframe_points:
                    kp.interpolation = 'SINE'
    
    # Boomer tem head bob quando "fala" (cenas 2, 5, 6)
    head_bob("Boomer_Cabeca", 73, 216, amplitude=0.025, frequencia=10)   # Cenas 2-3
    head_bob("Boomer_Cabeca", 289, 432, amplitude=0.03, frequencia=8)    # Cenas 5-6
    
    # Kev é mais agitado — head bob mais rápido
    head_bob("Kev_Cabeca", 193, 288, amplitude=0.04, frequencia=6)       # Cena 4
    head_bob("Kev_Cabeca", 601, 648, amplitude=0.035, frequencia=7)      # Cena 10
    
    # --- Animação de inclinação do Boomer (césptico na cena 5) ---
    boomer_torso = bpy.data.objects.get("Boomer_Torso")
    if boomer_torso:
        # Frame 289 (12s) — inclinado para trás, césptico
        bpy.context.scene.frame_set(289)
        boomer_torso.rotation_euler = (0, math.radians(-8), 0)
        boomer_torso.keyframe_insert(data_path="rotation_euler")
        
        # Frame 360 — volta posição normal
        bpy.context.scene.frame_set(360)
        boomer_torso.rotation_euler = (0, 0, 0)
        boomer_torso.keyframe_insert(data_path="rotation_euler")
    
    # --- Animação de risada (cena 8-9: frames 481-600) ---
    boomer_cabeca = bpy.data.objects.get("Boomer_Cabeca")
    if boomer_cabeca:
        for frame in range(481, 600, 5):
            bpy.context.scene.frame_set(frame)
            oscilacao = math.sin((frame - 481) * 0.5) * 0.07
            boomer_cabeca.location.z = boomer_cabeca.location.z + oscilacao
            boomer_cabeca.keyframe_insert(data_path="location", index=2)
    
    print("✅ BLOCO 8: Animação aplicada — head bobs, inclinações, risada")


# ═══════════════════════════════════════════════════════════════
# BLOCO 9: CONFIGURAÇÃO DO RENDER
# ═══════════════════════════════════════════════════════════════

def configurar_render():
    """
    Configura o render otimizado para o draft do episódio.
    EEVEE next com qualidade média para aprovação rápida.
    """
    
    scene = bpy.context.scene
    
    if RENDER_ENGINE == "EEVEE":
        scene.render.engine = 'BLENDER_EEVEE_NEXT'
        
        eevee = scene.eevee
        samples_map = {"preview": 16, "medium": 64, "high": 128}
        eevee.taa_render_samples = samples_map.get(QUALIDADE_RENDER, 64)
        eevee.use_bloom = True
        eevee.bloom_intensity = 0.05
        eevee.bloom_threshold = 0.8
        eevee.use_ssr = True
        eevee.use_gtao = True
        eevee.gtao_quality = 0.25
        
    else:  # CYCLES
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 128
        scene.cycles.use_denoising = True
        scene.cycles.denoiser = 'OPTIX'
        
        # Tentar ativar GPU
        try:
            prefs = bpy.context.preferences
            cycles_prefs = prefs.addons['cycles'].preferences
            cycles_prefs.compute_device_type = 'OPTIX'
            for device in cycles_prefs.devices:
                device.use = True
            scene.cycles.device = 'GPU'
        except:
            print("⚠️ GPU não configurado — usando CPU")
    
    # Formato de output
    scene.render.filepath = OUTPUT_PATH
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
    
    print(f"✅ BLOCO 9: Render configurado — {RENDER_ENGINE} {QUALIDADE_RENDER} | Output: {OUTPUT_PATH}")


# ═══════════════════════════════════════════════════════════════
# EXECUÇÃO PRINCIPAL
# Execute este script no Blender → tudo será criado automaticamente
# ═══════════════════════════════════════════════════════════════

def main():
    print("\n" + "="*60)
    print("  FELIPE GOUVEIA STUDIO — BOOMER & KEV EP.01")
    print("  Iniciando criação da cena...")
    print("="*60 + "\n")
    
    # 1. Setup
    setup_cena()
    
    # 2. Cenário
    criar_cenario()
    
    # 3. Personagens
    criar_boomer(posicao=(-1.0, 0.8, 0.5))
    criar_kev(posicao=(1.0, 0.8, 0.5))
    
    # 4. Iluminação
    criar_iluminacao()
    
    # 5. Câmeras e cortes
    criar_cameras_e_animacao()
    
    # 6. Animação
    animar_personagens()
    
    # 7. Render
    configurar_render()
    
    print("\n" + "="*60)
    print("  ✅ CENA CRIADA COM SUCESSO!")
    print("")
    print("  PRÓXIMOS PASSOS:")
    print("  1. Pressione Numpad 0 → Ver pela câmera principal")
    print("  2. Pressione F12 → Render de um frame para testar")
    print("  3. Pressione Ctrl+F12 → Render da animação completa")
    print(f"  4. Output salvo em: {OUTPUT_PATH}")
    print("")
    print("  CORTES DE CÂMERA: Visíveis na Timeline")
    print("  (Play a animação para ver os cortes automáticos)")
    print("="*60 + "\n")


# Executar
main()
