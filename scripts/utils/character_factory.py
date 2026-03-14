# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: character_factory.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: character_factory.py                              ║
║   Função: Fábrica Universal de Personagens 3D               ║
║           Qualquer tipo — animal, humano, criatura, abstrato ║
╚══════════════════════════════════════════════════════════════╝

USO:
  import sys
  sys.path.append("D:/Blender/blenderscripts/scripts/utils")
  from materials_library import MaterialLibrary
  from character_factory import CharacterFactory

  lib = MaterialLibrary()
  factory = CharacterFactory(lib)

  # Criar qualquer personagem:
  boomer = factory.criar(
      nome="Boomer",
      tipo="animal",
      especie="urso",
      posicao=(-1.0, 0, 0),
      estilo="cartoon",
      cor_corpo=(0.45, 0.28, 0.15),
      proporcao=1.0,           # 1.0=normal, 1.5=mais gordo, 0.8=mais esbelto
      humor="neutro"           # neutro | feliz | surpreso | bravo
  )

  lobo = factory.criar(
      nome="Max",
      tipo="animal",
      especie="lobo",
      posicao=(0, 0, 0),
      cor_corpo=(0.35, 0.35, 0.4),
      proporcao=0.9
  )

  cientista = factory.criar(
      nome="Dr_Ana",
      tipo="humano",
      posicao=(0, 0, 0),
      cor_pele=(0.85, 0.65, 0.5),
      estilo="cartoon",
      acessorio="jaleco"
  )
"""

import bpy
import math
from mathutils import Vector
from materials_library import MaterialLibrary



class IdentityPresets:
    """
    Conjunto de presets de identidade para personagens.
    """
    # Preset “MAESTRE_HERO” – o herói emblemático da série
    MAESTRE_HERO = {
        "nome": "Master Hero",
        "tipo": "humano",
        "especie": "humano_m",
        "posicao": (0, 0, 0),
        "estilo": "luxury",
        "cor_corpo": (0.85, 0.65, 0.5),
        "humor": "feliz",
        "proporcao": 1.35, # Proporção heróica (benchmark 1.35)
    }

    # Preset “LEAO_PREMIUM” – Realeza e Luxo
    LEAO_PREMIUM = {
        "nome": "Golden Lion",
        "tipo": "animal",
        "especie": "leao",
        "estilo": "luxury",
        "cor_corpo": (0.8, 0.5, 0.1), # Ouro/Bronze
        "humor": "bravo",
        "proporcao": 1.2,
    }

    # Preset “CIENTISTA” – Para vídeos educativos/médicos
    CIENTISTA = {
        "nome": "Dr. Nova",
        "tipo": "humano",
        "especie": "humano_f",
        "cor_corpo": (0.8, 0.6, 0.5),
        "acessorio": "jaleco",
        "humor": "neutro",
        "proporcao": 1.0,
    }

    # Preset “EXECUTIVO” – Corporativo
    EXECUTIVO = {
        "nome": "Director Smith",
        "tipo": "humano",
        "especie": "humano_m",
        "cor_corpo": (0.7, 0.5, 0.4),
        "acessorio": "oculos",
        "humor": "serio",
        "proporcao": 1.0,
    }

    # Preset “FAZENDA_VACA” – Estilo Fazenda
    FAZENDA_VACA = {
        "nome": "Clover",
        "tipo": "animal",
        "especie": "vaca",
        "cor_corpo": (0.9, 0.9, 0.9), # Branco com manchas (lógica de manchas pode ser expandida)
        "humor": "neutro",
        "proporcao": 1.1,
    }

    # Preset “FAZENDA_PORCO” – Estilo Fazenda
    FAZENDA_PORCO = {
        "nome": "Porky",
        "tipo": "animal",
        "especie": "porco",
        "cor_corpo": (0.95, 0.7, 0.75), # Rosa
        "humor": "feliz",
        "proporcao": 0.9,
    }


class CharacterFactory:
    """
    Fábrica Universal de Personagens do FGS Python 3D.
    
    Gera qualquer tipo de personagem 3D via parâmetros.
    Todos os personagens têm proporções consistentes e
    podem receber materiais, expressões e armature.
    """

    # Mapeamento de proporções por espécie
    ESPECIES = {
        # Animais grandes
        "urso":   {"corpo_escala": (1.0, 0.85, 1.1), "cabeca_ratio": 0.38, "orelha_tipo": "redonda", "focinho_tipo": "curto"},
        "gorila": {"corpo_escala": (1.1, 0.9, 1.0),  "cabeca_ratio": 0.35, "orelha_tipo": "redonda", "focinho_tipo": "chato"},
        # Animais médios
        "lobo":   {"corpo_escala": (0.85, 0.7, 1.05), "cabeca_ratio": 0.32, "orelha_tipo": "pontuda", "focinho_tipo": "longo"},
        "raposa": {"corpo_escala": (0.8, 0.65, 1.15), "cabeca_ratio": 0.30, "orelha_tipo": "pontuda", "focinho_tipo": "longo"},
        "leao":   {"corpo_escala": (1.0, 0.8, 1.0),  "cabeca_ratio": 0.40, "orelha_tipo": "redonda", "focinho_tipo": "medio"},
        "gato":   {"corpo_escala": (0.7, 0.6, 1.2),  "cabeca_ratio": 0.33, "orelha_tipo": "pontuda", "focinho_tipo": "curto"},
        "cachorro":{"corpo_escala": (0.85, 0.7, 1.0), "cabeca_ratio": 0.33, "orelha_tipo": "caida",   "focinho_tipo": "medio"},
        "coelho": {"corpo_escala": (0.75, 0.7, 1.1),  "cabeca_ratio": 0.32, "orelha_tipo": "longa",   "focinho_tipo": "curto"},
        "panda":  {"corpo_escala": (1.0, 0.85, 1.0),  "cabeca_ratio": 0.38, "orelha_tipo": "redonda", "focinho_tipo": "curto"},
        "aguia":  {"corpo_escala": (0.8, 0.65, 1.2),  "cabeca_ratio": 0.28, "orelha_tipo": "nenhuma", "focinho_tipo": "bico"},
        "vaca":   {"corpo_escala": (1.1, 0.9, 1.05),  "cabeca_ratio": 0.35, "orelha_tipo": "redonda", "focinho_tipo": "medio"},
        "porco":  {"corpo_escala": (0.9, 0.85, 0.95), "cabeca_ratio": 0.38, "orelha_tipo": "redonda", "focinho_tipo": "chato"},
        "pinguim":{"corpo_escala": (0.7, 0.6, 1.3),   "cabeca_ratio": 0.25, "orelha_tipo": "nenhuma", "focinho_tipo": "bico"},
        # Humanos (estilizados)
        "humano_m": {"corpo_escala": (0.9, 0.7, 1.25), "cabeca_ratio": 0.28, "orelha_tipo": "humana", "focinho_tipo": "humano"},
        "humano_f": {"corpo_escala": (0.82, 0.65, 1.3), "cabeca_ratio": 0.27, "orelha_tipo": "humana", "focinho_tipo": "humano"},
        # Criaturas
        "robo":   {"corpo_escala": (0.95, 0.8, 1.15), "cabeca_ratio": 0.33, "orelha_tipo": "antena",  "focinho_tipo": "grade"},
        "alien":  {"corpo_escala": (0.7, 0.6, 1.3),   "cabeca_ratio": 0.42, "orelha_tipo": "pontuda", "focinho_tipo": "curto"},
    }

    def __init__(self, material_lib=None):
        """
        Args:
            material_lib: Instância de MaterialLibrary (opcional)
        """
        # Garante que haja sempre uma MaterialLibrary
        self.lib = material_lib if material_lib is not None else MaterialLibrary()
        # Instância a coleção de presets
        self.presets = IdentityPresets()
        self.personagens = {}  # nome → dict com todos os objetos

    # ─────────────────────────────────────────────────────────────
    # API PRINCIPAL
    # ─────────────────────────────────────────────────────────────

    def criar(self, nome: str, tipo: str = "animal",
              especie: str = "urso", posicao=(0, 0, 0),
              estilo: str = "cartoon",
              cor_corpo=(0.45, 0.28, 0.15),
              cor_focinho=None, cor_olho=(0.05, 0.05, 0.05),
              proporcao: float = 1.0,
              humor: str = "neutro",
              acessorio: str = None,
              **kwargs) -> dict:
        """
        Cria um personagem completo.

        Args:
            nome:       Identificador único do personagem
            tipo:       'animal' | 'humano' | 'criatura' | 'abstrato'
            especie:    'urso' | 'raposa' | 'lobo' | 'humano_m' | etc.
            posicao:    Tupla XYZ de posição na cena
            estilo:     'cartoon' | 'semi-real' (afeta materiais)
            cor_corpo:  Cor principal RGB (0-1)
            cor_focinho:Cor do focinho/rosto (None = auto-derivada)
            cor_olho:   Cor das íris
            proporcao:  Multiplicador de escala geral (1.0 = padrão)
            humor:      'neutro' | 'feliz' | 'surpreso' | 'bravo'
            acessorio:  'oculos' | 'chapeu' | 'jaleco' | 'headphones' etc.

        Returns:
            dict com todos os objetos Blender criados pelo personagem
        """
        print(f"\n🎭 Criando personagem: {nome} ({especie})")

        x, y, z = posicao

        # Cor do focinho derivada automaticamente se não informada
        if cor_focinho is None:
            cor_focinho = tuple(min(1.0, c + 0.2) for c in cor_corpo)

        # Parâmetros da espécie
        spec = self.ESPECIES.get(especie, self.ESPECIES["urso"])
        cs = spec["corpo_escala"]
        cabeca_ratio = spec["cabeca_ratio"]
        orelha_tipo = spec["orelha_tipo"]
        focinho_tipo = spec["focinho_tipo"]

        # Escala geral
        p = proporcao
        objetos = {}

        # Construir personagem
        objetos.update(self._criar_corpo(nome, x, y, z, cs, p))
        objetos.update(self._criar_cabeca(nome, x, y, z, cabeca_ratio, p))
        objetos.update(self._criar_focinho(nome, x, y, z, focinho_tipo, cabeca_ratio, p))
        objetos.update(self._criar_olhos(nome, x, y, z, cabeca_ratio, p, cor_olho))
        objetos.update(self._criar_orelhas(nome, x, y, z, orelha_tipo, cabeca_ratio, p))
        objetos.update(self._criar_bracos(nome, x, y, z, p))

        # Aplicar materiais
        if self.lib:
            mat_corpo   = self.lib.pelo_animal(cor_base=cor_corpo, variacao=f"_{nome}")
            mat_focinho = self.lib.pele_estilizada(cor=cor_focinho, variacao=f"_focinho_{nome}")
        else:
            mat_corpo   = self._mat_simples(f"mat_{nome}_corpo", cor_corpo)
            mat_focinho = self._mat_simples(f"mat_{nome}_focinho", cor_focinho)

        mat_olho    = self._mat_simples(f"mat_{nome}_olho", cor_olho)
        mat_nariz   = self._mat_simples(f"mat_{nome}_nariz", (0.05, 0.03, 0.03))
        mat_brilho  = self._mat_simples(f"mat_brilho", (1.0, 1.0, 1.0))

        # Aplicar materiais em cada parte
        partes_corpo   = ['torso', 'cabeca', 'braco_esq', 'braco_dir',
                          'orelha_esq', 'orelha_dir']
        partes_focinho = ['focinho']
        partes_olho    = ['olho_esq', 'olho_dir']
        partes_nariz   = ['nariz']
        partes_brilho  = ['olho_brilho_esq', 'olho_brilho_dir']

        for parte in partes_corpo:
            if parte in objetos:
                self._aplicar_mat(objetos[parte], mat_corpo)
        for parte in partes_focinho:
            if parte in objetos:
                self._aplicar_mat(objetos[parte], mat_focinho)
        for parte in partes_olho:
            if parte in objetos:
                self._aplicar_mat(objetos[parte], mat_olho)
        for parte in partes_nariz:
            if parte in objetos:
                self._aplicar_mat(objetos[parte], mat_nariz)
        for parte in partes_brilho:
            if parte in objetos:
                self._aplicar_mat(objetos[parte], mat_brilho)

        # Adicionar acessório se solicitado
        if acessorio:
            objetos.update(self._adicionar_acessorio(nome, acessorio, x, y, z, cabeca_ratio, p))

        # Registrar personagem
        self.personagens[nome] = {
            "objetos": objetos,
            "posicao": posicao,
            "especie": especie,
            "proporcao": proporcao
        }

        print(f"   ✅ {nome}: {len(objetos)} partes criadas")
        return objetos

    def criar_preset(self, nome_preset: str, **kwargs) -> dict:
        """
        Cria um personagem a partir de um preset definido em IdentityPresets.
        
        Args:
            nome_preset: nome do preset (ex.: 'MAESTRE_HERO')
            **kwargs:   parâmetros que sobrescrevem ou acrescentam valores do preset
        
        Returns:
            dict – o mesmo formato retornado por criar
        """
        # Busca o preset na classe IdentityPresets
        preset_cls = self.presets
        
        # Normaliza o nome para maiúsculas (os presets são definidos em CAIXA-ALTA)
        key = nome_preset.upper()
        if not hasattr(preset_cls, key):
            raise ValueError(f"Preset '{nome_preset}' não encontrado.")
        
        # Copia o dicionário do preset e mescla com os kwargs recebidos
        preset_dict = getattr(preset_cls, key).copy()
        
        # Remover campos que não são argumentos de criar() se necessário
        # Mas aqui todos parecem compatíveis
        preset_dict.update(kwargs)
        
        # Ajuste de nome se não fornecido nos kwargs
        if "nome" not in kwargs:
            preset_dict["nome"] = f"{nome_preset}_{len(self.personagens) + 1}"

        return self.criar(**preset_dict)

    def criar_master_hero(self, posicao=(0, 0, 0), humor="feliz"):
        """
        Atalho rápido para criar o personagem Master Hero.
        
        Args:
            posicao:   tupla (x, y, z) – posição onde o personagem será criado
            humor:     expressão facial – "feliz" (padrão), "neutro", "surpreso", "bravo"
        
        Returns:
            dict – objetos do personagem recém-criado
        """
        return self.criar_preset(
            "MAESTRE_HERO",
            posicao=posicao,
            humor=humor
        )

    # ─────────────────────────────────────────────────────────────
    # BLOCOS DE CONSTRUÇÃO
    # ─────────────────────────────────────────────────────────────

    def _criar_corpo(self, nome, x, y, z, corpo_escala, p) -> dict:
        """Cria o torso do personagem."""
        cs = corpo_escala
        raio = 0.3 * p

        bpy.ops.mesh.primitive_uv_sphere_add(radius=raio, location=(x, y, z + raio))
        torso = bpy.context.active_object
        torso.name = f"{nome}_Torso"
        torso.scale = (cs[0] * p, cs[1] * p, cs[2] * p)
        bpy.ops.object.transform_apply(scale=True)

        return {"torso": torso}

    def _criar_cabeca(self, nome, x, y, z, cabeca_ratio, p) -> dict:
        """Cria a cabeça proporcionalmente ao body."""
        raio_cabeca = cabeca_ratio * p
        altura_cabeca = z + (0.3 * p * 2) + raio_cabeca * 0.85

        bpy.ops.mesh.primitive_uv_sphere_add(radius=raio_cabeca,
                                              location=(x, y, altura_cabeca))
        cabeca = bpy.context.active_object
        cabeca.name = f"{nome}_Cabeca"
        cabeca.scale = (1.0, 0.9, 1.05)
        bpy.ops.object.transform_apply(scale=True)

        return {"cabeca": cabeca, "_h_cabeca": altura_cabeca, "_r_cabeca": raio_cabeca}

    def _criar_focinho(self, nome, x, y, z, focinho_tipo, cabeca_ratio, p) -> dict:
        """Cria o focinho/nariz conforme o tipo da espécie."""
        h = z + (0.3 * p * 2) + cabeca_ratio * p * 0.85
        r = cabeca_ratio * p

        objetos = {}

        if focinho_tipo == "curto":
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.38, location=(x, y - r * 0.75, h - r * 0.08))
            focinho = bpy.context.active_object
            focinho.name = f"{nome}_Focinho"
            focinho.scale = (1.0, 0.65, 0.6)
            bpy.ops.object.transform_apply(scale=True)
            objetos["focinho"] = focinho

            # Nariz
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.1, location=(x, y - r * 1.1, h - r * 0.06))
            nariz = bpy.context.active_object
            nariz.name = f"{nome}_Nariz"
            nariz.scale = (1.0, 0.55, 0.75)
            bpy.ops.object.transform_apply(scale=True)
            objetos["nariz"] = nariz

        elif focinho_tipo == "longo":
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.38, location=(x, y - r * 0.8, h - r * 0.18))
            focinho = bpy.context.active_object
            focinho.name = f"{nome}_Focinho"
            focinho.scale = (0.72, 1.1, 0.52)  # Alongado
            bpy.ops.object.transform_apply(scale=True)
            objetos["focinho"] = focinho

            bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.09, location=(x, y - r * 1.05, h - r * 0.12))
            nariz = bpy.context.active_object
            nariz.name = f"{nome}_Nariz"
            nariz.scale = (1.0, 0.5, 0.65)
            bpy.ops.object.transform_apply(scale=True)
            objetos["nariz"] = nariz

        elif focinho_tipo in ("humano", "medio"):
            # Saliência sutil
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.2, location=(x, y - r * 0.85, h - r * 0.1))
            focinho = bpy.context.active_object
            focinho.name = f"{nome}_Focinho"
            focinho.scale = (1.0, 0.5, 0.7)
            bpy.ops.object.transform_apply(scale=True)
            objetos["focinho"] = focinho

            bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.07, location=(x, y - r * 0.95, h - r * 0.05))
            nariz = bpy.context.active_object
            nariz.name = f"{nome}_Nariz"
            objetos["nariz"] = nariz
            
        elif focinho_tipo == "chato":
            # Nariz de porco/gorila
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.35, location=(x, y - r * 0.7, h - r * 0.15))
            focinho = bpy.context.active_object
            focinho.name = f"{nome}_Focinho"
            focinho.scale = (1.1, 0.6, 0.75)
            bpy.ops.object.transform_apply(scale=True)
            objetos["focinho"] = focinho
            
            # Narinas sutilmente representadas
            for sinal in [-1, 1]:
                bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.06, location=(x + sinal * r * 0.1, y - r * 1.05, h - r * 0.15))
                narina = bpy.context.active_object
                narina.name = f"{nome}_Narina_{sinal}"
                objetos[f"narina_{sinal}"] = narina

        elif focinho_tipo == "bico":
            # Cone para pássaros
            bpy.ops.mesh.primitive_cone_add(radius1=r * 0.15, depth=r * 0.6, location=(x, y - r * 0.7, h - r * 0.1))
            bico = bpy.context.active_object
            bico.name = f"{nome}_Bico"
            bico.rotation_euler = (math.radians(-90), 0, 0)
            objetos["focinho"] = bico

        return objetos

    def _criar_olhos(self, nome, x, y, z, cabeca_ratio, p, cor_olho) -> dict:
        """Cria olhos com brilho."""
        h = z + (0.3 * p * 2) + cabeca_ratio * p * 0.85
        r = cabeca_ratio * p
        dx = r * 0.28
        dz = r * 0.08

        objetos = {}

        for lado, sinal in [("esq", -1), ("dir", 1)]:
            # Íris
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.16,
                                                  location=(x + sinal * dx, y - r * 0.55, h + dz))
            olho = bpy.context.active_object
            olho.name = f"{nome}_Olho_{lado.capitalize()}"
            olho.scale = (1.0, 0.55, 1.0)
            bpy.ops.object.transform_apply(scale=True)
            objetos[f"olho_{lado}"] = olho

            # Brilho (pequeno ponto branco — dá vida ao personagem)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.05,
                                                  location=(x + sinal * dx - r * 0.05,
                                                             y - r * 0.7, h + dz + r * 0.08))
            brilho = bpy.context.active_object
            brilho.name = f"{nome}_Olho_Brilho_{lado.capitalize()}"
            objetos[f"olho_brilho_{lado}"] = brilho

        return objetos

    def _criar_orelhas(self, nome, x, y, z, orelha_tipo, cabeca_ratio, p) -> dict:
        """Cria orelhas conforme o tipo."""
        h = z + (0.3 * p * 2) + cabeca_ratio * p * 0.85
        r = cabeca_ratio * p
        dx = r * 0.8

        objetos = {}

        for lado, sinal in [("esq", -1), ("dir", 1)]:
            pos = (x + sinal * dx, y, h + r * 0.75)

            if orelha_tipo == "redonda":
                bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.32, location=pos)
                orelha = bpy.context.active_object
                orelha.scale = (0.7, 0.5, 0.95)
                bpy.ops.object.transform_apply(scale=True)

            elif orelha_tipo == "pontuda":
                bpy.ops.mesh.primitive_cone_add(radius1=r * 0.28, depth=r * 0.7, location=pos)
                orelha = bpy.context.active_object

            elif orelha_tipo == "caida":
                bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.3,
                                                      location=(x + sinal * dx, y + r * 0.3, h + r * 0.4))
                orelha = bpy.context.active_object
                orelha.scale = (0.6, 0.4, 1.3)
                bpy.ops.object.transform_apply(scale=True)

            elif orelha_tipo == "longa":
                bpy.ops.mesh.primitive_cylinder_add(radius=r * 0.15, depth=r * 1.2, location=pos)
                orelha = bpy.context.active_object

            elif orelha_tipo == "humana":
                bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.2, location=pos)
                orelha = bpy.context.active_object
                orelha.scale = (0.35, 0.2, 0.55)
                bpy.ops.object.transform_apply(scale=True)

            elif orelha_tipo == "antena":
                bpy.ops.mesh.primitive_cylinder_add(radius=r * 0.06, depth=r * 0.8, location=pos)
                orelha = bpy.context.active_object
                orb_pos = (pos[0], pos[1], pos[2] + r * 0.5)
                bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 0.12, location=orb_pos)

            else:
                continue  # Sem orelha (bico, etc.)

            orelha.name = f"{nome}_Orelha_{lado.capitalize()}"
            objetos[f"orelha_{lado}"] = orelha

        return objetos

    def _criar_bracos(self, nome, x, y, z, p) -> dict:
        """Cria braços em posição de pose para podcast (cotovelos na mesa)."""
        objetos = {}
        z_braco = z + 0.45 * p

        for lado, sinal in [("esq", -1), ("dir", 1)]:
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.13 * p,
                                                  location=(x + sinal * 0.28 * p, y + 0.1 * p, z_braco))
            braco = bpy.context.active_object
            braco.name = f"{nome}_Braco_{lado.capitalize()}"
            braco.scale = (0.65, 1.4, 0.55)
            bpy.ops.object.transform_apply(scale=True)
            objetos[f"braco_{lado}"] = braco

        return objetos

    def _adicionar_acessorio(self, nome, acessorio, x, y, z, cabeca_ratio, p) -> dict:
        """Adiciona acessório ao personagem."""
        h = z + (0.3 * p * 2) + cabeca_ratio * p * 0.85
        r = cabeca_ratio * p
        objetos = {}

        if acessorio == "oculos":
            for sinal, lado in [(-1, "esq"), (1, "dir")]:
                bpy.ops.mesh.primitive_torus_add(
                    major_radius=r * 0.18, minor_radius=r * 0.03,
                    location=(x + sinal * r * 0.27, y - r * 0.5, h + r * 0.05)
                )
                lente = bpy.context.active_object
                lente.name = f"{nome}_Oculos_{lado}"
                lente.rotation_euler = (math.radians(90), 0, 0)
                objetos[f"oculos_{lado}"] = lente

        elif acessorio == "chapeu":
            bpy.ops.mesh.primitive_cylinder_add(radius=r * 0.65, depth=r * 0.1,
                                                location=(x, y, h + r * 0.9))
            aba = bpy.context.active_object
            aba.name = f"{nome}_Chapeu_Aba"
            objetos["chapeu_aba"] = aba

            bpy.ops.mesh.primitive_cylinder_add(radius=r * 0.4, depth=r * 0.55,
                                                location=(x, y, h + r * 1.2))
            copa = bpy.context.active_object
            copa.name = f"{nome}_Chapeu_Copa"
            objetos["chapeu_copa"] = copa

        elif acessorio == "headphones":
            bpy.ops.mesh.primitive_torus_add(
                major_radius=r * 0.85, minor_radius=r * 0.06,
                location=(x, y, h + r * 0.5)
            )
            headband = bpy.context.active_object
            headband.name = f"{nome}_Headphone_Band"
            headband.rotation_euler = (0, math.radians(90), 0)
            objetos["headphone_band"] = headband

        elif acessorio == "jaleco":
            # Jaleco branco (tira o material de corpo)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.32 * p, location=(x, y, z + 0.32 * p))
            jaleco = bpy.context.active_object
            jaleco.name = f"{nome}_Jaleco"
            jaleco.scale = (1.05, 0.8, 1.18)
            bpy.ops.object.transform_apply(scale=True)
            mat_jaleco = self._mat_simples(f"mat_jaleco_{nome}", (0.95, 0.95, 0.95))
            self._aplicar_mat(jaleco, mat_jaleco)
            objetos["jaleco"] = jaleco

        return objetos

    # ─────────────────────────────────────────────────────────────
    # ANIMAÇÃO
    # ─────────────────────────────────────────────────────────────

    def head_bob(self, nome: str, frame_inicio=1, frame_fim=240,
                 amplitude=0.03, frequencia=8):
        """
        Animação de balanço de cabeça (simula fala).
        Funciona para qualquer personagem registrado.
        """
        if nome not in self.personagens:
            print(f"⚠️ Personagem '{nome}' não encontrado")
            return

        cabeca = self.personagens[nome]["objetos"].get("cabeca")
        if not cabeca:
            return

        pos_base = cabeca.location.z

        for f in range(frame_inicio, frame_fim, frequencia):
            bpy.context.scene.frame_set(f)
            cabeca.location.z = pos_base
            cabeca.keyframe_insert(data_path="location", index=2)

            bpy.context.scene.frame_set(f + frequencia // 2)
            cabeca.location.z = pos_base + amplitude
            cabeca.keyframe_insert(data_path="location", index=2)

        # Suavizar
        if cabeca.animation_data and cabeca.animation_data.action:
            for fc in cabeca.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = 'SINE'

        print(f"   ✅ Head bob aplicado: {nome}")

    def inclinacao(self, nome: str, angulo_graus=-10,
                   frames=(1, 24), suave=True):
        """
        Inclina o torso do personagem (ceticismo, surpresa, ênfase).
        angulo_graus negativo = inclina para trás.
        """
        if nome not in self.personagens:
            return
        torso = self.personagens[nome]["objetos"].get("torso")
        if not torso:
            return

        bpy.context.scene.frame_set(frames[0])
        torso.rotation_euler.x = 0
        torso.keyframe_insert(data_path="rotation_euler", index=0)

        bpy.context.scene.frame_set(frames[1])
        torso.rotation_euler.x = math.radians(angulo_graus)
        torso.keyframe_insert(data_path="rotation_euler", index=0)

    def risada(self, nome: str, frame_inicio=480, duracao=60):
        """Animação de risada — balanço rápido de cabeça e torso."""
        if nome not in self.personagens:
            return

        cabeca = self.personagens[nome]["objetos"].get("cabeca")
        torso  = self.personagens[nome]["objetos"].get("torso")

        if not cabeca:
            return

        pos_z_base = cabeca.location.z

        for i, f in enumerate(range(frame_inicio, frame_inicio + duracao, 4)):
            bpy.context.scene.frame_set(f)
            cabeca.location.z = pos_z_base + math.sin(i * 0.8) * 0.07
            cabeca.keyframe_insert(data_path="location", index=2)

            if torso:
                torso.rotation_euler.x = math.radians(math.sin(i * 0.6) * 5)
                torso.keyframe_insert(data_path="rotation_euler", index=0)

    # ─────────────────────────────────────────────────────────────
    # PRESETS RÁPIDOS
    # ─────────────────────────────────────────────────────────────

    def criar_boomer(self, posicao=(-1.0, 0.8, 0.5)) -> dict:
        """Cria o personagem Boomer (urso) com configurações padrão da série."""
        return self.criar(
            nome="Boomer",
            tipo="animal",
            especie="urso",
            posicao=posicao,
            cor_corpo=(0.45, 0.28, 0.15),
            cor_focinho=(0.65, 0.45, 0.28),
            cor_olho=(0.12, 0.07, 0.04),
            proporcao=1.0,
            acessorio=None
        )

    def criar_kev(self, posicao=(1.0, 0.8, 0.5)) -> dict:
        """Cria o personagem Kev (raposa) com configurações padrão da série."""
        return self.criar(
            nome="Kev",
            tipo="animal",
            especie="raposa",
            posicao=posicao,
            cor_corpo=(0.85, 0.35, 0.08),
            cor_focinho=(0.95, 0.85, 0.75),
            cor_olho=(0.05, 0.4, 0.1),
            proporcao=0.88,
            acessorio=None
        )

    # ─────────────────────────────────────────────────────────────
    # UTILITÁRIOS
    # ─────────────────────────────────────────────────────────────

    def _mat_simples(self, nome, cor) -> bpy.types.Material:
        """Cria material simples sem MaterialLibrary."""
        if bpy.data.materials.get(nome):
            return bpy.data.materials[nome]
        mat = bpy.data.materials.new(nome)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (*cor, 1.0)
            bsdf.inputs['Roughness'].default_value = 0.8
        return mat

    def _aplicar_mat(self, obj, mat):
        if not obj or not mat:
            return
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

    def listar_personagens(self):
        print(f"\n🎭 PERSONAGENS CRIADOS ({len(self.personagens)}):")
        for nome, dados in self.personagens.items():
            print(f"   {nome} | {dados['especie']} | {len(dados['objetos'])} partes")
