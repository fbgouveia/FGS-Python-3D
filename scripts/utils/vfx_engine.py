# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: vfx_engine.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: vfx_engine.py                                     ║
║   Função: Motor de Efeitos Visuais Universal                 ║
║           Partículas, fluidos, fogo, energia, magia          ║
╚══════════════════════════════════════════════════════════════╝

USO:
  import sys
  sys.path.append("D:/Blender/blenderscripts/scripts/utils")
  from vfx_engine import VFXEngine

  vfx = VFXEngine()

  # Efeitos de partículas:
  vfx.glitter(objeto, quantidade=2000, cor=(1.0, 0.8, 0.2))
  vfx.neve(quantidade=5000)
  vfx.faiscas(objeto, velocidade=3.0)
  vfx.bolhas(objeto, raio=0.5)

  # Fluidos (Mantaflow):
  dominio, liquido = vfx.splash_liquido(
      posicao_gota=(0, 0, 1.5),
      cor_liquido=(0.8, 0.1, 0.0)   # Vermelho refrigerante
  )

  # Fogo e fumaça:
  vfx.fogo(objeto, intensidade=2.0)
  vfx.fumaca(objeto, densidade=0.5, cor=(0.3, 0.3, 0.3))
  vfx.explosao(posicao=(0, 0, 0.5), escala=2.0)

  # Sci-fi e energia:
  vfx.laser(inicio=(0,0,1), fim=(3,0,1), cor=(0,1,0))
  vfx.portal(posicao=(0,0,0), cor_interna=(0,0.8,1))
  vfx.holograma_particles(objeto)

  # Natureza:
  vfx.chuva(intensidade=1.0)
  vfx.vento_folhas(posicao=(0,0,0), quantidade=500)
"""

import bpy
import math
import random


class VFXEngine:
    """
    Motor Universal de Efeitos Visuais do FGS Python 3D.
    
    Abstrai a criação de sistemas de partículas, fluidos,
    fogo, fumaça e efeitos especiais em funções simples.
    """

    def __init__(self, fps=24):
        self.fps = fps
        self.sistemas = {}  # nome → objeto/sistema

    # ─────────────────────────────────────────────────────────────
    # UTILITÁRIOS INTERNOS
    # ─────────────────────────────────────────────────────────────

    def _ativar(self, obj):
        """Seleciona e ativa um objeto."""
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj

    def _criar_esfera(self, nome, posicao, raio=0.1) -> bpy.types.Object:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=raio, location=posicao)
        obj = bpy.context.active_object
        obj.name = nome
        return obj

    def _criar_material_emission(self, nome, cor, intensidade=3.0) -> bpy.types.Material:
        mat = bpy.data.materials.new(nome)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = (*cor, 1.0)
        emission.inputs['Strength'].default_value = intensidade

        output = nodes.new('ShaderNodeOutputMaterial')
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        return mat

    def _aplicar_mat(self, obj, mat):
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

    # ─────────────────────────────────────────────────────────────
    # CATEGORIA 1: PARTÍCULAS GENÉRICAS
    # ─────────────────────────────────────────────────────────────

    def _add_particle_system(self, obj, nome: str, configs: dict) -> bpy.types.ParticleSystem:
        """Adiciona sistema de partículas a um objeto com configurações completas."""
        self._ativar(obj)
        bpy.ops.object.particle_system_add()

        ps = obj.particle_systems[-1]
        ps.name = nome
        pset = ps.settings
        pset.name = f"{nome}_Settings"

        # Aplicar todas as configurações
        for attr, value in configs.items():
            try:
                setattr(pset, attr, value)
            except:
                pass  # Ignorar attrs não existentes silenciosamente

        return ps

    def glitter(self, objeto: bpy.types.Object = None,
                quantidade=3000, cor=(1.0, 0.8, 0.2),
                tamanho=0.015, velocidade=0.5,
                frame_inicio=1, frame_fim=120,
                nome="VFX_Glitter") -> bpy.types.ParticleSystem:
        """
        Chuva de glitter / confete dourado / brilhos.
        Ideal para: comemorações, comerciais de luxo, animações festivas.
        """
        if not objeto:
            bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, 2.5))
            objeto = bpy.context.active_object
            objeto.name = f"{nome}_Emitter"
            objeto.hide_render = False

        configs = {
            'count': quantidade,
            'lifetime': frame_fim - frame_inicio,
            'frame_start': frame_inicio,
            'frame_end': frame_fim * 0.3,  # Emite nos primeiros 30%
            'particle_size': tamanho,
            'size_random': 0.3,
            'normal_factor': 0.0,
            'factor_random': velocidade,
            'gravity': 0.3,
            'use_dynamic_rotation': True,
            'angular_velocity_mode': 'RAND',
            'angular_velocity_factor': 5.0,
            'render_type': 'OBJECT',  # Pode usar um mesh customizado
            'display_color': 'MATERIAL',
        }

        # Material da partícula
        mat = self._criar_material_emission(f"Mat_{nome}", cor, 3.0)
        objeto.data.materials.clear()
        objeto.data.materials.append(mat)

        ps = self._add_particle_system(objeto, nome, {'count': quantidade,
                                                        'lifetime': frame_fim,
                                                        'frame_start': frame_inicio,
                                                        'frame_end': frame_inicio + 30,
                                                        'particle_size': tamanho,
                                                        'size_random': 0.4,
                                                        'normal_factor': 0.5,
                                                        'factor_random': velocidade,
                                                        'gravity': 0.4,
                                                        'use_dynamic_rotation': True})

        self.sistemas[nome] = ps
        print(f"   ✅ VFX Glitter: {quantidade} partículas | cor={cor}")
        return ps

    def neve(self, quantidade=8000, area=8.0, velocidade_queda=0.5,
             tamanho=0.025, nome="VFX_Neve") -> bpy.types.ParticleSystem:
        """
        Sistema de neve caindo. Partículas leves e flutuantes.
        Ideal para: cenas de inverno, magia, fantasias.
        """
        bpy.ops.mesh.primitive_plane_add(size=area, location=(0, 0, 4))
        emitter = bpy.context.active_object
        emitter.name = f"{nome}_Emitter"

        ps = self._add_particle_system(emitter, nome, {
            'count': quantidade,
            'lifetime': 200,
            'frame_start': 1,
            'frame_end': 50,
            'particle_size': tamanho,
            'size_random': 0.5,
            'normal_factor': 0.0,
            'gravity': velocidade_queda,
            'use_dynamic_rotation': True,
            'angular_velocity_mode': 'RAND',
            'factor_random': 0.1,
        })

        mat_neve = self._criar_material_emission(f"Mat_{nome}", (0.95, 0.97, 1.0), 1.0)
        emitter.data.materials.append(mat_neve)

        self.sistemas[nome] = ps
        print(f"   ✅ VFX Neve: {quantidade} flocos | queda={velocidade_queda}")
        return ps

    def faiscas(self, objeto: bpy.types.Object = None,
                quantidade=500, velocidade=4.0,
                cor=(1.0, 0.7, 0.1), nome="VFX_Faiscas"):
        """
        Faíscas elétricas / centelhas / sparks.
        Ideal para: robôs, metal, eletricidade, explosões.
        """
        if not objeto:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0, 0, 0))
            objeto = bpy.context.active_object
            objeto.name = f"{nome}_Source"

        ps = self._add_particle_system(objeto, nome, {
            'count': quantidade,
            'lifetime': 40,
            'lifetime_random': 0.5,
            'frame_start': 1,
            'frame_end': 30,
            'particle_size': 0.02,
            'normal_factor': velocidade * 0.3,
            'factor_random': velocidade,
            'use_dynamic_rotation': True,
            'gravity': 0.8,
        })

        self.sistemas[nome] = ps
        print(f"   ✅ VFX Faísca: {quantidade} sparks")
        return ps

    def bolhas(self, objeto: bpy.types.Object = None,
               quantidade=300, raio_emissao=0.3,
               velocidade_sobe=1.0, nome="VFX_Bolhas"):
        """
        Bolhas subindo. Ideal para: bebidas, água, comemoração.
        """
        if not objeto:
            bpy.ops.mesh.primitive_cylinder_add(radius=raio_emissao, depth=0.1, location=(0, 0, 0))
            objeto = bpy.context.active_object
            objeto.name = f"{nome}_Emitter"

        ps = self._add_particle_system(objeto, nome, {
            'count': quantidade,
            'lifetime': 120,
            'frame_start': 1,
            'frame_end': 240,
            'particle_size': 0.04,
            'size_random': 0.6,
            'normal_factor': velocidade_sobe,
            'factor_random': 0.2,
            'gravity': -0.3,  # Sobe!
        })

        self.sistemas[nome] = ps
        print(f"   ✅ VFX Bolhas: {quantidade} bolhas | velocidade={velocidade_sobe}")
        return ps

    def estrelas_fundo(self, quantidade=5000, raio_esfera=50.0,
                       nome="VFX_Estrelas"):
        """
        Campo de estrelas para cenas cósmicas.
        Distribui pontos aleatórios em uma esfera gigante.
        """
        bpy.ops.mesh.primitive_uv_sphere_add(radius=raio_esfera, location=(0, 0, 0))
        esfera = bpy.context.active_object
        esfera.name = nome

        # Material emissivo branco com variação
        mat = bpy.data.materials.new(f"Mat_{nome}")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        noise = nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 100.0

        ramp = nodes.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
        ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
        ramp.color_ramp.elements[0].position = 0.7

        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Strength'].default_value = 1.0

        output = nodes.new('ShaderNodeOutputMaterial')
        links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
        links.new(ramp.outputs['Color'], emission.inputs['Color'])
        links.new(emission.outputs['Emission'], output.inputs['Surface'])

        esfera.data.materials.append(mat)

        # Virar normais para dentro
        esfera.scale = (-1, -1, -1)

        self.sistemas[nome] = esfera
        print(f"   ✅ VFX Estrelas: '{nome}' | raio={raio_esfera}")
        return esfera

    # ─────────────────────────────────────────────────────────────
    # CATEGORIA 2: FLUIDOS (Mantaflow)
    # ─────────────────────────────────────────────────────────────

    def splash_liquido(self, posicao_gota=(0, 0, 1.5),
                       tamanho_dominio=3.0,
                       cor_liquido=(0.8, 0.1, 0.05),
                       nome="VFX_Splash"):
        """
        Simulação de splash de líquido usando Mantaflow.
        Ideal para: comerciais de bebida, cenas de impacto com água.
        
        Returns:
            (dominio, inflow) — objetos do domínio e da fonte
        """
        # Domínio da simulação
        bpy.ops.mesh.primitive_cube_add(size=tamanho_dominio, location=(0, 0, 0))
        dominio = bpy.context.active_object
        dominio.name = f"{nome}_Dominio"

        bpy.ops.object.modifier_add(type='FLUID')
        dominio.modifiers['Fluid'].fluid_type = 'DOMAIN'
        dom_settings = dominio.modifiers['Fluid'].domain_settings
        dom_settings.domain_type = 'LIQUID'
        dom_settings.resolution_max = 64  # Alta resolução para splash
        dom_settings.use_mesh = True
        dom_settings.use_adaptive_domain = True

        # Material do líquido
        mat_liquido = bpy.data.materials.new(f"Mat_{nome}")
        mat_liquido.use_nodes = True
        bsdf = mat_liquido.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*cor_liquido, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.0
            bsdf.inputs['IOR'].default_value = 1.34
            bsdf.inputs['Transmission Weight'].default_value = 0.8
        dominio.data.materials.append(mat_liquido)

        # Gota (inflow)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=posicao_gota)
        gota = bpy.context.active_object
        gota.name = f"{nome}_Gota"

        bpy.ops.object.modifier_add(type='FLUID')
        gota.modifiers['Fluid'].fluid_type = 'FLOW'
        flow = gota.modifiers['Fluid'].flow_settings
        flow.flow_type = 'LIQUID'
        flow.flow_behavior = 'INFLOW'
        flow.use_initial_velocity = True
        flow.velocity_coord = (0, 0, -5)  # Velocidade de queda

        # Animação — gota cai
        bpy.context.scene.frame_set(1)
        gota.location = posicao_gota
        gota.keyframe_insert(data_path="location")

        bpy.context.scene.frame_set(30)
        gota.location = (posicao_gota[0], posicao_gota[1], 0)
        gota.keyframe_insert(data_path="location")

        # Coletor (chão)
        bpy.ops.mesh.primitive_cylinder_add(radius=tamanho_dominio * 0.6,
                                             depth=0.1, location=(0, 0, -tamanho_dominio / 2 + 0.1))
        chao = bpy.context.active_object
        chao.name = f"{nome}_Coletor"
        bpy.ops.object.modifier_add(type='FLUID')
        chao.modifiers['Fluid'].fluid_type = 'EFFECTOR'
        chao.modifiers['Fluid'].effector_settings.effector_type = 'COLLISION'

        print(f"   ✅ VFX Splash: domínio={tamanho_dominio}m | cor={cor_liquido}")
        print(f"   ⚠️  Bake necessário: Physics → Fluid → Bake Data")
        return dominio, gota

    # ─────────────────────────────────────────────────────────────
    # CATEGORIA 3: FOGO E FUMAÇA (Mantaflow Gas)
    # ─────────────────────────────────────────────────────────────

    def fogo(self, objeto: bpy.types.Object = None,
             escala=1.0, intensidade=2.0,
             frame_inicio=1, nome="VFX_Fogo"):
        """
        Simulação de fogo realista com Mantaflow.
        Ideal para: explosões, tochas, brasas, efeitos dramáticos.
        """
        if not objeto:
            bpy.ops.mesh.primitive_cylinder_add(radius=0.2 * escala, depth=0.05,
                                                location=(0, 0, 0))
            objeto = bpy.context.active_object
            objeto.name = f"{nome}_Source"

        # Domínio de gás
        dom_size = 2.0 * escala
        bpy.ops.mesh.primitive_cube_add(size=dom_size, location=(0, 0, dom_size / 2))
        dominio = bpy.context.active_object
        dominio.name = f"{nome}_Dominio"

        bpy.ops.object.modifier_add(type='FLUID')
        dominio.modifiers['Fluid'].fluid_type = 'DOMAIN'
        dom_s = dominio.modifiers['Fluid'].domain_settings
        dom_s.domain_type = 'GAS'
        dom_s.resolution_max = 128
        dom_s.use_noise = True

        # Material de fogo
        mat_fogo = bpy.data.materials.new(f"Mat_{nome}_Volume")
        mat_fogo.use_nodes = True
        nodes = mat_fogo.node_tree.nodes
        links = mat_fogo.node_tree.links
        nodes.clear()

        principled_vol = nodes.new('ShaderNodeVolumePrincipled')
        principled_vol.inputs['Color'].default_value = (1.0, 0.3, 0.0, 1.0)
        principled_vol.inputs['Emission Color'].default_value = (1.0, 0.5, 0.0, 1.0)
        principled_vol.inputs['Emission Strength'].default_value = intensidade
        principled_vol.inputs['Density'].default_value = 5.0

        output = nodes.new('ShaderNodeOutputMaterial')
        links.new(principled_vol.outputs['Volume'], output.inputs['Volume'])
        dominio.data.materials.append(mat_fogo)

        # Source (fogo)
        self._ativar(objeto)
        bpy.ops.object.modifier_add(type='FLUID')
        objeto.modifiers['Fluid'].fluid_type = 'FLOW'
        flow_s = objeto.modifiers['Fluid'].flow_settings
        flow_s.flow_type = 'FIRE'
        flow_s.flow_behavior = 'INFLOW'
        flow_s.use_initial_velocity = True
        flow_s.temperature = 1.0

        self.sistemas[nome] = dominio
        print(f"   ✅ VFX Fogo: escala={escala} | intensidade={intensidade}")
        print(f"   ⚠️  Bake necessário: Physics → Fluid → Bake Data")
        return dominio

    def fumaca(self, objeto: bpy.types.Object = None,
               densidade=0.5, cor=(0.3, 0.3, 0.3),
               escala=1.5, nome="VFX_Fumaca"):
        """
        Fumaça volumétrica realista.
        Ideal para: névoa, nuvens, mistério, cena de guerra.
        """
        if not objeto:
            bpy.ops.mesh.primitive_circle_add(radius=0.3 * escala, location=(0, 0, 0))
            objeto = bpy.context.active_object
            objeto.name = f"{nome}_Source"

        bpy.ops.mesh.primitive_cube_add(size=escala * 3, location=(0, 0, escala))
        dominio = bpy.context.active_object
        dominio.name = f"{nome}_Dominio"

        bpy.ops.object.modifier_add(type='FLUID')
        dominio.modifiers['Fluid'].fluid_type = 'DOMAIN'
        dom_s = dominio.modifiers['Fluid'].domain_settings
        dom_s.domain_type = 'GAS'
        dom_s.resolution_max = 64

        mat_fumaca = bpy.data.materials.new(f"Mat_{nome}")
        mat_fumaca.use_nodes = True
        nodes = mat_fumaca.node_tree.nodes
        links = mat_fumaca.node_tree.links
        nodes.clear()

        vol = nodes.new('ShaderNodeVolumePrincipled')
        vol.inputs['Color'].default_value = (*cor, 1.0)
        vol.inputs['Density'].default_value = densidade
        vol.inputs['Anisotropy'].default_value = 0.2

        output = nodes.new('ShaderNodeOutputMaterial')
        links.new(vol.outputs['Volume'], output.inputs['Volume'])
        dominio.data.materials.append(mat_fumaca)

        self._ativar(objeto)
        bpy.ops.object.modifier_add(type='FLUID')
        objeto.modifiers['Fluid'].fluid_type = 'FLOW'
        objeto.modifiers['Fluid'].flow_settings.flow_type = 'SMOKE'
        objeto.modifiers['Fluid'].flow_settings.flow_behavior = 'INFLOW'

        self.sistemas[nome] = dominio
        print(f"   ✅ VFX Fumaça: densidade={densidade} | cor={cor}")
        return dominio

    def explosao(self, posicao=(0, 0, 0), escala=2.0,
                 frame_pico=24, nome="VFX_Explosao"):
        """
        Explosão usando partículas + rigid body.
        Ideal para: ação, jogos, comerciais dramáticos.
        """
        # Esfera central que explode
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3 * escala, location=posicao)
        esfera = bpy.context.active_object
        esfera.name = f"{nome}_Core"

        # Partículas de debris
        ps = self._add_particle_system(esfera, nome, {
            'count': int(300 * escala),
            'lifetime': 60,
            'frame_start': frame_pico - 2,
            'frame_end': frame_pico + 2,
            'particle_size': 0.06 * escala,
            'normal_factor': 5.0 * escala,
            'factor_random': 2.0,
            'gravity': 1.0,
            'use_dynamic_rotation': True,
            'use_rotations': True,
        })

        # Material da explosão
        mat = self._criar_material_emission(f"Mat_{nome}", (1.0, 0.5, 0.1), 5.0)
        esfera.data.materials.append(mat)

        # Animar escala (expansão rápida)
        bpy.context.scene.frame_set(frame_pico - 2)
        esfera.scale = (0.1, 0.1, 0.1)
        esfera.keyframe_insert(data_path="scale")

        bpy.context.scene.frame_set(frame_pico)
        esfera.scale = (escala, escala, escala)
        esfera.keyframe_insert(data_path="scale")

        bpy.context.scene.frame_set(frame_pico + 12)
        esfera.scale = (0.01, 0.01, 0.01)
        esfera.keyframe_insert(data_path="scale")

        # Suavizar no pico, rápido no colapso
        if esfera.animation_data and esfera.animation_data.action:
            for fc in esfera.animation_data.action.fcurves:
                fc.keyframe_points[1].interpolation = 'EASE_IN'

        self.sistemas[nome] = esfera
        print(f"   ✅ VFX Explosão: posicao={posicao} | escala={escala} | frame={frame_pico}")
        return esfera

    # ─────────────────────────────────────────────────────────────
    # CATEGORIA 4: SCI-FI E ENERGIA
    # ─────────────────────────────────────────────────────────────

    def laser(self, inicio=(0, 0, 1), fim=(3, 0, 1),
              cor=(0.0, 1.0, 0.2), espessura=0.015,
              nome="VFX_Laser") -> bpy.types.Object:
        """
        Raio laser entre dois pontos.
        Ideal para: sci-fi, jogos, apresentações, hologramas.
        """
        from mathutils import Vector

        p1 = Vector(inicio)
        p2 = Vector(fim)
        comprimento = (p2 - p1).length
        centro = (p1 + p2) / 2

        bpy.ops.mesh.primitive_cylinder_add(radius=espessura, depth=comprimento, location=centro)
        laser = bpy.context.active_object
        laser.name = nome

        # Rotacionar para apontar do início ao fim
        direcao = (p2 - p1).normalized()
        eixo_z = Vector((0, 0, 1))
        if direcao != eixo_z and direcao != -eixo_z:
            angulo = eixo_z.angle(direcao)
            eixo = eixo_z.cross(direcao).normalized()
            laser.rotation_mode = 'AXIS_ANGLE'
            laser.rotation_axis_angle = (angulo, *eixo)

        mat = self._criar_material_emission(f"Mat_{nome}", cor, 8.0)
        laser.data.materials.append(mat)

        self.sistemas[nome] = laser
        print(f"   ✅ VFX Laser: {inicio} → {fim} | cor={cor}")
        return laser

    def portal(self, posicao=(0, 0, 0), raio=1.0,
               cor_interna=(0.0, 0.8, 1.0),
               cor_borda=(1.0, 0.3, 0.0),
               nome="VFX_Portal") -> bpy.types.Object:
        """
        Portal dimensional circular com efeito de energia.
        """
        # Borda do portal
        bpy.ops.mesh.primitive_torus_add(
            major_radius=raio, minor_radius=raio * 0.08,
            location=posicao
        )
        borda = bpy.context.active_object
        borda.name = f"{nome}_Borda"
        mat_borda = self._criar_material_emission(f"Mat_{nome}_Borda", cor_borda, 6.0)
        borda.data.materials.append(mat_borda)

        # Interior do portal
        bpy.ops.mesh.primitive_circle_add(radius=raio * 0.92, location=posicao)
        interior = bpy.context.active_object
        interior.name = f"{nome}_Interior"
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.fill()
        bpy.ops.object.mode_set(mode='OBJECT')

        mat_int = self._criar_material_emission(f"Mat_{nome}_Interior", cor_interna, 3.0)
        interior.data.materials.append(mat_int)

        # Partículas de energia ao redor
        self.glitter(borda, quantidade=500, cor=cor_borda, tamanho=0.02,
                     velocidade=1.5, nome=f"{nome}_Particles")

        self.sistemas[nome] = borda
        print(f"   ✅ VFX Portal: raio={raio} | cor={cor_interna}")
        return borda

    def holograma_scan(self, objeto: bpy.types.Object,
                       cor=(0.0, 0.8, 1.0),
                       frame_inicio=1, frame_fim=60,
                       nome="VFX_Scan"):
        """
        Efeito de scan/materialização holográfica num objeto.
        O objeto aparece linha por linha de baixo para cima.
        """
        mat_holo = bpy.data.materials.new(f"Mat_{nome}")
        mat_holo.use_nodes = True
        nodes = mat_holo.node_tree.nodes
        links = mat_holo.node_tree.links
        nodes.clear()

        # Usar posição Z para corte animado
        tex_coord = nodes.new('ShaderNodeTexCoord')
        separate = nodes.new('ShaderNodeSeparateXYZ')
        gt = nodes.new('ShaderNodeMath')
        gt.operation = 'GREATER_THAN'

        emission = nodes.new('ShaderNodeEmission')
        emission.inputs['Color'].default_value = (*cor, 1.0)
        emission.inputs['Strength'].default_value = 3.0

        transparent = nodes.new('ShaderNodeBsdfTransparent')
        mix = nodes.new('ShaderNodeMixShader')
        output = nodes.new('ShaderNodeOutputMaterial')

        links.new(tex_coord.outputs['Object'], separate.inputs['Vector'])
        links.new(separate.outputs['Z'], gt.inputs[0])
        links.new(gt.outputs['Value'], mix.inputs['Fac'])
        links.new(transparent.outputs['BSDF'], mix.inputs[1])
        links.new(emission.outputs['Emission'], mix.inputs[2])
        links.new(mix.outputs['Shader'], output.inputs['Surface'])

        mat_holo.blend_method = 'BLEND'
        objeto.data.materials.clear()
        objeto.data.materials.append(mat_holo)

        # Animar o threshold (corte animado)
        limiar = gt.inputs[1]
        bpy.context.scene.frame_set(frame_inicio)
        limiar.default_value = -2.0
        limiar.keyframe_insert(data_path="default_value")

        bpy.context.scene.frame_set(frame_fim)
        limiar.default_value = 2.0
        limiar.keyframe_insert(data_path="default_value")

        print(f"   ✅ VFX Holo Scan: {frame_inicio}→{frame_fim} | cor={cor}")

    # ─────────────────────────────────────────────────────────────
    # CATEGORIA 5: NATUREZA
    # ─────────────────────────────────────────────────────────────

    def chuva(self, intensidade=1.0, area=15.0,
              nome="VFX_Chuva") -> bpy.types.ParticleSystem:
        """
        Sistema de chuva caindo. Gotas lineares em alta velocidade.
        """
        bpy.ops.mesh.primitive_plane_add(size=area, location=(0, 0, 8))
        emitter = bpy.context.active_object
        emitter.name = f"{nome}_Emitter"

        ps = self._add_particle_system(emitter, nome, {
            'count': int(5000 * intensidade),
            'lifetime': 60,
            'frame_start': 1,
            'frame_end': 100,
            'particle_size': 0.01,
            'normal_factor': 0.0,
            'factor_random': 0.3,
            'gravity': 8.0,  # Cai rápido
            'length_tail': 0.5,
        })

        print(f"   ✅ VFX Chuva: intensidade={intensidade}x")
        return ps

    def vento_folhas(self, posicao=(0, 0, 0), quantidade=800,
                     cor=(0.3, 0.7, 0.2),
                     nome="VFX_Folhas"):
        """
        Folhas sendo carregadas pelo vento. Cenas de outono ou natureza.
        """
        bpy.ops.mesh.primitive_plane_add(size=8, location=(posicao[0], posicao[1], posicao[2] + 4))
        emitter = bpy.context.active_object
        emitter.name = f"{nome}_Emitter"

        ps = self._add_particle_system(emitter, nome, {
            'count': quantidade,
            'lifetime': 180,
            'frame_start': 1,
            'frame_end': 60,
            'particle_size': 0.05,
            'size_random': 0.6,
            'normal_factor': 0.0,
            'object_align_factor': (2.0, 0.5, -0.3),
            'use_dynamic_rotation': True,
            'angular_velocity_mode': 'RAND',
            'angular_velocity_factor': 3.0,
            'gravity': 0.4,
        })

        print(f"   ✅ VFX Folhas: {quantidade} folhas voando")
        return ps

    # ─────────────────────────────────────────────────────────────
    # UTILIDADES
    # ─────────────────────────────────────────────────────────────

    def listar_efeitos(self):
        print(f"\n✨ EFEITOS VFX ATIVOS ({len(self.sistemas)}):")
        for nome in self.sistemas.keys():
            print(f"   • {nome}")
