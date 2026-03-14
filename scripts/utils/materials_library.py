# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: materials_library.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: materials_library.py                              ║
║   Função: Biblioteca Universal de Materiais PBR             ║
║           100% procedural — sem texturas externas           ║
║   Uso: Importar e chamar criar_material() em qualquer        ║
║        outro script do projeto                              ║
╚══════════════════════════════════════════════════════════════╝

USO:
  # No topo de qualquer outro script:
  import sys
  sys.path.append("D:/Blender/blenderscripts/scripts/utils")
  from materials_library import MaterialLibrary

  lib = MaterialLibrary()

  # Criar materiais:
  mat_metal    = lib.metal(cor=(0.8, 0.8, 0.9), roughness=0.1)
  mat_plastico = lib.plastico(cor=(0.9, 0.2, 0.1), roughness=0.5)
  mat_pele     = lib.pele_estilizada(cor=(0.85, 0.6, 0.45))
  mat_agua     = lib.liquido(tipo="agua")
  mat_neon     = lib.neon(cor=(0.0, 1.0, 0.8), intensidade=3.0)

  # Aplicar no objeto:
  lib.aplicar(objeto, mat_metal)
"""

import bpy
import random
from mathutils import Color


class MaterialLibrary:
    """
    Biblioteca Central de Materiais do FGS Python 3D.
    
    Todos os materiais são 100% procedurais (nó-based).
    Sem dependência de texturas externas.
    Reutilizável em qualquer projeto.
    """

    def __init__(self, prefixo="FGS"):
        """
        Args:
            prefixo: Prefixo para nomear materiais (evita conflitos entre projetos)
        """
        self.prefixo = prefixo
        self._cache = {}  # Evita duplicar materiais idênticos

    # ─────────────────────────────────────────────────────────────
    # UTILITÁRIOS INTERNOS
    # ─────────────────────────────────────────────────────────────

    def _nome(self, categoria: str, variacao: str) -> str:
        return f"{self.prefixo}_{categoria}_{variacao}"

    def _existe(self, nome: str):
        return bpy.data.materials.get(nome)

    def _base_principled(self, nome: str) -> tuple:
        """Cria material base com Principled BSDF e retorna (mat, nodes, links, bsdf, output)."""
        mat = bpy.data.materials.new(name=nome)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (300, 0)
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

        return mat, nodes, links, bsdf, output

    def aplicar(self, obj, mat):
        """Aplica material a um objeto Blender."""
        if obj is None or mat is None:
            return
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

    def aplicar_por_nome(self, nome_objeto: str, mat):
        """Aplica material buscando objeto pelo nome."""
        obj = bpy.data.objects.get(nome_objeto)
        if obj:
            self.aplicar(obj, mat)

    # ─────────────────────────────────────────────────────────────
    # CATEGORIA 1: MATERIAIS FÍSICOS (PBR realistas)
    # ─────────────────────────────────────────────────────────────

    def metal(self, cor=(0.8, 0.8, 0.85), roughness=0.15,
              anisotropia=0.0, variacao="_01") -> bpy.types.Material:
        """
        Metal polido: aço, alumínio, ouro, prata, bronze.
        
        Args:
            cor: Cor base do metal (RGB 0-1)
            roughness: 0.0=espelho perfeito, 1.0=fosco
            anisotropia: Riscos na superfície (0-1)
        """
        nome = self._nome("metal", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat, nodes, links, bsdf, output = self._base_principled(nome)

        bsdf.inputs['Base Color'].default_value = (*cor, 1.0)
        bsdf.inputs['Metallic'].default_value = 1.0
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Anisotropic'].default_value = anisotropia
        bsdf.inputs['Specular IOR Level'].default_value = 0.8

        return mat

    def metal_ouro(self) -> bpy.types.Material:
        """Atalho: ouro polido (comerciais de luxo)."""
        return self.metal(cor=(0.9, 0.7, 0.2), roughness=0.08, variacao="ouro")

    def metal_prata(self) -> bpy.types.Material:
        """Atalho: prata polida."""
        return self.metal(cor=(0.85, 0.87, 0.9), roughness=0.05, variacao="prata")

    def metal_aco_escovado(self) -> bpy.types.Material:
        """Atalho: aço escovado (microfones, eletrodomésticos)."""
        return self.metal(cor=(0.6, 0.62, 0.65), roughness=0.4, anisotropia=0.7, variacao="aco_escovado")

    def plastico(self, cor=(0.9, 0.2, 0.1), roughness=0.4,
                 translucido=False, variacao="_01") -> bpy.types.Material:
        """
        Plástico sólido ou translúcido.
        roughness baixo = brilhante (embalagem), alto = fosco (móvel)
        """
        nome = self._nome("plastico", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat, nodes, links, bsdf, output = self._base_principled(nome)

        bsdf.inputs['Base Color'].default_value = (*cor, 1.0)
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = 0.0

        if translucido:
            bsdf.inputs['Transmission Weight'].default_value = 0.3

        return mat

    def borracha(self, cor=(0.05, 0.05, 0.05), variacao="_01") -> bpy.types.Material:
        """Borracha fosca — pneus, cabos, solas."""
        nome = self._nome("borracha", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat, nodes, links, bsdf, output = self._base_principled(nome)
        bsdf.inputs['Base Color'].default_value = (*cor, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.95
        bsdf.inputs['Specular IOR Level'].default_value = 0.1

        return mat

    def madeira(self, cor_base=(0.35, 0.2, 0.1), cor_veio=(0.25, 0.13, 0.06),
                roughness=0.65, variacao="_01") -> bpy.types.Material:
        """
        Madeira com veios procedurais (sem textura externa).
        Usa Wave Texture para simular veio do material.
        """
        nome = self._nome("madeira", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat = bpy.data.materials.new(name=nome)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Wave texture simula veio da madeira
        tex_coord = nodes.new('ShaderNodeTexCoord')
        tex_coord.location = (-600, 0)

        mapping = nodes.new('ShaderNodeMapping')
        mapping.location = (-400, 0)
        mapping.inputs['Scale'].default_value = (1.0, 5.0, 1.0)  # Estica veios

        wave = nodes.new('ShaderNodeTexWave')
        wave.location = (-200, 0)
        wave.wave_type = 'RINGS'
        wave.inputs['Scale'].default_value = 3.0
        wave.inputs['Distortion'].default_value = 2.0
        wave.inputs['Detail'].default_value = 5.0
        wave.inputs['Detail Scale'].default_value = 1.5

        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.location = (0, 0)
        color_ramp.color_ramp.elements[0].color = (*cor_veio, 1.0)
        color_ramp.color_ramp.elements[1].color = (*cor_base, 1.0)

        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (250, 0)
        bsdf.inputs['Roughness'].default_value = roughness

        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (500, 0)

        links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
        links.new(wave.outputs['Color'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

        return mat

    def vidro(self, cor=(0.9, 0.95, 1.0), ior=1.45,
              roughness=0.0, variacao="_01") -> bpy.types.Material:
        """Vidro transparente com refração. Requer Cycles para resultado real."""
        nome = self._nome("vidro", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat, nodes, links, bsdf, output = self._base_principled(nome)
        mat.blend_method = 'BLEND'

        bsdf.inputs['Base Color'].default_value = (*cor, 1.0)
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['IOR'].default_value = ior
        bsdf.inputs['Transmission Weight'].default_value = 1.0
        bsdf.inputs['Alpha'].default_value = 0.15

        return mat

    # ─────────────────────────────────────────────────────────────
    # CATEGORIA 2: MATERIAIS ORGÂNICOS (personagens, natureza)
    # ─────────────────────────────────────────────────────────────

    def pele_estilizada(self, cor=(0.85, 0.65, 0.5),
                        variacao="_01") -> bpy.types.Material:
        """
        Pele estilizada para personagens cartoon / semi-realistas.
        SSS (subsurface scattering) suave para aparência orgânica.
        """
        nome = self._nome("pele", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat, nodes, links, bsdf, output = self._base_principled(nome)

        bsdf.inputs['Base Color'].default_value = (*cor, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.7
        bsdf.inputs['Subsurface Weight'].default_value = 0.15
        bsdf.inputs['Subsurface Radius'].default_value = (1.0, 0.2, 0.1)
        bsdf.inputs['Specular IOR Level'].default_value = 0.3

        return mat

    def pelo_animal(self, cor_base=(0.45, 0.28, 0.15),
                    cor_ponta=None, variacao="_01") -> bpy.types.Material:
        """
        Pelo de animal estilizado (urso, raposa, lobo, etc.).
        Usa noise texture para variação natural de cor.
        """
        nome = self._nome("pelo", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        if cor_ponta is None:
            cor_ponta = tuple(max(0, c - 0.15) for c in cor_base)

        mat = bpy.data.materials.new(name=nome)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Noise para variação natural
        noise = nodes.new('ShaderNodeTexNoise')
        noise.location = (-400, 0)
        noise.inputs['Scale'].default_value = 8.0
        noise.inputs['Detail'].default_value = 4.0
        noise.inputs['Roughness'].default_value = 0.6

        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.location = (-200, 0)
        color_ramp.color_ramp.elements[0].color = (*cor_ponta, 1.0)
        color_ramp.color_ramp.elements[1].color = (*cor_base, 1.0)
        color_ramp.color_ramp.elements[0].position = 0.35
        color_ramp.color_ramp.elements[1].position = 0.65

        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (50, 0)
        bsdf.inputs['Roughness'].default_value = 0.85
        bsdf.inputs['Subsurface Weight'].default_value = 0.08
        bsdf.inputs['Sheen Weight'].default_value = 0.3  # Brilho suave do pelo

        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (350, 0)

        links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

        return mat

    def folha(self, cor=(0.1, 0.5, 0.1), variacao="_01") -> bpy.types.Material:
        """Folha de planta/árvore com SSS vegetal."""
        nome = self._nome("folha", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat, nodes, links, bsdf, output = self._base_principled(nome)
        mat.use_backface_culling = False

        bsdf.inputs['Base Color'].default_value = (*cor, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.6
        bsdf.inputs['Subsurface Weight'].default_value = 0.2
        bsdf.inputs['Subsurface Radius'].default_value = (0.1, 0.5, 0.1)

        return mat

    # ─────────────────────────────────────────────────────────────
    # CATEGORIA 3: LÍQUIDOS
    # ─────────────────────────────────────────────────────────────

    def liquido(self, tipo="agua", cor=None,
                variacao="_01") -> bpy.types.Material:
        """
        Líquido físicamente baseado.
        
        tipo: 'agua' | 'mel' | 'refrigerante' | 'leite' | 'vinho' | 'custom'
        cor: sobrescreve a cor padrão do tipo
        """
        TIPOS = {
            "agua":        {"cor": (0.85, 0.95, 1.0),  "ior": 1.33, "roughness": 0.0, "alpha": 0.15},
            "mel":         {"cor": (0.9, 0.55, 0.05),  "ior": 1.48, "roughness": 0.05, "alpha": 0.7},
            "refrigerante":{"cor": (0.8, 0.15, 0.05),  "ior": 1.34, "roughness": 0.02, "alpha": 0.5},
            "leite":       {"cor": (0.95, 0.95, 0.92), "ior": 1.35, "roughness": 0.05, "alpha": 0.9},
            "vinho":       {"cor": (0.4, 0.05, 0.1),   "ior": 1.36, "roughness": 0.0, "alpha": 0.6},
            "lava":        {"cor": (1.0, 0.3, 0.0),    "ior": 1.5,  "roughness": 0.3, "alpha": 1.0},
        }

        config = TIPOS.get(tipo, TIPOS["agua"])
        if cor:
            config["cor"] = cor

        nome = self._nome(f"liquido_{tipo}", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat, nodes, links, bsdf, output = self._base_principled(nome)
        mat.blend_method = 'BLEND' if config["alpha"] < 0.9 else 'OPAQUE'

        bsdf.inputs['Base Color'].default_value = (*config["cor"], 1.0)
        bsdf.inputs['Roughness'].default_value = config["roughness"]
        bsdf.inputs['IOR'].default_value = config["ior"]
        bsdf.inputs['Transmission Weight'].default_value = 1.0 - config["alpha"]
        bsdf.inputs['Alpha'].default_value = config["alpha"]

        # Lava tem emissão
        if tipo == "lava":
            bsdf.inputs['Emission Color'].default_value = (1.0, 0.4, 0.0, 1.0)
            bsdf.inputs['Emission Strength'].default_value = 2.0

        return mat

    # ─────────────────────────────────────────────────────────────
    # CATEGORIA 4: ESPECIAIS (sci-fi, magia, tecnologia)
    # ─────────────────────────────────────────────────────────────

    def neon(self, cor=(0.0, 1.0, 0.8), intensidade=3.0,
             variacao="_01") -> bpy.types.Material:
        """
        Material neon/emissivo. Luz própria sem precisar de luz externa.
        Ideal para: hologramas, sinais, cyberpunk, sci-fi.
        """
        nome = self._nome("neon", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat, nodes, links, bsdf, output = self._base_principled(nome)

        bsdf.inputs['Base Color'].default_value = (*cor, 1.0)
        bsdf.inputs['Roughness'].default_value = 1.0
        bsdf.inputs['Metallic'].default_value = 0.0
        bsdf.inputs['Emission Color'].default_value = (*cor, 1.0)
        bsdf.inputs['Emission Strength'].default_value = intensidade

        return mat

    def holograma(self, cor=(0.1, 0.8, 1.0), opacidade=0.6,
                  variacao="_01") -> bpy.types.Material:
        """
        Holograma semi-transparente com scan lines.
        """
        nome = self._nome("holograma", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat = bpy.data.materials.new(nome)
        mat.use_nodes = True
        mat.blend_method = 'BLEND'
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Scan lines (linhas horizontais)
        tex_coord = nodes.new('ShaderNodeTexCoord')
        tex_coord.location = (-700, 0)

        wave = nodes.new('ShaderNodeTexWave')
        wave.location = (-500, 0)
        wave.wave_type = 'BANDS'
        wave.inputs['Scale'].default_value = 50.0
        wave.inputs['Distortion'].default_value = 0.0
        wave.inputs['Detail'].default_value = 0.0

        # Emissão com scan lines
        emission = nodes.new('ShaderNodeEmission')
        emission.location = (-100, 100)
        emission.inputs['Color'].default_value = (*cor, 1.0)
        emission.inputs['Strength'].default_value = 2.0

        transparent = nodes.new('ShaderNodeBsdfTransparent')
        transparent.location = (-100, -100)

        mix = nodes.new('ShaderNodeMixShader')
        mix.location = (150, 0)
        mix.inputs['Fac'].default_value = opacidade

        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (350, 0)

        links.new(transparent.outputs['BSDF'], mix.inputs[1])
        links.new(emission.outputs['Emission'], mix.inputs[2])
        links.new(mix.outputs['Shader'], output.inputs['Surface'])

        return mat

    def cristal(self, cor=(0.9, 0.95, 1.0), variacao="_01") -> bpy.types.Material:
        """Cristal com efeitos de dispersão (caustics requerem Cycles)."""
        nome = self._nome("cristal", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat, nodes, links, bsdf, output = self._base_principled(nome)
        mat.blend_method = 'BLEND'

        bsdf.inputs['Base Color'].default_value = (*cor, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.0
        bsdf.inputs['IOR'].default_value = 2.4  # Diamante
        bsdf.inputs['Transmission Weight'].default_value = 1.0
        bsdf.inputs['Alpha'].default_value = 0.1

        return mat

    # ─────────────────────────────────────────────────────────────
    # CATEGORIA 5: ESTILIZADOS (cartoon, toon, cel-shading)
    # ─────────────────────────────────────────────────────────────

    def cartoon(self, cor=(0.8, 0.3, 0.3), contorno=True,
                variacao="_01") -> bpy.types.Material:
        """
        Material cartoon / cel-shading.
        Cores planas sem gradiente físico. Ideal para animações.
        """
        nome = self._nome("cartoon", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat = bpy.data.materials.new(nome)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Difuso simples (cor plana)
        diffuse = nodes.new('ShaderNodeBsdfDiffuse')
        diffuse.location = (-100, 0)
        diffuse.inputs['Color'].default_value = (*cor, 1.0)
        diffuse.inputs['Roughness'].default_value = 1.0

        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (200, 0)
        links.new(diffuse.outputs['BSDF'], output.inputs['Surface'])

        return mat

    def toon_outline(self, cor=(0.05, 0.05, 0.05),
                     espessura=0.003) -> bpy.types.Material:
        """
        Material de contorno (para o efeito toon/cartoon outline).
        Aplicar em cópia do mesh com normals invertidas.
        """
        nome = self._nome("toon", "outline")
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat = bpy.data.materials.new(nome)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = (*cor, 1.0)
        emission.inputs['Strength'].default_value = 0.0

        output = nodes.new('ShaderNodeOutputMaterial')
        links.new(emission.outputs['Emission'], output.inputs['Surface'])

        mat.use_backface_culling = True

        return mat

    # ─────────────────────────────────────────────────────────────
    # CATEGORIA 6: CENÁRIO (fundos, chão, paredes)
    # ─────────────────────────────────────────────────────────────

    def fundo_studio(self, cor=(0.05, 0.05, 0.05),
                     variacao="_01") -> bpy.types.Material:
        """Fundo escuro para estúdio fotográfico/podcast."""
        nome = self._nome("fundo_studio", variacao)
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat, nodes, links, bsdf, output = self._base_principled(nome)
        bsdf.inputs['Base Color'].default_value = (*cor, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.9
        bsdf.inputs['Specular IOR Level'].default_value = 0.0

        return mat

    def tijolo(self, cor_tijolo=(0.55, 0.25, 0.15),
               cor_argamassa=(0.6, 0.58, 0.55)) -> bpy.types.Material:
        """Parede de tijolos procedural (sem imagem de textura)."""
        nome = self._nome("tijolo", "_01")
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat = bpy.data.materials.new(nome)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        # Brick texture nativa do Blender
        brick = nodes.new('ShaderNodeTexBrick')
        brick.location = (-300, 0)
        brick.inputs['Color1'].default_value = (*cor_tijolo, 1.0)
        brick.inputs['Color2'].default_value = (*cor_tijolo[:2], cor_tijolo[2] + 0.05, 1.0)
        brick.inputs['Mortar'].default_value = (*cor_argamassa, 1.0)
        brick.inputs['Scale'].default_value = 5.0
        brick.inputs['Mortar Size'].default_value = 0.02
        brick.inputs['Brick Width'].default_value = 0.5
        brick.inputs['Row Height'].default_value = 0.25

        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        bsdf.inputs['Roughness'].default_value = 0.9

        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (300, 0)

        links.new(brick.outputs['Color'], bsdf.inputs['Base Color'])
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

        return mat

    def gradiente_degrade(self, cor_topo=(0.02, 0.02, 0.08),
                           cor_base=(0.0, 0.0, 0.0)) -> bpy.types.Material:
        """Fundo degradê vertical — muito usado em comerciais modernos."""
        nome = self._nome("gradiente", "_01")
        if self._existe(nome):
            return bpy.data.materials[nome]

        mat = bpy.data.materials.new(nome)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        tex_coord = nodes.new('ShaderNodeTexCoord')
        tex_coord.location = (-600, 0)

        mapping = nodes.new('ShaderNodeMapping')
        mapping.location = (-400, 0)

        gradient = nodes.new('ShaderNodeTexGradient')
        gradient.location = (-200, 0)
        gradient.gradient_type = 'LINEAR'

        color_ramp = nodes.new('ShaderNodeValToRGB')
        color_ramp.location = (0, 0)
        color_ramp.color_ramp.elements[0].color = (*cor_base, 1.0)
        color_ramp.color_ramp.elements[1].color = (*cor_topo, 1.0)

        emission = nodes.new('ShaderNodeEmission')
        emission.location = (250, 0)

        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (450, 0)

        links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], gradient.inputs['Vector'])
        links.new(gradient.outputs['Color'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
        links.new(emission.outputs['Emission'], output.inputs['Surface'])

        return mat

    # ─────────────────────────────────────────────────────────────
    # PALETAS NARRATIVAS (Acesso rápido por nicho)
    # ─────────────────────────────────────────────────────────────

    def paleta(self, nicho: str) -> dict:
        """
        Retorna dicionário com cores da paleta narrativa do nicho.
        
        nicho: 'luxo' | 'saude' | 'tech' | 'natureza' | 
               'alimentos' | 'cosmos' | 'acao' | 'surreal'
        """
        PALETAS = {
            "luxo":      {"principal": (0.9, 0.7, 0.2),  "fundo": (0.02, 0.02, 0.02), "destaque": (1.0, 1.0, 0.9)},
            "saude":     {"principal": (0.0, 0.5, 0.7),  "fundo": (0.95, 0.98, 1.0),  "destaque": (0.0, 0.8, 0.5)},
            "tech":      {"principal": (0.0, 0.8, 1.0),  "fundo": (0.03, 0.03, 0.08), "destaque": (0.0, 1.0, 0.8)},
            "natureza":  {"principal": (0.3, 0.8, 0.1),  "fundo": (0.05, 0.15, 0.05), "destaque": (0.9, 0.7, 0.1)},
            "alimentos": {"principal": (0.9, 0.2, 0.05), "fundo": (0.02, 0.01, 0.01), "destaque": (1.0, 0.8, 0.0)},
            "cosmos":    {"principal": (0.5, 0.3, 1.0),  "fundo": (0.0, 0.0, 0.02),   "destaque": (1.0, 0.9, 0.4)},
            "acao":      {"principal": (0.8, 0.3, 0.0),  "fundo": (0.08, 0.06, 0.04), "destaque": (1.0, 0.9, 0.7)},
            "surreal":   {"principal": (0.0, 0.9, 0.9),  "fundo": (0.05, 0.0, 0.1),   "destaque": (1.0, 0.2, 0.5)},
        }
        return PALETAS.get(nicho, PALETAS["tech"])
