# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: scene_factory.py                                  ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝

Fábrica Universal de Cenários 3D. Interior, exterior, produto, sci-fi, surreal.

USO:
  import sys
  sys.path.append("D:/Blender/blenderscripts/scripts/utils")
  from materials_library import MaterialLibrary
  from scene_factory import SceneFactory

  lib = MaterialLibrary()
  scene_f = SceneFactory(lib)

  # Criar qualquer cenário:
  scene_f.criar("podcast_studio")
  scene_f.criar("product_studio", cor_fundo=(0.02, 0.02, 0.02))
  scene_f.criar("sci_fi_lab",  paleta="tech")
  scene_f.criar("city_night")
  scene_f.criar("nature_forest")
  scene_f.criar("medical_lab",  paleta="saude")

  # Adicionar props:
  scene_f.prop("mesa", posicao=(0, 0.5, 0))
  scene_f.prop("microfone", posicao=(-1, 0.5, 0.8))
"""

import bpy
import math
import os


class SceneFactory:
    """
    Fábrica Universal de Cenários do FGS Python 3D.
    
    Gera qualquer ambiente 3D automaticamente via parâmetros.
    Todos os cenários são modulares e reutilizáveis.
    """

    CENARIOS = {
        # Interior
        "podcast_studio":   "Interior: Estúdio de podcast com ring lights e sign ON AIR",
        "product_studio":   "Interior: Fundo infinito para produto/comercial",
        "office_modern":    "Interior: Escritório moderno corporativo",
        "medical_lab":      "Interior: Laboratório médico/científico",
        "kitchen_gourmet":  "Interior: Cozinha gourmet de chef",
        "classroom":        "Interior: Sala de aula futurista",
        # Exterior
        "city_night":       "Exterior: Cidade à noite com luzes neon",
        "nature_forest":    "Exterior: Floresta densa com luz filtrada",
        "desert_plain":     "Exterior: Planície deserta árida",
        "space_void":       "Especial: Espaço profundo com estrelas",
        # Abstrato
        "abstract_dark":    "Abstrato: Void escuro minimalista",
        "sci_fi_lab":       "Sci-Fi: Laboratório futurista holográfico",
        "surreal_world":    "Surreal: Mundo impossível com geometria estranha",
        "luxury_showroom":  "Luxury: Showroom de alto brilho com iluminação de palco",
        "cyberpunk_street": "Sci-Fi: Rua futurista com neon denso e volumetria",
    }

    def __init__(self, material_lib=None):
        self.lib = material_lib
        self.objetos = {}  # tipo → lista de objetos criados

    # ─────────────────────────────────────────────────────────────
    # API PRINCIPAL
    # ─────────────────────────────────────────────────────────────

    def criar(self, tipo: str, **kwargs) -> dict:
        """
        Cria um cenário completo pelo tipo.
        
        Args:
            tipo: Um dos cenários disponíveis (ver CENARIOS)
            **kwargs: Parâmetros específicos de cada cenário
        
        Returns:
            Dict com todos os objetos criados
        """
        print(f"\n🏗️  Criando cenário: {tipo}")
        descricao = self.CENARIOS.get(tipo, "Cenário customizado")
        print(f"   {descricao}")

        BUILDERS = {
            "podcast_studio":  self._build_podcast_studio,
            "product_studio":  self._build_product_studio,
            "office_modern":   self._build_office_modern,
            "medical_lab":     self._build_medical_lab,
            "kitchen_gourmet": self._build_kitchen_gourmet,
            "city_night":      self._build_city_night,
            "nature_forest":   self._build_nature_forest,
            "desert_plain":    self._build_desert_plain,
            "space_void":      self._build_space_void,
            "abstract_dark":   self._build_abstract_dark,
            "sci_fi_lab":      self._build_sci_fi_lab,
            "surreal_world":   self._build_surreal_world,
            "luxury_showroom": self._build_luxury_showroom,
            "cyberpunk_street":self._build_cyberpunk_street,
        }

        builder = BUILDERS.get(tipo)
        if builder:
            resultado = builder(**kwargs)
            print(f"   ✅ Cenário '{tipo}': {len(resultado)} objetos criados\n")
            return resultado
        else:
            print(f"   ❌ Tipo '{tipo}' não encontrado. Disponíveis: {list(BUILDERS.keys())}")
            return {}

    # ─────────────────────────────────────────────────────────────
    # UTILITÁRIOS INTERNOS
    # ─────────────────────────────────────────────────────────────

    def _cubo(self, nome, posicao, escala, cor=None) -> bpy.types.Object:
        bpy.ops.mesh.primitive_cube_add(size=1, location=posicao)
        obj = bpy.context.active_object
        obj.name = nome
        obj.scale = escala
        bpy.ops.object.transform_apply(scale=True)
        if cor and self.lib:
            mat = self.lib.fundo_studio(cor=cor)
            self.lib.aplicar(obj, mat)
        return obj

    def _plano(self, nome, posicao, escala, cor=None) -> bpy.types.Object:
        bpy.ops.mesh.primitive_plane_add(size=1, location=posicao)
        obj = bpy.context.active_object
        obj.name = nome
        obj.scale = (escala[0], escala[1], 1)
        bpy.ops.object.transform_apply(scale=True)
        if cor and self.lib:
            mat = self.lib.fundo_studio(cor=cor)
            self.lib.aplicar(obj, mat)
        return obj

    def _cilindro(self, nome, posicao, raio, altura, cor=None) -> bpy.types.Object:
        bpy.ops.mesh.primitive_cylinder_add(radius=raio, depth=altura, location=posicao)
        obj = bpy.context.active_object
        obj.name = nome
        if cor and self.lib:
            mat = self.lib.fundo_studio(cor=cor)
            self.lib.aplicar(obj, mat)
        return obj

    def _mat_simples(self, nome, cor, roughness=0.8, metallic=0.0):
        if bpy.data.materials.get(nome):
            return bpy.data.materials[nome]
        mat = bpy.data.materials.new(nome)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*cor, 1.0)
            bsdf.inputs['Roughness'].default_value = roughness
            bsdf.inputs['Metallic'].default_value = metallic
        return mat

    def _aplicar_mat(self, obj, mat):
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

    # ─────────────────────────────────────────────────────────────
    # CENÁRIOS INTERIORES
    # ─────────────────────────────────────────────────────────────

    def _build_podcast_studio(self,
                                largura=6.0, profundidade=5.0, altura=3.5,
                                cor_parede=(0.06, 0.06, 0.1),
                                cor_chao=(0.04, 0.04, 0.06), **kwargs) -> dict:
        """
        Estúdio de Podcast "The Den".
        Paredes escuras, mesa, cadeiras e sinal ON AIR.
        """
        objetos = {}

        # Estrutura base
        chao = self._plano("Studio_Chao", (0, 0, 0), (largura, profundidade),
                            cor=cor_chao)
        mat_chao = self._mat_simples("Mat_Chao", cor_chao, roughness=0.5, metallic=0.3)
        self._aplicar_mat(chao, mat_chao)
        objetos["chao"] = chao

        # Paredes
        for nome, pos, rot in [
            ("Studio_Parede_Fundo",  (0, profundidade / 2, altura / 2), (90, 0, 0)),
            ("Studio_Parede_Esq",    (-largura / 2, 0, altura / 2),      (90, 0, 90)),
            ("Studio_Parede_Dir",    (largura / 2, 0, altura / 2),       (90, 0, -90)),
        ]:
            wall = self._plano(nome, pos, (largura, altura))
            wall.rotation_euler = [math.radians(r) for r in rot]
            mat = self._mat_simples(f"Mat_{nome}", cor_parede, roughness=0.95)
            self._aplicar_mat(wall, mat)
            objetos[nome] = wall

        # Mesa do podcast
        mesa = self._cubo("Studio_Mesa", (0, 0.6, 0.45), (2.8, 0.9, 0.08))
        mat_mesa = self._mat_simples("Mat_Mesa", (0.12, 0.08, 0.06), roughness=0.3, metallic=0.3)
        self._aplicar_mat(mesa, mat_mesa)
        objetos["mesa"] = mesa

        # Pés da mesa
        for dx in [-1.2, 1.2]:
            pe = self._cubo(f"Studio_Mesa_Pe_{dx}", (dx, 0.6, 0.22), (0.06, 0.06, 0.44))
            self._aplicar_mat(pe, mat_mesa)

        # Sign ON AIR
        objetos.update(self._prop_onair_sign((0, 2.8, 2.8)))

        # Prateleira de fundo
        shelf = self._cubo("Studio_Shelf", (1.5, 2.4, 1.8), (1.2, 0.18, 0.04))
        mat_shelf = self._mat_simples("Mat_Shelf", (0.08, 0.05, 0.04), roughness=0.4)
        self._aplicar_mat(shelf, mat_shelf)
        objetos["shelf"] = shelf

        # Vasos e detalhes na prateleira
        for pos in [(1.2, 2.35, 2.0), (1.7, 2.35, 2.0)]:
            vaso = self._cilindro(f"Studio_Vaso_{pos[0]}", pos, 0.06, 0.18)
            mat_vaso = self._mat_simples(f"Mat_Vaso", (0.2, 0.4, 0.3), roughness=0.5)
            self._aplicar_mat(vaso, mat_vaso)

        # Tapete
        tapete = self._plano("Studio_Tapete", (0, 0.5, 0.002), (2.5, 2.0))
        mat_tapete = self._mat_simples("Mat_Tapete", (0.15, 0.1, 0.3), roughness=0.98)
        self._aplicar_mat(tapete, mat_tapete)
        objetos["tapete"] = tapete

        print(f"   📻 Podcast Studio 'The Den' criado | {largura}m x {profundidade}m")
        return objetos

    def _build_product_studio(self,
                                cor_fundo=(0.02, 0.02, 0.02),
                                tamanho=8.0,
                                tipo="escuro",  # 'escuro' | 'branco' | 'gradiente'
                                **kwargs) -> dict:
        """
        Fundo infinito (cyc) para fotografia e comercial de produto.
        O fundo curvo elimina horizonte visível.
        """
        objetos = {}

        if tipo == "branco":
            cor = (0.95, 0.95, 0.95)
        elif tipo == "gradiente":
            cor = (0.03, 0.03, 0.05)
        else:
            cor = cor_fundo

        # Chão
        chao = self._plano("Product_Chao", (0, 0, 0), (tamanho, tamanho))
        mat_chao = self._mat_simples("Mat_Product_Chao", cor, roughness=0.3, metallic=0.4)
        self._aplicar_mat(chao, mat_chao)
        objetos["chao"] = chao

        # Parede de fundo (cyc curvo simulado)
        fundo = self._plano("Product_Fundo", (0, tamanho / 2, tamanho / 2),
                             (tamanho, tamanho))
        fundo.rotation_euler = (math.radians(90), 0, 0)
        mat_fundo = self._mat_simples("Mat_Product_Fundo", cor, roughness=0.95)
        self._aplicar_mat(fundo, mat_fundo)
        objetos["fundo"] = fundo

        # Aplicar gradiente se solicitado
        if tipo == "gradiente" and self.lib:
            mat_grad = self.lib.gradiente_degrade(cor_base=(0.0, 0.0, 0.0), cor_topo=(0.04, 0.04, 0.08))
            self._aplicar_mat(fundo, mat_grad)

        print(f"   🎬 Product Studio: {tipo} | {tamanho}m")
        return objetos

    def _build_office_modern(self, largura=8.0, profundidade=6.0,
                               altura=3.0, **kwargs) -> dict:
        """Escritório moderno para vídeos corporativos e apresentações."""
        objetos = {}

        c_cinza = (0.55, 0.55, 0.58)
        c_chao = (0.18, 0.18, 0.2)

        chao = self._plano("Office_Chao", (0, 0, 0), (largura, profundidade))
        self._aplicar_mat(chao, self._mat_simples("Mat_Office_Chao", c_chao, 0.1, 0.5))
        objetos["chao"] = chao

        for nome, pos, rot in [
            ("Office_Parede_Fundo", (0, profundidade / 2, altura / 2), (90, 0, 0)),
        ]:
            wall = self._plano(nome, pos, (largura, altura))
            wall.rotation_euler = [math.radians(r) for r in rot]
            self._aplicar_mat(wall, self._mat_simples(f"Mat_{nome}", c_cinza))
            objetos[nome] = wall

        # Janela (retângulo brilhante)
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, profundidade / 2 - 0.01, altura * 0.6))
        janela = bpy.context.active_object
        janela.name = "Office_Janela"
        janela.scale = (3.0, 1, 1.5)
        bpy.ops.object.transform_apply(scale=True)
        janela.rotation_euler = (math.radians(90), 0, 0)
        mat_janela = self._mat_simples("Mat_Janela", (0.6, 0.8, 1.0))
        mat_janela.use_nodes = True
        emission = mat_janela.node_tree.nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = (0.7, 0.85, 1.0, 1.0)
        emission.inputs['Strength'].default_value = 2.5
        output = mat_janela.node_tree.nodes.get("Material Output")
        if output:
            mat_janela.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
        self._aplicar_mat(janela, mat_janela)
        objetos["janela"] = janela

        # Mesa de escritório
        mesa = self._cubo("Office_Mesa", (0, 0, 0.38), (2.2, 1.0, 0.06))
        self._aplicar_mat(mesa, self._mat_simples("Mat_Office_Mesa", (0.15, 0.1, 0.08), 0.2, 0.1))
        objetos["mesa"] = mesa

        return objetos

    def _build_medical_lab(self, **kwargs) -> dict:
        """Laboratório médico: branco clean, iluminação fria, equipamentos."""
        objetos = {}

        c_branco = (0.9, 0.92, 0.95)

        chao = self._plano("Med_Chao", (0, 0, 0), (8, 6))
        self._aplicar_mat(chao, self._mat_simples("Mat_Med_Chao", (0.85, 0.87, 0.9), 0.1, 0.2))
        objetos["chao"] = chao

        for nome, pos, rot in [
            ("Med_Parede_Fundo", (0, 3, 1.7), (90, 0, 0)),
            ("Med_Parede_Esq", (-4, 0, 1.7), (90, 0, 90)),
        ]:
            p = self._plano(nome, pos, (8, 3.5))
            p.rotation_euler = [math.radians(r) for r in rot]
            self._aplicar_mat(p, self._mat_simples(f"Mat_{nome}", c_branco, 0.85))
            objetos[nome] = p

        # Mesa de laboratório
        bancada = self._cubo("Med_Bancada", (0, 1.5, 0.45), (3.5, 0.8, 0.07))
        self._aplicar_mat(bancada, self._mat_simples("Mat_Bancada", (0.88, 0.90, 0.92), 0.15))
        objetos["bancada"] = bancada

        # Equipamentos simplificados
        monitor = self._cubo("Med_Monitor", (0.8, 1.3, 0.85), (0.5, 0.04, 0.4))
        self._aplicar_mat(monitor, self._mat_simples("Mat_Monitor", (0.05, 0.05, 0.08), 0.1, 0.5))
        objetos["monitor"] = monitor

        return objetos

    def _build_kitchen_gourmet(self, **kwargs) -> dict:
        """Cozinha gourmet para conteúdo gastronômico."""
        objetos = {}

        chao = self._plano("Kitchen_Chao", (0, 0, 0), (7, 5))
        self._aplicar_mat(chao, self._mat_simples("Mat_Kitchen_Chao", (0.25, 0.2, 0.15), 0.3, 0.2))
        objetos["chao"] = chao

        # Balcão
        balcao = self._cubo("Kitchen_Balcao", (0, 1, 0.45), (3.0, 0.85, 0.08))
        if self.lib:
            self._aplicar_mat(balcao, self.lib.madeira(cor_base=(0.35, 0.2, 0.1)))
        else:
            self._aplicar_mat(balcao, self._mat_simples("Mat_Balcao", (0.4, 0.22, 0.12), 0.3))
        objetos["balcao"] = balcao

        # Superfície de marmore
        tampo = self._cubo("Kitchen_Tampo", (0, 1, 0.5), (3.0, 0.85, 0.04))
        self._aplicar_mat(tampo, self._mat_simples("Mat_Tampo", (0.9, 0.88, 0.86), 0.1, 0.1))
        objetos["tampo"] = tampo

        return objetos

    # ─────────────────────────────────────────────────────────────
    # CENÁRIOS EXTERIORES
    # ─────────────────────────────────────────────────────────────

    def _build_city_night(self, extensao=30.0, **kwargs) -> dict:
        """Rua urbana à noite com edifícios e luzes."""
        objetos = {}

        # Rua
        rua = self._plano("City_Rua", (0, 0, 0), (extensao, extensao))
        self._aplicar_mat(rua, self._mat_simples("Mat_Rua", (0.08, 0.08, 0.1), 0.3, 0.4))
        objetos["rua"] = rua

        # Edifícios ao fundo
        alturas = [6, 9, 5, 11, 7, 8, 4, 10]
        for i, h in enumerate(alturas):
            x = -14 + i * 4
            predio = self._cubo(f"City_Predio_{i}", (x, 10, h / 2), (3.5, 2.5, h))
            cor = (0.1 + i * 0.03, 0.08 + i * 0.02, 0.12)
            self._aplicar_mat(predio, self._mat_simples(f"Mat_Predio_{i}", cor, 0.6, 0.3))
            objetos[f"predio_{i}"] = predio

            # Janelas iluminadas (cubo emissivo amarelo)
            janela = self._cubo(f"City_Janela_{i}", (x, 9.3, h * 0.5), (3.0, 0.1, h * 0.6))
            mat_j = bpy.data.materials.new(f"Mat_Janela_City_{i}")
            mat_j.use_nodes = True
            nodes = mat_j.node_tree.nodes
            links = mat_j.node_tree.links
            nodes.clear()
            noise = nodes.new('ShaderNodeTexNoise')
            noise.inputs['Scale'].default_value = 20.0
            ramp_j = nodes.new('ShaderNodeValToRGB')
            ramp_j.color_ramp.elements[0].color = (0, 0, 0, 1)
            ramp_j.color_ramp.elements[1].color = (0.9, 0.8, 0.4, 1)
            ramp_j.color_ramp.elements[0].position = 0.5
            emission = nodes.new('ShaderNodeEmission')
            emission.inputs['Strength'].default_value = 1.5
            output_j = nodes.new('ShaderNodeOutputMaterial')
            links.new(noise.outputs['Fac'], ramp_j.inputs['Fac'])
            links.new(ramp_j.outputs['Color'], emission.inputs['Color'])
            links.new(emission.outputs['Emission'], output_j.inputs['Surface'])
            self._aplicar_mat(janela, mat_j)

        return objetos

    def _build_nature_forest(self, num_arvores=15, **kwargs) -> dict:
        """Floresta densa com chão orgânico."""
        objetos = {}

        # Chão
        chao = self._plano("Forest_Chao", (0, 0, 0), (20, 20))
        self._aplicar_mat(chao, self._mat_simples("Mat_Forest_Chao", (0.12, 0.2, 0.08), 0.95))
        objetos["chao"] = chao

        # Árvores estilizadas
        import random as rnd
        rnd.seed(42)
        for i in range(num_arvores):
            x = rnd.uniform(-8, 8)
            y = rnd.uniform(1, 8)
            h_tronco = rnd.uniform(1.5, 3.5)
            r_copa = rnd.uniform(0.8, 1.8)

            # Tronco
            tronco = self._cilindro(f"Forest_Tronco_{i}", (x, y, h_tronco / 2),
                                    0.15 + rnd.uniform(0, 0.1), h_tronco)
            if self.lib:
                self._aplicar_mat(tronco, self.lib.madeira())
            else:
                self._aplicar_mat(tronco, self._mat_simples(f"Mat_Tronco_{i}", (0.3, 0.18, 0.1)))

            # Copa
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r_copa, location=(x, y, h_tronco + r_copa * 0.7))
            copa = bpy.context.active_object
            copa.name = f"Forest_Copa_{i}"
            copa.scale = (1.0, 0.9, rnd.uniform(0.8, 1.3))
            bpy.ops.object.transform_apply(scale=True)
            cor_copa = (rnd.uniform(0.1, 0.3), rnd.uniform(0.4, 0.7), rnd.uniform(0.1, 0.2))
            if self.lib:
                self._aplicar_mat(copa, self.lib.folha(cor=cor_copa))
            else:
                self._aplicar_mat(copa, self._mat_simples(f"Mat_Copa_{i}", cor_copa))
            objetos[f"arvore_{i}"] = copa

        return objetos

    def _build_desert_plain(self, **kwargs) -> dict:
        """Planície deserta árida."""
        objetos = {}
        chao = self._plano("Desert_Chao", (0, 0, 0), (40, 40))
        self._aplicar_mat(chao, self._mat_simples("Mat_Desert", (0.7, 0.55, 0.3), 0.9))
        objetos["chao"] = chao
        return objetos

    # ─────────────────────────────────────────────────────────────
    # CENÁRIOS ESPECIAIS
    # ─────────────────────────────────────────────────────────────

    def _build_space_void(self, **kwargs) -> dict:
        """Espaço profundo — esfera com estrelas internas."""
        objetos = {}
        # A câmera fica dentro desta esfera gigante
        bpy.ops.mesh.primitive_uv_sphere_add(radius=100, location=(0, 0, 0))
        esfera = bpy.context.active_object
        esfera.name = "Space_Esfera"
        esfera.scale = (-1, -1, -1)  # Normais para dentro

        mat = bpy.data.materials.new("Mat_Space_Stars")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        tex = nodes.new('ShaderNodeTexNoise')
        tex.inputs['Scale'].default_value = 200.0
        tex.inputs['Detail'].default_value = 6.0

        ramp = nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].color = (0, 0, 0.02, 1)
        ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
        ramp.color_ramp.elements[0].position = 0.85

        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Strength'].default_value = 2.0

        output = nodes.new('ShaderNodeOutputMaterial')
        links.new(tex.outputs['Fac'], ramp.inputs['Fac'])
        links.new(ramp.outputs['Color'], emission.inputs['Color'])
        links.new(emission.outputs['Emission'], output.inputs['Surface'])

        esfera.data.materials.append(mat)
        objetos["space_sphere"] = esfera
        return objetos

    def _build_abstract_dark(self, **kwargs) -> dict:
        """Fundo totalmente escuro — minimalista para foco no personagem/produto."""
        objetos = {}
        chao = self._plano("Dark_Chao", (0, 0, -0.01), (20, 20))
        self._aplicar_mat(chao, self._mat_simples("Mat_Dark_Chao", (0.01, 0.01, 0.01), 0.9))
        objetos["chao"] = chao
        return objetos

    def _build_sci_fi_lab(self, **kwargs) -> dict:
        """Laboratório sci-fi com hologramas e paredes metálicas."""
        objetos = {}

        chao = self._plano("SciFi_Chao", (0, 0, 0), (10, 8))
        self._aplicar_mat(chao, self._mat_simples("Mat_SciFi_Chao", (0.05, 0.05, 0.08), 0.1, 0.8))
        objetos["chao"] = chao

        # Grade emissiva no chão (grid lines)
        for i in range(-5, 6):
            linha = self._cubo(f"SciFi_Grid_H_{i}", (0, i, 0.005), (10, 0.02, 0.005))
            self._aplicar_mat(linha, self._mat_simples(f"Mat_Grid_{i}", (0.0, 0.5, 1.0), 0.0))

        # Paredes metálicas
        for nome, pos, escala in [
            ("SciFi_Parede_Fundo", (0, 4, 2), (10, 0.2, 4)),
            ("SciFi_Parede_Esq",  (-5, 0, 2), (0.2, 8, 4)),
        ]:
            p = self._cubo(nome, pos, escala)
            self._aplicar_mat(p, self._mat_simples(f"Mat_{nome}", (0.1, 0.12, 0.15), 0.2, 0.7))
            objetos[nome] = p

        return objetos

    def _build_surreal_world(self, **kwargs) -> dict:
        """Mundo surreal com geometria impossível."""
        objetos = {}
        import random as rnd
        rnd.seed(7)

        chao = self._plano("Surreal_Chao", (0, 0, 0), (20, 20))
        self._aplicar_mat(chao, self._mat_simples("Mat_Surreal_Chao", (0.02, 0.0, 0.05), 0.9))
        objetos["chao"] = chao

        # Formas flutuantes
        for i in range(12):
            x = rnd.uniform(-6, 6)
            y = rnd.uniform(-4, 8)
            z = rnd.uniform(0.5, 4)
            escala = rnd.uniform(0.3, 1.2)
            tipo_forma = rnd.choice(['SPHERE', 'CUBE', 'TORUS', 'CONE'])

            if tipo_forma == 'SPHERE':
                bpy.ops.mesh.primitive_uv_sphere_add(radius=escala * 0.5, location=(x, y, z))
            elif tipo_forma == 'CUBE':
                bpy.ops.mesh.primitive_cube_add(size=escala * 0.6, location=(x, y, z))
            elif tipo_forma == 'TORUS':
                bpy.ops.mesh.primitive_torus_add(major_radius=escala * 0.4, minor_radius=escala * 0.1, location=(x, y, z))
            elif tipo_forma == 'CONE':
                bpy.ops.mesh.primitive_cone_add(radius1=escala * 0.4, depth=escala * 0.8, location=(x, y, z))

            forma = bpy.context.active_object
            forma.name = f"Surreal_Forma_{i}"
            cor = (rnd.uniform(0.0, 0.5), rnd.uniform(0.5, 1.0), rnd.uniform(0.6, 1.0))
            mat = self._mat_simples(f"Mat_Surreal_{i}", cor)
            mat.use_nodes = True
            emission = mat.node_tree.nodes.new('ShaderNodeEmission')
            emission.inputs['Color'].default_value = (*cor, 1.0)
            emission.inputs['Strength'].default_value = rnd.uniform(0.5, 2.5)
            output_s = mat.node_tree.nodes.get("Material Output")
            if output_s:
                mat.node_tree.links.new(emission.outputs['Emission'], output_s.inputs['Surface'])
            self._aplicar_mat(forma, mat)

            # Rotação animada lenta
            bpy.context.scene.frame_set(1)
            forma.rotation_euler = (0, 0, 0)
            forma.keyframe_insert(data_path="rotation_euler")
            bpy.context.scene.frame_set(240)
            forma.rotation_euler = (math.radians(rnd.uniform(-180, 180)),
                                    math.radians(rnd.uniform(-180, 180)),
                                    math.radians(rnd.uniform(-180, 180)))
            forma.keyframe_insert(data_path="rotation_euler")

            objetos[f"forma_{i}"] = forma
        return objetos

    def _build_luxury_showroom(self, **kwargs) -> dict:
        """Showroom de luxo: piso reflexivo, pódio central e luzes de destaque."""
        objetos = {}
        
        # Piso de alto brilho
        chao = self._plano("Luxury_Chao", (0, 0, 0), (15, 15))
        self._aplicar_mat(chao, self._mat_simples("Mat_Luxury_Floor", (0.01, 0.01, 0.01), 0.05, 0.2))
        objetos["chao"] = chao
        
        # Pódio Central
        podio = self._cilindro("Luxury_Podio", (0, 0, 0.1), 3.0, 0.2)
        self._aplicar_mat(podio, self._mat_simples("Mat_Luxury_Podium", (0.05, 0.05, 0.05), 0.1, 0.8))
        objetos["podio"] = podio
        
        # Paredes laterais escuras (Vantagem do Void)
        fundo = self._plano("Luxury_Wall", (0, 6, 4), (15, 8))
        fundo.rotation_euler = (math.radians(90), 0, 0)
        self._aplicar_mat(fundo, self._mat_simples("Mat_Luxury_Wall", (0.005, 0.005, 0.005)))
        objetos["parede"] = fundo
        
        return objetos

    def _build_cyberpunk_street(self, **kwargs) -> dict:
        """Rua cyberpunk: Evolução do city_night com mais neon e volumetria."""
        objetos = self._build_city_night(extensao=40.0, **kwargs)
        
        import random as rnd
        rnd.seed(2077)
        
        # Adicionar letreiros neon aleatórios nas paredes dos prédios
        for i in range(5):
            x = -12 + i * 5
            z = rnd.uniform(2, 8)
            letreiro = self._cubo(f"Cyber_Neon_{i}", (x, 8.8, z), (1.5, 0.05, 0.6))
            cor = rnd.choice([(1, 0, 0.5), (0, 1, 1), (1, 0.5, 0)]) # Magenta, Ciano, Laranja
            mat_n = self._mat_simples(f"Mat_Cyber_Neon_{i}", cor, 0.0)
            mat_n.use_nodes = True
            nodes = mat_n.node_tree.nodes
            emission = nodes.get("Emission") or nodes.new('ShaderNodeEmission')
            emission.inputs['Color'].default_value = (*cor, 1.0)
            emission.inputs['Strength'].default_value = 10.0
            objetos[f"neon_{i}"] = letreiro
            self._aplicar_mat(letreiro, mat_n)
            
        return objetos

    # ─────────────────────────────────────────────────────────────
    # PROPS INDIVIDUAIS
    # ─────────────────────────────────────────────────────────────

    def _prop_onair_sign(self, posicao=(0, 2.8, 2.8)) -> dict:
        """Sign ON AIR luminoso — assinatura do Podcast Studio."""
        objetos = {}

        base = self._cubo("Sign_Base", posicao, (0.8, 0.06, 0.22))
        self._aplicar_mat(base, self._mat_simples("Mat_Sign_Base", (0.05, 0.05, 0.05), 0.5, 0.8))
        objetos["sign_base"] = base

        mat_sign = bpy.data.materials.new("Mat_Sign_ON_AIR")
        mat_sign.use_nodes = True
        nodes = mat_sign.node_tree.nodes
        links = mat_sign.node_tree.links
        nodes.clear()
        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = (1.0, 0.05, 0.02, 1.0)
        emission.inputs['Strength'].default_value = 4.0
        output = nodes.new('ShaderNodeOutputMaterial')
        links.new(emission.outputs['Emission'], output.inputs['Surface'])

        bpy.ops.mesh.primitive_cube_add(size=1,
                                        location=(posicao[0], posicao[1] - 0.04, posicao[2]))
        texto = bpy.context.active_object
        texto.name = "Sign_Light"
        texto.scale = (0.6, 0.02, 0.12)
        bpy.ops.object.transform_apply(scale=True)
        self._aplicar_mat(texto, mat_sign)
        objetos["sign_light"] = texto

        return objetos

    def prop(self, tipo: str, posicao=(0, 0, 0), escala=1.0) -> bpy.types.Object:
        """
        Adiciona um prop individual à cena.
        
        tipo: 'mesa' | 'cadeira' | 'microfone' | 'notebook' | 
              'garrafa' | 'planta' | 'livro' | 'lampada'
        """
        PROPS = {
            "mesa":       lambda: self._cubo("Prop_Mesa", posicao, (2.0 * escala, 0.8 * escala, 0.06)),
            "microfone":  lambda: self._cilindro("Prop_Mic_Base", posicao, 0.04 * escala, 0.5 * escala),
            "garrafa":    lambda: self._cilindro("Prop_Garrafa", posicao, 0.06 * escala, 0.28 * escala),
            "livro":      lambda: self._cubo("Prop_Livro", posicao, (0.22 * escala, 0.04, 0.3 * escala)),
        }

        builder = PROPS.get(tipo)
        if builder:
            obj = builder()
            print(f"   ✅ Prop '{tipo}' adicionado em {posicao}")
            return obj
        else:
            print(f"   ⚠️ Prop '{tipo}' não disponível")
            return None

    def listar_cenarios(self):
        print("\n🏗️  CENÁRIOS DISPONÍVEIS:")
        for nome, desc in self.CENARIOS.items():
            print(f"   '{nome}' → {desc}")
