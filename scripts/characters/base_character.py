# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: base_character.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: base_character.py                                 ║
║   Função: Classe Base para Personagens Humanoides (Lorena)   ║
║           Integração com Rigify, Mocap e Estilos Ghost       ║
╚══════════════════════════════════════════════════════════════╝
"""

import bpy
import math
import sys
from pathlib import Path

# Setup paths
BASE_DIR = Path("D:/Blender/blenderscripts")
sys.path.append(str(BASE_DIR / "scripts" / "utils"))

try:
    from character_factory import CharacterFactory
    from materials_library import MaterialLibrary
except ImportError as e:
    print(f"❌ Erro ao importar dependências: {e}")

class HumanoidCharacter:
    """
    Representação de um personagem humanoide compatível com o ecossistema FGS.
    Focado na Lorena (Avatar IA Holográfica).
    """
    
    def __init__(self, nome="Lorena", escala=1.0):
        self.nome = nome
        self.escala = escala
        self.lib = MaterialLibrary()
        self.factory = CharacterFactory(self.lib)
        self.meta_data = {
            "versao": "1.0",
            "tipo": "holographic_ai"
        }

    def build(self, posicao=(0, 0, 0), estilo="holograma"):
        """
        Gera a geometria e materiais do personagem.
        """
        print(f"✨ Gerando avatar: {self.nome}...")
        
        # Usar a fábrica para gerar a base estilizada (humanoide)
        objetos = self.factory.criar(
            nome=self.nome,
            tipo="humano",
            especie="humano_f",
            posicao=posicao,
            proporcao=self.escala,
            cor_corpo=(0.1, 0.5, 1.0) # Azul base se não for holograma
        )
        
        # Aplicar estilo específico
        if estilo == "holograma":
            mat_holograma = self.lib.holograma(cor=(0.1, 0.8, 1.0), opacidade=0.4)
            for obj in objetos.values():
                if isinstance(obj, bpy.types.Object) and obj.type == 'MESH':
                    self.lib.aplicar(obj, mat_holograma)
                    
        return objetos

    def setup_rig(self):
        """
        Cria uma armature básica ou vincula ao Rigify.
        P0: Implementação de Meta-Rig para Retargeting posterior.
        """
        # TODO: Implementar geração de Armature proporcional
        # Por enquanto, focamos na existência do personagem na cena.
        pass

    def speak(self, phrase_length_frames=60):
        """Gera animação de fala (head bob + mandíbula se houver)."""
        self.factory.head_bob(self.nome, frame_fim=phrase_length_frames)

if __name__ == "__main__":
    # Teste de criação da Lorena
    lorena = HumanoidCharacter("Lorena")
    lorena.build(estilo="holograma")
    print(f"✅ Avatar {lorena.nome} inicializado com sucesso.")
