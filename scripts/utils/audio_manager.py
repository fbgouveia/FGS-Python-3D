# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: audio_manager.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: audio_manager.py                                  ║
║   Função: Gerenciador de Áudio (SFX & BGM) no Blender VSE   ║
╚══════════════════════════════════════════════════════════════╝

Este módulo gerencia a inserção e sincronização de arquivos de áudio
no Video Sequence Editor (VSE) do Blender. Permite adicionar trilhas 
sonoras (BGM) e efeitos sonoros (SFX) via Python.
"""

import bpy
import os

class AudioManager:
    """
    Controlador de áudio do FGS Python 3D.
    Trabalha com o Video Sequence Editor para montagem sonora.
    """

    def __init__(self):
        # Garante que o VSE está habilitado
        if not bpy.context.scene.sequence_editor:
            bpy.context.scene.sequence_editor_create()
        self.sequencer = bpy.context.scene.sequence_editor

    def limpar_audio(self):
        """Remove todos os strips de áudio da cena."""
        if not self.sequencer:
            return
        
        strips = self.sequencer.sequences
        for s in strips:
            if s.type == 'SOUND':
                strips.remove(s)
        print("   🧹 Limpeza de áudio concluída")

    def adicionar_bgm(self, caminho_arquivo: str, volume: float = 0.5, 
                      fade_in: float = 1.0, fade_out: float = 1.0):
        """
        Adiciona uma música de fundo (BGM).
        
        Args:
            caminho_arquivo: Caminho absoluto para o arquivo .mp3 ou .wav
            volume: Volume inicial (0.0 a 1.0)
            fade_in: Duração do fade in em segundos
            fade_out: Duração do fade out em segundos
        """
        if not os.path.exists(caminho_arquivo):
            print(f"   ⚠️ Arquivo BGM não encontrado: {caminho_arquivo}")
            return None

        # Adicionar no Channel 1
        strip = self.sequencer.sequences.new_sound(
            name="BGM_Track",
            filepath=caminho_arquivo,
            channel=1,
            frame_start=1
        )
        
        strip.volume = volume
        
        # Aplicar Fades
        fps = bpy.context.scene.render.fps
        if fade_in > 0:
            self._aplicar_fade(strip, 1, int(fade_in * fps), 0.0, volume)
        
        # Fade out no final do strip
        if fade_out > 0:
            fim = strip.frame_final_duration
            self._aplicar_fade(strip, int(fim - fade_out * fps), int(fim), volume, 0.0)

        print(f"   🎶 BGM Adicionada: {os.path.basename(caminho_arquivo)}")
        return strip

    def adicionar_sfx(self, caminho_arquivo: str, frame_inicio: int, volume: float = 1.0):
        """
        Adiciona um efeito sonoro (SFX) em um frame específico.
        """
        if not os.path.exists(caminho_arquivo):
            print(f"   ⚠️ Arquivo SFX não encontrado: {caminho_arquivo}")
            return None

        # Procurar canal livre (começa do 2 para não bater na BGM)
        channel = 2
        existing_channels = [s.channel for s in self.sequencer.sequences]
        while channel in existing_channels:
            channel += 1

        strip = self.sequencer.sequences.new_sound(
            name=f"SFX_{os.path.basename(caminho_arquivo)}",
            filepath=caminho_arquivo,
            channel=channel,
            frame_start=frame_inicio
        )
        strip.volume = volume
        
        print(f"   🔊 SFX Adicionado: {os.path.basename(caminho_arquivo)} no frame {frame_inicio}")
        return strip

    def _aplicar_fade(self, strip, frame_ini, frame_fim, vol_ini, vol_fim):
        """Helper para criar keyframes de volume (Fade)."""
        strip.volume = vol_ini
        strip.keyframe_insert(data_path="volume", frame=frame_ini)
        strip.volume = vol_fim
        strip.keyframe_insert(data_path="volume", frame=frame_fim)

    def configurar_mixagem_final(self):
        """Ajusta as configurações de render de áudio para MP3/Mixagem padrão."""
        scene = bpy.context.scene
        scene.render.ffmpeg.audio_codec = 'MP3'
        scene.render.ffmpeg.audio_bitrate = 192
        print("   🎚️ Render de áudio configurado para MP3 192kbps")

if __name__ == "__main__":
    # Teste rápido se rodar direto
    am = AudioManager()
    print("AudioManager inicializado.")
