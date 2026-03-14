# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: animation_engine.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: animation_engine.py                               ║
║   Função: Motor Universal de Animação e Movimento           ║
║           Keyframes, IK, procedural, mocap (BVH) e físicas  ║
╚══════════════════════════════════════════════════════════════╝

USO:
  import sys
  sys.path.append("D:/Blender/blenderscripts/scripts/utils")
  from animation_engine import AnimationEngine

  anim = AnimationEngine(fps=24)

  # Movimento Básico (Transição Suave):
  anim.mover(objeto, inicio=(0,0,0), fim=(5,0,0), frames=(1, 48))
  anim.rotacionar(objeto, inicio=(0,0,0), fim=(0,0,90), frames=(1, 48))
  anim.escalar(objeto, inicio=1.0, fim=2.5, frames=(1, 24))

  # Animação Procedural (Sem dependência de keyframes estáticos):
  anim.flutuar(objeto, amplitude=0.5, velocidade=1.0)
  anim.tremer(objeto, intensidade=0.1)
  anim.respiracao(objeto, amplitude_escala=0.02) # Para focar em personagens

  # Animação Baseada em Física:
  anim.cair_kikando(objeto, altura_inicial=5.0, quiques=3)

  # [Futuro] Captura de Movimento:
  # anim.carregar_bvh(armature, "caminho/para/animacao.bvh")
"""

import bpy
import math
import random
from mathutils import Vector, Euler

class AnimationEngine:
    """
    Motor Universal de Animação do FGS Python 3D.
    
    Cria movimentos fluidos, animações procedurais contínuas
    e gerencia físicas simples sem precisar lidar diretamente 
    com o sistema complexo de fcurves do Blender o tempo todo.
    """

    def __init__(self, fps=24):
        self.fps = fps
        self.scene = bpy.context.scene
        if self.scene.render.fps != fps:
            self.scene.render.fps = fps

    # ─────────────────────────────────────────────────────────────
    # MOVIMENTOS BÁSICOS (Keyframes)
    # ─────────────────────────────────────────────────────────────

    def mover(self, obj: bpy.types.Object,
              inicio: tuple, fim: tuple,
              frames: tuple = (1, 60),
              suave: bool = True):
        """Move um objeto do ponto A ao ponto B."""
        if not obj: return

        self.scene.frame_set(frames[0])
        obj.location = inicio
        obj.keyframe_insert(data_path="location")

        self.scene.frame_set(frames[1])
        obj.location = fim
        obj.keyframe_insert(data_path="location")

        if suave:
            self._suavizar(obj, "location")
        print(f"   🏃 Mover: {obj.name} de {inicio} para {fim}")

    def rotacionar(self, obj: bpy.types.Object,
                   inicio_graus: tuple, fim_graus: tuple,
                   frames: tuple = (1, 60),
                   suave: bool = True):
        """Rotaciona um objeto num espaço de tempo (em graus)."""
        if not obj: return

        r_ini = tuple(math.radians(g) for g in inicio_graus)
        r_fim = tuple(math.radians(g) for g in fim_graus)

        self.scene.frame_set(frames[0])
        obj.rotation_euler = r_ini
        obj.keyframe_insert(data_path="rotation_euler")

        self.scene.frame_set(frames[1])
        obj.rotation_euler = r_fim
        obj.keyframe_insert(data_path="rotation_euler")

        if suave:
            self._suavizar(obj, "rotation_euler")

    def escalar(self, obj: bpy.types.Object,
                inicio: float, fim: float,
                frames: tuple = (1, 24),
                suave: bool = True,
                bounce: bool = False):
        """Aumenta ou diminui o tamanho do objeto."""
        if not obj: return

        self.scene.frame_set(frames[0])
        obj.scale = (inicio, inicio, inicio)
        obj.keyframe_insert(data_path="scale")

        if bounce:
            # Pop-up cartoon (passa do tamanho final antes de assentar)
            meio = frames[0] + int((frames[1] - frames[0]) * 0.7)
            self.scene.frame_set(meio)
            obj.scale = (fim * 1.2, fim * 1.2, fim * 1.2)
            obj.keyframe_insert(data_path="scale")

        self.scene.frame_set(frames[1])
        obj.scale = (fim, fim, fim)
        obj.keyframe_insert(data_path="scale")

        if suave:
            self._suavizar(obj, "scale")

    def virar_para(self, obj: bpy.types.Object, alvo,
                   frame: int = 1):
        """Faz o objeto A rotacionar instantaneamente apontando para o objeto/coord B."""
        if not obj: return
        
        pos_b = alvo if isinstance(alvo, tuple) else alvo.location
        pos_a = obj.location
        
        direcao = Vector(pos_b) - Vector(pos_a)
        rot_quat = direcao.to_track_quat('-Y', 'Z')
        
        self.scene.frame_set(frame)
        obj.rotation_euler = rot_quat.to_euler()
        obj.keyframe_insert(data_path="rotation_euler")

    def orbitar(self, obj: bpy.types.Object, alvo: tuple, raio: float, 
                altura: float, frame_inicio=1, frame_fim=240, voltas=1.0):
        """Faz a câmera ou objeto orbitar um ponto fixo."""
        if not obj: return
        
        for f in range(frame_inicio, frame_fim + 1, 10):
            self.scene.frame_set(f)
            t = (f - frame_inicio) / (frame_fim - frame_inicio)
            angulo = t * math.pi * 2 * voltas
            
            obj.location.x = alvo[0] + math.cos(angulo) * raio
            obj.location.y = alvo[1] + math.sin(angulo) * raio
            obj.location.z = alvo[2] + altura
            
            obj.keyframe_insert(data_path="location")
            
            # Olhar para o alvo
            self.virar_para(obj, alvo, frame=f)
            
        print(f"   🎡 Orbita: {obj.name} ao redor de {alvo}")

    # ─────────────────────────────────────────────────────────────
    # ANIMAÇÃO PROCEDURAL (Modificadores FCurve)
    # ─────────────────────────────────────────────────────────────
    # Estes métodos adicionam modificadores curvos para gerar animação
    # contínua (loop infinito) sem criar milhares de keyframes.

    def flutuar(self, obj: bpy.types.Object,
                amplitude: float = 0.2, velocidade: float = 1.0,
                eixo: int = 2): # Z = 2
        """Faz o objeto flutuar para cima e para baixo infinitamente."""
        if not obj: return
        
        # Garante que pelo menos um keyframe exista para poder aplicar o modificador
        self.scene.frame_set(1)
        obj.keyframe_insert(data_path="location", index=eixo)
        
        action = obj.animation_data.action
        fcurve = None
        for fc in action.fcurves:
            if fc.data_path == "location" and fc.array_index == eixo:
                fcurve = fc
                break
                
        if fcurve:
            mod = fcurve.modifiers.new(type='FNGENERATOR')
            mod.function_type = 'SIN'
            mod.amplitude = amplitude
            mod.phase_multiplier = velocidade / 10.0
            mod.phase_offset = random.uniform(0, 10)  # Offset aleatório para objetos não flutuarem iguais
            
            # Adiciona o valor base (location atual)
            loc = obj.location[eixo]
            mod.value_offset = loc

    def tremer(self, obj: bpy.types.Object,
               intensidade: float = 0.1,
               eixos: tuple = (0, 1, 2)): # X, Y, Z
        """Aplica um modificador de Noise para simular tremor/câmera na mão/frio."""
        if not obj: return
        
        self.scene.frame_set(1)
        
        for eixo in eixos:
            obj.keyframe_insert(data_path="location", index=eixo)
            action = obj.animation_data.action
            
            for fc in action.fcurves:
                if fc.data_path == "location" and fc.array_index == eixo:
                    # Checa se já tem noise
                    has_noise = any(m.type == 'NOISE' for m in fc.modifiers)
                    if not has_noise:
                        mod = fcurve = fc.modifiers.new(type='NOISE')
                        mod.scale = 5.0
                        mod.strength = intensidade
                        mod.phase = random.uniform(0, 100)

    def respiracao(self, obj: bpy.types.Object,
                   amplitude_escala: float = 0.03,
                   velocidade: float = 0.5):
        """Escala sutilmente o eixo Z e Y (tórax) para simular respiração."""
        if not obj: return
        
        self.scene.frame_set(1)
        obj.keyframe_insert(data_path="scale", index=1) # Y Profundidade
        obj.keyframe_insert(data_path="scale", index=2) # Z Altura
        
        action = obj.animation_data.action
        
        for fc in action.fcurves:
            if fc.data_path == "scale" and fc.array_index in [1, 2]:
                mod = fc.modifiers.new(type='FNGENERATOR')
                mod.function_type = 'SIN'
                mod.amplitude = amplitude_escala
                mod.phase_multiplier = velocidade / 10.0
                mod.phase_offset = random.uniform(0, 10)
                mod.value_offset = obj.scale[fc.array_index]

    def caminhar_procedural(self, obj: bpy.types.Object, 
                            velocidade=1.0, amplitude=0.08):
        """Simula um balanço de caminhada (bobbing + tilt lateral)."""
        if not obj: return
        
        # Flutuar sutil em Z (o passo)
        self.flutuar(obj, amplitude=amplitude, velocidade=velocidade * 2, eixo=2)
        
        # Balanço em X (distribuição de peso)
        self.scene.frame_set(1)
        obj.keyframe_insert(data_path="location", index=0)
        action = obj.animation_data.action
        for fc in action.fcurves:
            if fc.data_path == "location" and fc.array_index == 0:
                mod = fc.modifiers.new(type='FNGENERATOR')
                mod.function_type = 'SIN'
                mod.amplitude = amplitude * 0.5
                mod.phase_multiplier = velocidade / 10.0
                mod.value_offset = obj.location.x
                
        print(f"   🚶 Caminhada Procedural: {obj.name}")

    # ─────────────────────────────────────────────────────────────
    # FÍSICAS SIMPLIFICADAS
    # ─────────────────────────────────────────────────────────────

    def cair_kikando(self, obj: bpy.types.Object,
                     altura_inicial: float = 5.0,
                     chao_z: float = 0.0,
                     frame_inicio: int = 1,
                     quiques: int = 3,
                     tamanho_queda: int = 15):
        """Simula a gravidade e o bounce de um objeto elástico ou rígido."""
        if not obj: return
        
        z = altura_inicial
        frame = frame_inicio
        amortecimento = 0.5
        passo = tamanho_queda
        
        # Posição inicial (Lá no alto)
        self.scene.frame_set(frame)
        obj.location.z = z
        obj.keyframe_insert(data_path="location", index=2)
        
        # Quiques
        for i in range(quiques):
            # Toca o chão
            frame += passo
            self.scene.frame_set(frame)
            obj.location.z = chao_z
            obj.keyframe_insert(data_path="location", index=2)
            
            # Quica para cima
            passo = int(passo * 0.8) # Fica mais rápido a cada quique
            if passo < 2: passo = 2
            
            frame += passo
            z = (z - chao_z) * amortecimento + chao_z
            self.scene.frame_set(frame)
            obj.location.z = z
            obj.keyframe_insert(data_path="location", index=2)
            
        # Repouso
        frame += passo
        self.scene.frame_set(frame)
        obj.location.z = chao_z
        obj.keyframe_insert(data_path="location", index=2)
        
        # Ajuste de interpolação curva para gravidade
        if obj.animation_data and obj.animation_data.action:
            for fc in obj.animation_data.action.fcurves:
                if fc.data_path == "location" and fc.array_index == 2:
                    for i, kp in enumerate(fc.keyframe_points):
                        # Ponto alto: ease in-out
                        if i == 0 or i == len(fc.keyframe_points)-1 or kp.co[1] > chao_z:
                            kp.interpolation = 'BEZIER'
                            kp.easing = 'AUTO'
                        # Batida no chão: linear/bounce
                        else:
                            kp.interpolation = 'BEZIER'
                            kp.handle_left_type = 'VECTOR'
                            kp.handle_right_type = 'VECTOR'


    # ─────────────────────────────────────────────────────────────
    # UTILITÁRIOS INTERNOS
    # ─────────────────────────────────────────────────────────────

    def _suavizar(self, obj, data_path: str):
        """Converte a interpolação dos keyframes para BEZIER (Suave)."""
        if not obj.animation_data or not obj.animation_data.action: return
        
        for fc in obj.animation_data.action.fcurves:
            if fc.data_path == data_path:
                for kp in fc.keyframe_points:
                    kp.interpolation = 'BEZIER'
                    kp.handle_left_type = 'AUTO'
                    kp.handle_right_type = 'AUTO'
                    
    def limpar_animacoes(self, obj: bpy.types.Object):
        """Remove toda a animação do objeto."""
        if obj and obj.animation_data:
            obj.animation_data_clear()
