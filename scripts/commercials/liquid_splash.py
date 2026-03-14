# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: liquid_splash.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import sys
import os
import math

# Adiciona o diretório 'utils' ao path temporalmente para importar nossas bibliotecas FGS
utils_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "utils"))
if utils_path not in sys.path:
    sys.path.append(utils_path)

# ==============================================================================
# FELIPE GOUVEIA STUDIO - PYTHON 3D
# Projeto: Comercial (Liquid Splash — MantaFlow)
# Versão: 1.0
# Descrição: Template de fluido MantaFlow. Objeto caindo em um recipiente
#            com água em câmera lenta e renderização PBR fina (Cycles recomendado).
# ==============================================================================

def build_commercial_splash():
    # Importar nossas bibliotecas modulares (Fase 1)
    import scene_setup as setup
    from materials_library import MaterialLibrary
    
    # 1. SETUP INICIAL DA CENA
    setup.limpar_cena()
    scene = setup.setup_scene_comercial()
    
    # 2. INSTANCIAR BIBLIOTECA DE MATERIAIS FGS
    lib = MaterialLibrary(prefixo="FGS_Lq")
    
    # 3. CRIAR OBJETOS DA SIMULAÇÃO (MantaFlow)
    
    # O Domínio (A caixa invisível onde o líquido pode existir)
    bpy.ops.mesh.primitive_cube_add(size=4, location=(0, 0, 2))
    domain = bpy.context.active_object
    domain.name = "Liquid_Domain"
    
    # Configurar Domínio MantaFlow
    bpy.ops.object.modifier_add(type='FLUID')
    domain.modifiers["Fluid"].fluid_type = 'DOMAIN'
    domain.modifiers["Fluid"].domain_settings.domain_type = 'LIQUID'
    domain.modifiers["Fluid"].domain_settings.resolution_max = 64 # Qualidade do líquido (Aumentar para final)
    domain.modifiers["Fluid"].domain_settings.use_mesh = True # Gera o mesh da água visível
    
    # Material da Água (da nossa lib PBR)
    mat_agua = lib.liquido(tipo="agua")
    lib.aplicar(domain, mat_agua)
    
    # O Flow (Objeto que vai "jorrar" ou "conter" líquido no início)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 3.2))
    flow = bpy.context.active_object
    flow.name = "Liquid_Flow"
    
    # Configurar Flow MantaFlow
    bpy.ops.object.modifier_add(type='FLUID')
    flow.modifiers["Fluid"].fluid_type = 'FLOW'
    flow.modifiers["Fluid"].flow_settings.flow_type = 'LIQUID'
    flow.modifiers["Fluid"].flow_settings.flow_behavior = 'GEOMETRY' # O líquido cai de uma vez
    
    # O Effector (Uma taça/copo invisível onde o líquido vai cair e bater)
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1.0))
    effector = bpy.context.active_object
    effector.name = "Liquid_Effector_Obstacle"
    
    # Entra no modo edição para apagar a tampa e fazer uma "caixa" vazando
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    effector.data.polygons[5].select = True # Face superior (assumindo Z-up padrão cubo)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Dar espessura "Solidify" para não vazar pela física
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    effector.modifiers["Solidify"].thickness = 0.1
    
    # Configurar Effector MantaFlow
    bpy.ops.object.modifier_add(type='FLUID')
    effector.modifiers["Fluid"].fluid_type = 'EFFECTOR'
    effector.modifiers["Fluid"].effector_settings.effector_type = 'COLLISION'
    
    # Material do Effector (Vidro premium da nossa lib)
    mat_vidro = lib.vidro()
    lib.aplicar(effector, mat_vidro)
    
    # 4. OBJETO DA QUEDA (Um diamante brilhante caindo na água)
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.3, subdivisions=2, location=(0, 0, 4.5))
    produto = bpy.context.active_object
    produto.name = "Drop_Product"
    
    # O objeto também colide com a água
    bpy.ops.object.modifier_add(type='FLUID')
    produto.modifiers["Fluid"].fluid_type = 'EFFECTOR'
    
    # Animar a queda do diamante via Keyframes (sem Rigid Body pesado para teste)
    produto.keyframe_insert(data_path="location", frame=1, index=2)
    produto.location[2] = 0.5 # Bate com fundona água
    produto.keyframe_insert(data_path="location", frame=25, index=2)
    
    mat_ouro = lib.metal_ouro()
    lib.aplicar(produto, mat_ouro)
    
    # 5. CENÁRIO, LUZ E CÂMERA (Usando Utils do FGS Studio)
    
    # Câmera cinematográfica mirando no vidro
    cam, alvo = setup.configurar_camera_padrao(posicao=(0, -6, 2.5), alvo=(0, 0, 1), fov_graus=60)
    
    # Iluminação 3 Pontos Clássica focada no objeto central
    luzes = setup.adicionar_iluminacao_3_pontos(posicao_centro=(0, 0, 1))
    
    # Chão de Fundo Estúdio Fosco Infinito
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, 0))
    chao = bpy.context.active_object
    chao.name = "FGS_Studio_Floor"
    mat_fundo = lib.fundo_studio()
    lib.aplicar(chao, mat_fundo)
    
    print("💧 FGS: Comercial 'Liquid Splash' gerado com sucesso!")
    print("👉 Passo próximo manual: Selecione o 'Liquid_Domain' e na aba 'Physics', clique em 'Bake Data' e depois 'Bake Mesh' para calcular a simulação de água antes de dar o Render (CTLR+F12).")

if __name__ == "__main__":
    build_commercial_splash()
