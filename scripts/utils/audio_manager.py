"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: audio_manager.py                                   ║
║   Função: Gerenciador de Áudio (SFX, Música e Voz)           ║
║           Usa o Video Sequence Editor (VSE) do Blender       ║
╚══════════════════════════════════════════════════════════════╝

USO:
  import sys
  sys.path.append("D:/Blender/blenderscripts/scripts/utils")
  from audio_manager import AudioManager

  audio = AudioManager()

  # Adicionar música de fundo (toca do início ao fim com volume baixo)
  audio.bgm("D:/Blender/blenderscripts/audio/music/lofi_chill.mp3", volume=0.15, frame=1)

  # Adicionar SFX num frame de impacto (ex: explosão ou corte de câmera)
  audio.sfx("D:/Blender/blenderscripts/audio/sfx/whoosh_transit.wav", volume=0.8, frame=120)

  # Adicionar fala do personagem
  audio.voice("D:/Blender/blenderscripts/audio/voice/boomer_ep01.wav", frame=24)
"""

import bpy
import os

class AudioManager:
    """
    Abstração para adicionar trilhas de áudio diretamente na 
    timeline (VSE) do Blender via Python, permitindo renderizar
    o vídeo já 100% mixado com som.
    """

    def __init__(self):
        self.scene = bpy.context.scene
        
        # Garante que o Video Sequence Editor existe
        if not self.scene.sequence_editor:
            self.scene.sequence_editor_create()

    def _adicionar_audio(self, caminho_arquivo: str, frame: int,
                         canal: int, volume: float) -> bpy.types.SoundSequence:
        """Função base para carregar um áudio na timeline."""
        if not os.path.exists(caminho_arquivo):
            print(f"⚠️ Áudio não encontrado: {caminho_arquivo}")
            return None

        nome_strip = os.path.basename(caminho_arquivo)
        
        # Cria a "faixa" de áudio no VSE do Blender
        strip = self.scene.sequence_editor.sequences.new_sound(
            name=nome_strip,
            filepath=caminho_arquivo,
            channel=canal,
            frame_start=frame
        )
        strip.volume = volume
        return strip

    def bgm(self, caminho_musica: str, volume=0.15, frame=1):
        """Música de fundo (BackGround Music) — sempre no Canal 1"""
        s = self._adicionar_audio(caminho_musica, frame, canal=1, volume=volume)
        if s: print(f"   🎵 Música (BGM) adicionada: {os.path.basename(caminho_musica)}")

    def voice(self, caminho_voz: str, frame: int, volume=1.0):
        """Falas dos personagens — sempre no Canal 2"""
        s = self._adicionar_audio(caminho_voz, frame, canal=2, volume=volume)
        if s: print(f"   🗣️ Voz adicionada no frame {frame}")

    def sfx(self, caminho_sfx: str, frame: int, volume=1.0):
        """Efeitos Sonoros (Sound Effects) — sempre no Canal 3 ou superior"""
        s = self._adicionar_audio(caminho_sfx, frame, canal=3, volume=volume)
        if s: print(f"   💥 Efeito sonoro adicionado no frame {frame}")
        
    def limpar_timeline_de_audio(self):
        """Deleta todas as faixas de áudio antes de um novo render."""
        for seq in self.scene.sequence_editor.sequences:
            if seq.type == 'SOUND':
                self.scene.sequence_editor.sequences.remove(seq)
        print("   🧹 Timeline de áudio limpa.")
