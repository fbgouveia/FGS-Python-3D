"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: transitions_engine.py                              ║
║   Função: Motor de Transições Conscientes (Context-Aware)    ║
║           Gera entradas e saídas que respeitam a psicologia  ║
║           do tema e o clima (pesado, alerta, alívio).        ║
╚══════════════════════════════════════════════════════════════╝

USO:
  from transitions_engine import TransitionsEngine
  trans = TransitionsEngine()

  # O script detecta automaticamente o tom e aplica no final do B-Roll
  trans.aplicar_saida("reflexivo", camera, luz_principal, frame_inicio=60, frame_fim=72)
"""

import bpy
import math

class TransitionsEngine:
    """
    Motor que traduz climas emocionais em transições cinematográficas,
    evitando cortes bruscos e efeitos de 'YouTuber' em temas sérios.
    """

    def __init__(self, fps=24):
        self.fps = fps
        self.scene = bpy.context.scene

    def aplicar_entrada(self, clima: str, obj_camera: bpy.types.Object, luz_principal=None, frame_inicio=1, duracao=12):
        """
        Aplica a transição no começo do clip (Quando sai da Psicóloga para o B-Roll).
        """
        frame_fim = frame_inicio + duracao
        
        if clima in ["reflexivo", "depressao", "luto", "peso"]:
            # Transição: Emergindo do escuro (Fade In de luz lento) + Focus Pull
            if luz_principal:
                self._animar_luz(luz_principal, inicio=0.0, fim=luz_principal.data.energy, f_in=frame_inicio, f_out=frame_fim)
            self._dof_pull(obj_camera, inicio_dist=0.1, fim_dist=5.0, f_in=frame_inicio, f_out=frame_fim)
            
        elif clima in ["alerta", "ansiedade", "panico", "burnout"]:
            # Transição: Abertura seca como um "piscar de olhos" pesado
            # Corta logo seco, não tem fade in. Mas a câmera entra tremendo.
            pass # Sem fade in suave, o corte brusco assusta e chama atenção.
            
        elif clima in ["solucao", "clareza", "paz", "terapia"]:
            # Transição: Luz vazando (Light Leak branco) e câmera descendo suave
            if luz_principal:
                luz_over = luz_principal.data.energy * 3.0
                self._animar_luz(luz_principal, inicio=luz_over, fim=luz_principal.data.energy, f_in=frame_inicio, f_out=frame_fim)
            self._mover_camera_suave(obj_camera, offset_z=1.0, f_in=frame_inicio, f_out=frame_fim)

        print(f"   🎞️ Transição de Entrada ({clima}) aplicada. [Frames {frame_inicio}-{frame_fim}]")

    def aplicar_saida(self, clima: str, obj_camera: bpy.types.Object, luz_principal=None, profundidade_camera=0.5, frame_inicio=60, frame_fim=72):
        """
        Aplica a transição no fim do clip (Quando volta do B-Roll para a Psicóloga).
        """
        if clima in ["reflexivo", "depressao", "luto", "peso"]:
            # Transição "Mergulho Interno": A luz vai morrendo suavemente, a câmera perde o foco
            # Volta para a locutora passando uma sensação de introspecção grave.
            if luz_principal:
                self._animar_luz(luz_principal, inicio=luz_principal.data.energy, fim=0.0, f_in=frame_inicio, f_out=frame_fim)
            self._dof_pull(obj_camera, inicio_dist=5.0, fim_dist=profundidade_camera, f_in=frame_inicio, f_out=frame_fim)
            # Áudio: Sugerir um LPF (Low Pass Filter) caindo.
            
        elif clima in ["alerta", "ansiedade", "panico", "burnout"]:
            # Transição "Obstrução Fóbica": Um bloqueio passa na frente da lente
            # Ou a câmera da um zoom-in violento até o preenchimento total em preto/sombra.
            self._mover_camera_suave(obj_camera, offset_y=2.0, f_in=frame_inicio, f_out=frame_fim, rapido=True)
            self._dof_pull(obj_camera, inicio_dist=5.0, fim_dist=0.1, f_in=frame_inicio, f_out=frame_fim)
            
        elif clima in ["solucao", "clareza", "paz", "terapia"]:
            # Transição "Elevação": Câmera sobe em direção à luz, clareia tudo (White Out)
            # Retorna para a profissional de saúde em um estado de "abertura".
            if luz_principal:
                luz_over = luz_principal.data.energy * 5.0
                self._animar_luz(luz_principal, inicio=luz_principal.data.energy, fim=luz_over, f_in=frame_inicio, f_out=frame_fim)
            self._mover_camera_suave(obj_camera, offset_z=1.5, f_in=frame_inicio, f_out=frame_fim)

        print(f"   🎞️ Transição de Saída ({clima}) aplicada. [Frames {frame_inicio}-{frame_fim}]")

    # --- Auxiliares Privados de Animação ---

    def _animar_luz(self, luz, inicio, fim, f_in, f_out):
        self.scene.frame_set(f_in)
        luz.data.energy = inicio
        luz.data.keyframe_insert(data_path="energy")
        
        self.scene.frame_set(f_out)
        luz.data.energy = fim
        luz.data.keyframe_insert(data_path="energy")
        self._suavizar_fcurve(luz.data, "energy")

    def _dof_pull(self, camera, inicio_dist, fim_dist, f_in, f_out):
        if not camera.data.dof.use_dof:
            camera.data.dof.use_dof = True
            
        self.scene.frame_set(f_in)
        camera.data.dof.focus_distance = inicio_dist
        camera.data.keyframe_insert(data_path="dof.focus_distance")
        
        self.scene.frame_set(f_out)
        camera.data.dof.focus_distance = fim_dist
        camera.data.keyframe_insert(data_path="dof.focus_distance")
        self._suavizar_fcurve(camera.data, "dof.focus_distance")

    def _mover_camera_suave(self, camera, offset_y=0.0, offset_z=0.0, f_in=1, f_out=12, rapido=False):
        ini_loc = camera.location.copy()
        
        self.scene.frame_set(f_in)
        camera.location = ini_loc
        camera.keyframe_insert(data_path="location")
        
        self.scene.frame_set(f_out)
        camera.location.y += offset_y
        camera.location.z += offset_z
        camera.keyframe_insert(data_path="location")
        
        if rapido:
            # Ease In acelerando
            for fc in camera.animation_data.action.fcurves:
                if fc.data_path == "location":
                    fc.keyframe_points[0].interpolation = 'BEZIER'
                    fc.keyframe_points[0].easing = 'EASE_IN'
        else:
            self._suavizar_fcurve(camera, "location")

    def _suavizar_fcurve(self, obj, data_path: str):
        if hasattr(obj, "animation_data") and obj.animation_data and obj.animation_data.action:
            for fc in obj.animation_data.action.fcurves:
                if fc.data_path == data_path:
                    for kp in fc.keyframe_points:
                        kp.interpolation = 'BEZIER'
                        kp.handle_left_type = 'AUTO'
                        kp.handle_right_type = 'AUTO'
