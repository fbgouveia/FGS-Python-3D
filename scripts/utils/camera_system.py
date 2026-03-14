# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: camera_system.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: camera_system.py                                  ║
║   Função: Sistema Universal de Câmeras Cinematográficas      ║
║           Qualquer movimento, qualquer ângulo, multi-cam     ║
╚══════════════════════════════════════════════════════════════╝

USO:
  from pathlib import Path
  import sys
  # O orquestrador já deve ter o UTILS_DIR no path, mas caso precise:
  # sys.path.append(str(Path(__file__).parent))
  from camera_system import CameraSystem

  cam_sys = CameraSystem(scene)

  # Criar câmeras:
  cam_ws  = cam_sys.criar("CAM_WS",  posicao=(0,-6,2), alvo=(0,0,1.2), fov=60)
  cam_mcu = cam_sys.criar("CAM_MCU", posicao=(0,-2,1.8), alvo=(0,0,1.5), fov=35)

  # Animar movimentos:
  cam_sys.orbit(cam_ws, alvo=(0,0,1), raio=5, frame_inicio=1, frame_fim=120)
  cam_sys.dolly(cam_ws, inicio=(0,-6,2), fim=(0,-3,1.8), frames=(1,60))

  # Definir cortes:
  cam_sys.corte(frame=1,   camera=cam_ws)
  cam_sys.corte(frame=73,  camera=cam_mcu)
"""

import bpy
import math
from mathutils import Vector, Euler


class CameraSystem:
    """
    Sistema Universal de Câmeras para o FGS Python 3D.
    
    Abstrai a criação, posicionamento e animação de câmeras
    em funções simples, reutilizáveis em qualquer projeto.
    """

    def __init__(self, scene=None):
        self.scene = scene or bpy.context.scene
        self.cameras = {}   # nome → objeto câmera
        self.marcadores = []

    # ─────────────────────────────────────────────────────────────
    # CRIAÇÃO DE CÂMERA
    # ─────────────────────────────────────────────────────────────

    def criar(self, nome: str, posicao=(0, -5, 2), alvo=(0, 0, 1),
              fov=50, use_dof=True, foco_dist=3.0,
              fstop=2.8) -> bpy.types.Object:
        """
        Cria uma câmera cinematográfica completa.
        
        Args:
            nome: Identificador único (ex: "CAM_WS", "CAM_MCU_Boomer")
            posicao: Tupla XYZ da câmera
            alvo: Ponto para onde a câmera olha (XYZ)
            fov: Field of View em graus (35=tele, 50=normal, 70=wide)
            use_dof: Ativar depth of field (desfoque de fundo)
            foco_dist: Distância de foco em metros
            fstop: Abertura do diafragma (1.4=muito blur, 8.0=tudo nítido)
        
        Returns:
            Objeto câmera do Blender
        """
        bpy.ops.object.camera_add(location=posicao)
        cam = bpy.context.active_object
        cam.name = nome
        cam.data.name = f"{nome}_Data"

        # FOV
        cam.data.lens_unit = 'FOV'
        cam.data.angle = math.radians(fov)

        # Depth of Field
        cam.data.dof.use_dof = use_dof
        if use_dof:
            cam.data.dof.focus_distance = foco_dist
            cam.data.dof.aperture_fstop = fstop

        # Clip planes
        cam.data.clip_start = 0.1
        cam.data.clip_end = 1000.0

        # Track To — câmera sempre aponta para o alvo
        alvo_obj = self._criar_alvo(f"{nome}_Alvo", alvo)
        constraint = cam.constraints.new(type='TRACK_TO')
        constraint.target = alvo_obj
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'

        self.cameras[nome] = cam
        return cam

    # Alias para compatibilidade global
    def criar_camera(self, *args, **kwargs):
        """Alias master para criar(). Garante que o Orquestrador Central nunca falhe."""
        return self.criar(*args, **kwargs)

    def _criar_alvo(self, nome: str, posicao) -> bpy.types.Object:
        """Cria objeto Empty como alvo de câmera."""
        bpy.ops.object.empty_add(type='SPHERE', location=posicao)
        alvo = bpy.context.active_object
        alvo.name = nome
        alvo.scale = (0.05, 0.05, 0.05)
        return alvo

    # ─────────────────────────────────────────────────────────────
    # TIPOS DE CÂMERA PRÉ-CONFIGURADOS
    # ─────────────────────────────────────────────────────────────

    def wide_shot(self, nome="CAM_WS", alvo=(0, 0, 1.2)) -> bpy.types.Object:
        """Wide Shot — estabelecimento de cena completa."""
        return self.criar(nome, posicao=(0, -6, 1.8), alvo=alvo, fov=62, use_dof=False)

    def medium_shot(self, nome="CAM_MS", alvo=(0, 0, 1.5),
                    lado="centro") -> bpy.types.Object:
        """Medium Shot — da cintura para cima."""
        x = -1.5 if lado == "esquerda" else (1.5 if lado == "direita" else 0)
        return self.criar(nome, posicao=(x, -3.5, 1.7), alvo=alvo, fov=45, foco_dist=3.5)

    def medium_closeup(self, nome="CAM_MCU", alvo=(0, 0, 1.5),
                       lado="centro") -> bpy.types.Object:
        """Medium Close-Up — peito para cima. Padrão de diálogos."""
        x = -1.8 if lado == "esquerda" else (1.8 if lado == "direita" else 0)
        return self.criar(nome, posicao=(x, -2.2, 1.75), alvo=alvo, fov=38, foco_dist=2.5)

    def closeup(self, nome="CAM_CU", alvo=(0, 0, 1.6),
                lado="centro") -> bpy.types.Object:
        """Close-Up — foco no rosto. Alta expressividade."""
        x = -1.5 if lado == "esquerda" else (1.5 if lado == "direita" else 0)
        return self.criar(nome, posicao=(x, -1.5, 1.7), alvo=alvo, fov=30, fstop=1.8, foco_dist=1.8)

    def over_shoulder(self, nome="CAM_OTS", personagem_frente=(0, 0, 1.5),
                      lado_da_camera="esquerda") -> bpy.types.Object:
        """Over the Shoulder — câmera por cima do ombro de um personagem."""
        x_cam = -1.6 if lado_da_camera == "esquerda" else 1.6
        return self.criar(nome, posicao=(x_cam, -3.0, 1.85), alvo=personagem_frente, fov=44, foco_dist=3.0)

    def cutaway(self, nome="CAM_CUT", posicao=(0, -1.0, 0.7),
                alvo=(0, 0.5, 0.5)) -> bpy.types.Object:
        """Insert / Cutaway — close em detalhe de objeto."""
        return self.criar(nome, posicao=posicao, alvo=alvo, fov=40, foco_dist=1.0, fstop=1.4)

    def pov(self, nome="CAM_POV", posicao=(0, 0, 1.7),
            alvo=(0, -5, 1.0)) -> bpy.types.Object:
        """Point of View — perspectiva subjetiva do personagem."""
        return self.criar(nome, posicao=posicao, alvo=alvo, fov=75, use_dof=False)

    def product_orbit(self, nome="CAM_PRODUCT", raio=3.0,
                      altura=1.0, fov=40) -> bpy.types.Object:
        """Câmera de produto — posição inicial para orbit."""
        return self.criar(nome, posicao=(raio, -raio, altura),
                         alvo=(0, 0, 0.5), fov=fov, foco_dist=raio * 1.2)

    # ─────────────────────────────────────────────────────────────
    # MOVIMENTOS DE CÂMERA
    # ─────────────────────────────────────────────────────────────

    def orbit(self, camera: bpy.types.Object, alvo=(0, 0, 1),
              raio=5.0, altura=2.0, angulo_inicio=0, angulo_fim=360,
              frame_inicio=1, frame_fim=240,
              suave=True):
        """
        Movimento de órbita circular em torno de um ponto.
        
        Args:
            angulo_inicio/fim: Graus (0=frente, 90=direita, 180=costas, 270=esquerda)
            frame_inicio/fim: Range de frames da animação
        """
        total_frames = frame_fim - frame_inicio
        total_angulo = angulo_fim - angulo_inicio

        for f in range(frame_inicio, frame_fim + 1):
            progresso = (f - frame_inicio) / total_frames
            angulo_rad = math.radians(angulo_inicio + progresso * total_angulo)

            x = alvo[0] + raio * math.sin(angulo_rad)
            y = alvo[1] - raio * math.cos(angulo_rad)
            z = altura

            bpy.context.scene.frame_set(f)
            camera.location = (x, y, z)
            camera.keyframe_insert(data_path="location")

        if suave:
            self._suavizar_fcurves(camera, 'location')

    def dolly(self, camera: bpy.types.Object,
              inicio=(0, -6, 2), fim=(0, -3, 1.8),
              frames=(1, 60), suave=True):
        """
        Dolly in/out — aproximação ou afastamento linear em linha reta.
        
        Args:
            inicio: Posição inicial XYZ
            fim: Posição final XYZ (mais perto = dolly in, mais longe = dolly out)
        """
        bpy.context.scene.frame_set(frames[0])
        camera.location = inicio
        camera.keyframe_insert(data_path="location")

        bpy.context.scene.frame_set(frames[1])
        camera.location = fim
        camera.keyframe_insert(data_path="location")

        if suave:
            self._suavizar_fcurves(camera, 'location')

    def crane(self, camera: bpy.types.Object,
              posicao_base=(0, -5, 0.5), altura_fim=3.5,
              frames=(1, 60), suave=True):
        """
        Movimento de grua — câmera sobe ou desce elegantemente.
        Usado para revelar grande ou finalizar com grandiosidade.
        """
        inicio = list(posicao_base)
        fim = [posicao_base[0], posicao_base[1], altura_fim]

        bpy.context.scene.frame_set(frames[0])
        camera.location = inicio
        camera.keyframe_insert(data_path="location")

        bpy.context.scene.frame_set(frames[1])
        camera.location = fim
        camera.keyframe_insert(data_path="location")

        if suave:
            self._suavizar_fcurves(camera, 'location')

    def handheld(self, camera: bpy.types.Object,
                 frame_inicio=1, frame_fim=120,
                 intensidade=0.02, fps=24):
        """
        Efeito câmera na mão — tremido orgânico sutil.
        Adiciona vida e realismo mesmo em cenas simples.
        """
        import random
        pos_base = camera.location.copy()

        for f in range(frame_inicio, frame_fim + 1, 2):
            ruido_x = random.gauss(0, intensidade)
            ruido_y = random.gauss(0, intensidade * 0.5)
            ruido_z = random.gauss(0, intensidade * 0.3)

            bpy.context.scene.frame_set(f)
            camera.location.x = pos_base.x + ruido_x
            camera.location.y = pos_base.y + ruido_y
            camera.location.z = pos_base.z + ruido_z
            camera.keyframe_insert(data_path="location")

    def zoom_dramatico(self, camera: bpy.types.Object,
                       fov_inicio=60, fov_fim=20,
                       frames=(1, 48)):
        """
        Crash Zoom — redução rápida de FOV para efeito dramático.
        Usado no momento de revelação ou impacto.
        """
        bpy.context.scene.frame_set(frames[0])
        camera.data.angle = math.radians(fov_inicio)
        camera.data.keyframe_insert(data_path="angle")

        bpy.context.scene.frame_set(frames[1])
        camera.data.angle = math.radians(fov_fim)
        camera.data.keyframe_insert(data_path="angle")

    def rack_focus(self, camera: bpy.types.Object,
                   foco_inicio=1.0, foco_fim=4.0,
                   frames=(1, 36)):
        """
        Rack Focus — mudança de foco de um plano para outro.
        Direciona atenção sem cortar a cena.
        """
        camera.data.dof.use_dof = True

        bpy.context.scene.frame_set(frames[0])
        camera.data.dof.focus_distance = foco_inicio
        camera.data.keyframe_insert(data_path="dof.focus_distance")

        bpy.context.scene.frame_set(frames[1])
        camera.data.dof.focus_distance = foco_fim
        camera.data.keyframe_insert(data_path="dof.focus_distance")

    def respiracao_camera(self, camera: bpy.types.Object,
                          frame_inicio=1, frame_fim=720,
                          amplitude=0.005):
        """
        Micro-animação de 'respiração' da câmera.
        Mesmo em cenas estáticas, evita o look de câmera travada.
        """
        periodo = 48  # 2 segundos @ 24fps
        pos_base = camera.location.copy()

        for f in range(frame_inicio, frame_fim + 1, periodo // 4):
            progresso = (f - frame_inicio) / periodo
            offset = math.sin(progresso * math.pi * 2) * amplitude

            bpy.context.scene.frame_set(f)
            camera.location.z = pos_base.z + offset
            camera.keyframe_insert(data_path="location", index=2)

    # ─────────────────────────────────────────────────────────────
    # SISTEMA DE CORTES (Multi-cam)
    # ─────────────────────────────────────────────────────────────

    def corte(self, frame: int, camera: bpy.types.Object):
        """
        Define um corte de câmera em um frame específico.
        Os markers ficam visíveis na timeline do Blender.
        """
        marker = self.scene.timeline_markers.new(f"Cut_{camera.name}_F{frame}", frame=frame)
        marker.camera = camera
        self.marcadores.append(marker)

    def aplicar_shot_list(self, shot_list: list):
        """
        Aplica uma lista completa de cortes de uma vez.
        
        Args:
            shot_list: Lista de tuplas [(frame, camera_obj), ...]
        
        Exemplo:
            cam_sys.aplicar_shot_list([
                (1,   cam_ws),
                (73,  cam_mcu_a),
                (145, cam_ots),
            ])
        """
        for frame, cam in shot_list:
            self.corte(frame, cam)

        # Ativar primeira câmera como câmera da cena
        if shot_list:
            self.scene.camera = shot_list[0][1]

        print(f"✅ {len(shot_list)} cortes aplicados na timeline")

    # ─────────────────────────────────────────────────────────────
    # PRESET COMPLETO: PODCAST (Boomer & Kev e qualquer outro)
    # ─────────────────────────────────────────────────────────────

    def setup_podcast(self, pos_personagem_a=(-1.0, 0.8, 1.5),
                      pos_personagem_b=(1.0, 0.8, 1.5)) -> dict:
        """
        Cria o setup completo de câmeras para qualquer formato de podcast.
        6 câmeras posicionadas e prontas para usar.
        
        Returns:
            Dicionário com todas as câmeras criadas
        """
        cameras = {}

        cameras['ws']         = self.wide_shot(nome="CAM_WS", alvo=(0, 0, 1.2))
        cameras['mcu_a']      = self.medium_closeup("CAM_MCU_A", alvo=pos_personagem_a, lado="esquerda")
        cameras['mcu_b']      = self.medium_closeup("CAM_MCU_B", alvo=pos_personagem_b, lado="direita")
        cameras['ots_a']      = self.over_shoulder("CAM_OTS_A", personagem_frente=pos_personagem_b, lado_da_camera="esquerda")
        cameras['ots_b']      = self.over_shoulder("CAM_OTS_B", personagem_frente=pos_personagem_a, lado_da_camera="direita")
        cameras['cutaway']    = self.cutaway("CAM_CUT", posicao=(0, -0.8, 0.65), alvo=(0, 0.5, 0.5))

        # Adicionar respiração a todas as câmeras
        for cam in cameras.values():
            self.respiracao_camera(cam, amplitude=0.003)

        print(f"✅ Setup Podcast: {len(cameras)} câmeras criadas")
        return cameras

    def setup_produto(self, raio=3.0, altura=1.2) -> dict:
        """
        Setup de câmeras para comercial de produto.
        Orbit 360° + close-up + câmera de logo.
        """
        cameras = {}

        cameras['orbit']   = self.product_orbit("CAM_ORBIT", raio=raio, altura=altura)
        cameras['closeup'] = self.closeup("CAM_PRODUCT_CU", alvo=(0, 0, 0.5))
        cameras['wide']    = self.wide_shot("CAM_PRODUCT_WS", alvo=(0, 0, 0.3))

        # Animar orbit
        self.orbit(cameras['orbit'], alvo=(0, 0, 0.5), raio=raio,
                  altura=altura, angulo_inicio=0, angulo_fim=360,
                  frame_inicio=1, frame_fim=720)

        print("✅ Setup Produto: orbit + closeup + wide criados")
        return cameras

    # ─────────────────────────────────────────────────────────────
    # UTILITÁRIOS
    # ─────────────────────────────────────────────────────────────

    def _suavizar_fcurves(self, obj, data_path: str):
        """Suaviza interpolação de keyframes para movimentos fluidos."""
        if not obj.animation_data or not obj.animation_data.action:
            return
        for fcurve in obj.animation_data.action.fcurves:
            if fcurve.data_path == data_path:
                for kp in fcurve.keyframe_points:
                    kp.interpolation = 'BEZIER'

    def listar_cameras(self):
        """Lista todas as câmeras criadas pelo sistema."""
        print(f"\n📷 CÂMERAS CRIADAS ({len(self.cameras)}):")
        for nome, cam in self.cameras.items():
            print(f"   {nome} → {cam.location}")
        print(f"   Cortes na timeline: {len(self.marcadores)}\n")
