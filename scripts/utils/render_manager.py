# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: render_manager.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: render_manager.py                                  ║
║   Função: Sistema Universal de Render                        ║
║           Presets otimizados por tipo de output              ║
╚══════════════════════════════════════════════════════════════╝

USO:
  import sys
  sys.path.append("D:/Blender/blenderscripts/scripts/utils")
  from render_manager import RenderManager

  render = RenderManager()

  # Usar um preset:
  render.preset("youtube",      output="D:/renders/meu_video.mp4")
  render.preset("short_reel",   output="D:/renders/reel.mp4")
  render.preset("comercial",    output="D:/renders/comercial.mp4")
  render.preset("draft",        output="D:/renders/draft.mp4")

  # Ou configurar manualmente:
  render.configurar(
      engine="EEVEE",
      resolucao=(1920, 1080),
      fps=24,
      samples=64,
      output="D:/renders/custom.mp4"
  )

  # Verificar setup antes de renderizar:
  render.relatorio()
"""

import bpy
import os


class RenderManager:
    """
    Sistema Universal de Render do FGS Python 3D.
    
    Abstrai toda a configuração de render em um único ponto,
    com presets otimizados para cada caso de uso.
    """

    # Presets de qualidade
    PRESETS = {
        # ─── RASCUNHO ───────────────────────────────────────────
        "draft": {
            "descricao": "Rascunho rápido para aprovação do cliente",
            "engine": "EEVEE",
            "resolucao": (1280, 720),
            "fps": 24,
            "samples": 16,
            "formato": "MP4",
            "codec": "H264",
            "qualidade_video": "MEDIUM",
            "denoiser": False,
            "bloom": False,
            "tempo_estimado": "~1 min GPU"
        },
        # ─── YOUTUBE HD ─────────────────────────────────────────
        "youtube": {
            "descricao": "YouTube 1080p — séries e episódios",
            "engine": "EEVEE",
            "resolucao": (1920, 1080),
            "fps": 24,
            "samples": 64,
            "formato": "MP4",
            "codec": "H264",
            "qualidade_video": "HIGH",
            "denoiser": False,
            "bloom": True,
            "tempo_estimado": "~5-10 min GPU"
        },
        # ─── SHORT / REEL ────────────────────────────────────────
        "short_reel": {
            "descricao": "Short/Reel vertical 9:16 para redes sociais",
            "engine": "EEVEE",
            "resolucao": (1080, 1920),
            "fps": 30,
            "samples": 64,
            "formato": "MP4",
            "codec": "H264",
            "qualidade_video": "HIGH",
            "denoiser": False,
            "bloom": True,
            "tempo_estimado": "~3-5 min GPU"
        },
        # ─── COMERCIAL ──────────────────────────────────────────
        "comercial": {
            "descricao": "Comercial profissional — Cycles com denoiser",
            "engine": "CYCLES",
            "resolucao": (1920, 1080),
            "fps": 24,
            "samples": 256,
            "formato": "MP4",
            "codec": "H264",
            "qualidade_video": "LOSSLESS",
            "denoiser": True,
            "bloom": False,
            "tempo_estimado": "~20-40 min GPU"
        },
        # ─── CINEMA ─────────────────────────────────────────────
        "cinema": {
            "descricao": "Qualidade cinema — Cycles alto sample 2K",
            "engine": "CYCLES",
            "resolucao": (2560, 1440),
            "fps": 24,
            "samples": 512,
            "formato": "MP4",
            "codec": "H264",
            "qualidade_video": "LOSSLESS",
            "denoiser": True,
            "bloom": False,
            "tempo_estimado": "~1-2h GPU"
        },
        # ─── PRINT / STILL ──────────────────────────────────────
        "print": {
            "descricao": "Imagem estática 4K para impressão",
            "engine": "CYCLES",
            "resolucao": (3840, 2160),
            "fps": 24,
            "samples": 1024,
            "formato": "PNG",
            "codec": None,
            "qualidade_video": None,
            "denoiser": True,
            "bloom": False,
            "tempo_estimado": "~5-15 min GPU (1 frame)"
        },
        # ─── ANIMATIC ───────────────────────────────────────────
        "animatic": {
            "descricao": "Animatic — viewport rápido para story",
            "engine": "EEVEE",
            "resolucao": (1280, 720),
            "fps": 24,
            "samples": 4,
            "formato": "MP4",
            "codec": "H264",
            "qualidade_video": "LOW",
            "denoiser": False,
            "bloom": False,
            "tempo_estimado": "~30 seg GPU"
        },
        # ─── TIKTOK ─────────────────────────────────────────────
        "tiktok": {
            "descricao": "TikTok — vertical 9:16, 30fps",
            "engine": "EEVEE",
            "resolucao": (1080, 1920),
            "fps": 30,
            "samples": 32,
            "formato": "MP4",
            "codec": "H264",
            "qualidade_video": "MEDIUM",
            "denoiser": False,
            "bloom": True,
            "tempo_estimado": "~2-3 min GPU"
        },
        # ─── INSTAGRAM SQUARE ───────────────────────────────────
        "instagram_quad": {
            "descricao": "Instagram quadrado 1:1",
            "engine": "EEVEE",
            "resolucao": (1080, 1080),
            "fps": 30,
            "samples": 32,
            "formato": "MP4",
            "codec": "H264",
            "qualidade_video": "HIGH",
            "denoiser": False,
            "bloom": True,
            "tempo_estimado": "~2-4 min GPU"
        },
    }

    def __init__(self):
        self.scene = bpy.context.scene
        self._preset_atual = None

    # ─────────────────────────────────────────────────────────────
    # API PRINCIPAL
    # ─────────────────────────────────────────────────────────────

    def preset(self, nome: str, output: str = None, frame_inicio=None, frame_fim=None):
        """
        Aplica um preset de render completo.
        
        Args:
            nome:         'draft' | 'youtube' | 'short_reel' | 'comercial' |
                          'cinema' | 'print' | 'animatic' | 'tiktok' | 'instagram_quad'
            output:       Caminho do arquivo de output (sobrescreve padrão)
            frame_inicio: Frame inicial (None = usar da cena)
            frame_fim:    Frame final (None = usar da cena)
        """
        config = self.PRESETS.get(nome)
        if not config:
            print(f"❌ Preset '{nome}' não encontrado.")
            print(f"   Disponíveis: {list(self.PRESETS.keys())}")
            return

        print(f"\n🎬 RENDER PRESET: '{nome}'")
        print(f"   {config['descricao']}")
        print(f"   Tempo estimado: {config['tempo_estimado']}\n")

        # Aplicar configurações
        self._aplicar_engine(config)
        self._aplicar_resolucao(config["resolucao"], config["fps"])
        self._aplicar_output(config, output)
        self._aplicar_qualidade(config)
        self._configurar_gpu()

        if frame_inicio is not None:
            self.scene.frame_start = frame_inicio
        if frame_fim is not None:
            self.scene.frame_end = frame_fim

        self._preset_atual = nome
        self.relatorio()

    def configurar(self, engine="EEVEE", resolucao=(1920, 1080),
                   fps=24, samples=64, output=None,
                   denoiser=True, formato="MP4"):
        """Configuração manual granular do render."""
        config = {
            "engine": engine,
            "resolucao": resolucao,
            "fps": fps,
            "samples": samples,
            "formato": formato,
            "codec": "H264" if formato == "MP4" else None,
            "qualidade_video": "HIGH",
            "denoiser": denoiser,
            "bloom": True
        }
        self._aplicar_engine(config)
        self._aplicar_resolucao(resolucao, fps)
        self._aplicar_output(config, output)
        self._aplicar_qualidade(config)
        self._configurar_gpu()

    # ─────────────────────────────────────────────────────────────
    # CONFIGURAÇÕES INTERNAS
    # ─────────────────────────────────────────────────────────────

    def _aplicar_engine(self, config: dict):
        """Configura o motor de render."""
        engine = config["engine"]
        samples = config["samples"]
        denoiser = config.get("denoiser", False)

        if engine == "EEVEE":
            self.scene.render.engine = 'BLENDER_EEVEE_NEXT'
            eevee = self.scene.eevee
            eevee.taa_render_samples = samples
            eevee.use_bloom = config.get("bloom", False)
            eevee.bloom_intensity = 0.05
            eevee.bloom_threshold = 0.8
            eevee.use_ssr = True
            eevee.use_gtao = True
            eevee.gtao_quality = 0.25
            eevee.use_volumetric_lights = False  # Desligado por padrão para velocidade

        elif engine == "CYCLES":
            self.scene.render.engine = 'CYCLES'
            self.scene.cycles.samples = samples
            self.scene.cycles.use_denoising = denoiser

            if denoiser:
                # Tentar OptiX (NVIDIA) > Open Image Denoise (CPU)
                try:
                    self.scene.cycles.denoiser = 'OPTIX'
                except:
                    self.scene.cycles.denoiser = 'OPENIMAGEDENOISE'

            # Otimizações
            self.scene.cycles.use_adaptive_sampling = True
            self.scene.cycles.adaptive_threshold = 0.01
            self.scene.cycles.max_bounces = 6
            self.scene.cycles.diffuse_bounces = 4
            self.scene.cycles.glossy_bounces = 4
            self.scene.cycles.transmission_bounces = 8
            self.scene.cycles.volume_bounces = 2
            self.scene.cycles.transparent_max_bounces = 8

    def _aplicar_resolucao(self, resolucao: tuple, fps: int):
        """Configura resolução e FPS."""
        self.scene.render.resolution_x = resolucao[0]
        self.scene.render.resolution_y = resolucao[1]
        self.scene.render.resolution_percentage = 100
        self.scene.render.fps = fps

    def _aplicar_output(self, config: dict, output_path: str = None):
        """Configura formato e caminho de saída."""
        formato = config["formato"]

        if output_path:
            self.scene.render.filepath = output_path
        else:
            # Path padrão do projeto
            base = "D:/Blender/blenderscripts/renders/finals/"
            os.makedirs(base, exist_ok=True)
            self.scene.render.filepath = base

        if formato == "MP4":
            self.scene.render.image_settings.file_format = 'FFMPEG'
            self.scene.render.ffmpeg.format = 'MPEG4'
            self.scene.render.ffmpeg.codec = 'H264'

            mapa_qualidade = {
                "LOSSLESS": 'LOSSLESS',
                "HIGH":     'MEDIUM',
                "MEDIUM":   'MEDIUM',
                "LOW":      'LOW'
            }
            crf = mapa_qualidade.get(config.get("qualidade_video", "HIGH"), 'MEDIUM')
            self.scene.render.ffmpeg.constant_rate_factor = crf

            # Áudio
            self.scene.render.ffmpeg.audio_codec = 'AAC'
            self.scene.render.ffmpeg.audio_bitrate = 192

        elif formato == "PNG":
            self.scene.render.image_settings.file_format = 'PNG'
            self.scene.render.image_settings.color_mode = 'RGBA'
            self.scene.render.image_settings.compression = 15

        elif formato == "EXR":
            self.scene.render.image_settings.file_format = 'OPEN_EXR'
            self.scene.render.image_settings.exr_codec = 'ZIP'

    def _aplicar_qualidade(self, config: dict):
        """Configurações adicionais de qualidade."""
        # Motion Blur
        self.scene.render.use_motion_blur = False  # Ligado manualmente quando necessário

        # Color Management
        self.scene.view_settings.view_transform = 'Filmic'
        self.scene.view_settings.look = 'Medium High Contrast'
        self.scene.view_settings.gamma = 1.0
        self.scene.view_settings.exposure = 0.0

        # Render threads — usar todos os cores
        self.scene.render.threads_mode = 'AUTO'

    def _configurar_gpu(self):
        """Ativa GPU automaticamente se disponível."""
        try:
            prefs = bpy.context.preferences
            cycles_prefs = prefs.addons.get('cycles')
            if not cycles_prefs:
                return

            cprefs = cycles_prefs.preferences

            # Tentar OptiX → CUDA → HIP → Fallback CPU
            for device_type in ['OPTIX', 'CUDA', 'HIP', 'METAL']:
                try:
                    cprefs.compute_device_type = device_type
                    # Ativar todos os devices
                    for device in cprefs.devices:
                        device.use = True
                    self.scene.cycles.device = 'GPU'
                    print(f"   ✅ GPU ativado: {device_type}")
                    return
                except:
                    continue

            print("   ⚠️ GPU não disponível — usando CPU")
        except Exception as e:
            print(f"   ⚠️ Config GPU: {e}")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITING (Pós-produção automática)
    # ─────────────────────────────────────────────────────────────

    def ativar_compositing(self, estilo="cinematico"):
        """
        Ativa compositing com pós-produção automática.
        
        estilo: 'cinematico' | 'vibrante' | 'minimalista' | 'neon'
        """
        scene = self.scene
        scene.use_nodes = True
        tree = scene.node_tree
        nodes = tree.nodes
        links = tree.links
        nodes.clear()

        # Nós base
        render_layers = nodes.new('CompositorNodeRLayers')
        render_layers.location = (-600, 0)

        composite = nodes.new('CompositorNodeComposite')
        composite.location = (600, 0)

        viewer = nodes.new('CompositorNodeViewer')
        viewer.location = (600, -200)

        ultimo_output = render_layers.outputs['Image']

        if estilo == "cinematico":
            # Glare sutil
            glare = nodes.new('CompositorNodeGlare')
            glare.location = (-300, 100)
            glare.glare_type = 'FOG_GLOW'
            glare.threshold = 0.85
            glare.size = 6
            glare.mix = -0.5  # Muito sutil

            # Lens distortion (aberração cromática leve)
            lens = nodes.new('CompositorNodeLensdist')
            lens.location = (-100, 0)
            lens.inputs['Distortion'].default_value = -0.02
            lens.inputs['Dispersion'].default_value = 0.01

            # Vignette via Ellipse Mask
            ellipse = nodes.new('CompositorNodeEllipseMask')
            ellipse.location = (-400, -200)
            ellipse.width = 0.85
            ellipse.height = 0.85

            blur_vig = nodes.new('CompositorNodeBlur')
            blur_vig.location = (-200, -200)
            blur_vig.size_x = 80
            blur_vig.size_y = 80

            invert = nodes.new('CompositorNodeInvert')
            invert.location = (-100, -200)

            mix_vig = nodes.new('CompositorNodeMixRGB')
            mix_vig.location = (100, 0)
            mix_vig.blend_type = 'MULTIPLY'

            # Conectar
            links.new(render_layers.outputs['Image'], glare.inputs['Image'])
            links.new(glare.outputs['Image'], lens.inputs['Image'])
            links.new(ellipse.outputs['Mask'], blur_vig.inputs['Image'])
            links.new(blur_vig.outputs['Image'], invert.inputs['Color'])
            links.new(lens.outputs['Image'], mix_vig.inputs[1])
            links.new(invert.outputs['Color'], mix_vig.inputs[2])
            ultimo_output = mix_vig.outputs['Image']

        elif estilo == "vibrante":
            # Saturação aumentada + contraste
            color_balance = nodes.new('CompositorNodeColorBalance')
            color_balance.location = (-200, 0)
            color_balance.correction_method = 'LIFT_GAMMA_GAIN'
            color_balance.gain = (1.1, 1.05, 1.0)  # Ligeiramente mais quente

            links.new(render_layers.outputs['Image'], color_balance.inputs['Image'])
            ultimo_output = color_balance.outputs['Image']

        elif estilo == "neon":
            # Brilho neon exagerado
            glare = nodes.new('CompositorNodeGlare')
            glare.location = (-200, 0)
            glare.glare_type = 'STREAKS'
            glare.threshold = 0.5
            glare.size = 8
            glare.streaks = 4

            links.new(render_layers.outputs['Image'], glare.inputs['Image'])
            ultimo_output = glare.outputs['Image']

        # Conectar ao output final
        links.new(ultimo_output, composite.inputs['Image'])
        links.new(ultimo_output, viewer.inputs['Image'])

        print(f"   ✅ Compositing '{estilo}' ativado")

    # ─────────────────────────────────────────────────────────────
    # MOTION BLUR
    # ─────────────────────────────────────────────────────────────

    def ativar_motion_blur(self, shutter=0.5):
        """
        Ativa motion blur para movimentos dinâmicos.
        
        Args:
            shutter: Ângulo de obturador (0.1=pouco, 0.5=normal, 1.0=muito)
        """
        self.scene.render.use_motion_blur = True
        self.scene.render.motion_blur_shutter = shutter
        print(f"   ✅ Motion Blur ativado: shutter={shutter}")

    # ─────────────────────────────────────────────────────────────
    # UTILIDADES
    # ─────────────────────────────────────────────────────────────

    def relatorio(self):
        """Exibe relatório completo da configuração atual."""
        r = self.scene.render
        print("\n" + "─" * 50)
        print("  📊 RELATÓRIO DE RENDER")
        print("─" * 50)
        print(f"  Engine:       {r.engine}")
        print(f"  Resolução:    {r.resolution_x}×{r.resolution_y}px")
        print(f"  FPS:          {r.fps}")
        print(f"  Frames:       {self.scene.frame_start} → {self.scene.frame_end}")
        print(f"  Duração:      {(self.scene.frame_end - self.scene.frame_start) / r.fps:.1f}s")
        print(f"  Formato:      {r.image_settings.file_format}")
        print(f"  Output:       {r.filepath}")

        if r.engine == 'BLENDER_EEVEE_NEXT':
            print(f"  Samples:      {self.scene.eevee.taa_render_samples}")
        elif r.engine == 'CYCLES':
            print(f"  Samples:      {self.scene.cycles.samples}")
            print(f"  Denoiser:     {'Sim' if self.scene.cycles.use_denoising else 'Não'}")

        print("─" * 50)
        print("  🚀 PARA RENDERIZAR:")
        print("     F12        → Render de 1 frame")
        print("     Ctrl+F12   → Render animação completa")
        print("─" * 50 + "\n")

    def listar_presets(self):
        """Lista todos os presets disponíveis."""
        print("\n🎬 PRESETS DISPONÍVEIS:")
        for nome, config in self.PRESETS.items():
            res = config["resolucao"]
            print(f"   '{nome}' → {res[0]}×{res[1]} | {config['engine']} | {config['tempo_estimado']}")
        print()
