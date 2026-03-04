"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: lighting_system.py                                ║
║   Função: Sistema Universal de Iluminação Cinematográfica   ║
║           8 presets narrativos + iluminação customizável    ║
╚══════════════════════════════════════════════════════════════╝

USO:
  import sys
  sys.path.append("D:/Blender/blenderscripts/scripts/utils")
  from lighting_system import LightingSystem

  luzes = LightingSystem()

  # Usar um preset completo:
  luzes.preset("luxo")      # Preto + dourado — comerciais premium
  luzes.preset("saude")     # Azul/branco — medicina, bem-estar
  luzes.preset("tech")      # Neon escuro — tecnologia
  luzes.preset("podcast")   # Ring lights — talk shows

  # Ou criar iluminação customizada:
  luzes.key("Minha_Key", posicao=(-2,3,4), energia=100, cor=(1,0.9,0.8))
  luzes.fill("Minha_Fill", posicao=(2,2,3), energia=40)
  luzes.rim("Meu_Rim", posicao=(0,-2,3), energia=80)
"""

import bpy
import math


class LightingSystem:
    """
    Sistema Universal de Iluminação do FGS Python 3D.
    
    Abstrai a configuração de iluminação cinematográfica em
    funções simples com presets prontos para cada nicho.
    """

    def __init__(self):
        self.luzes = {}  # nome → objeto luz

    # ─────────────────────────────────────────────────────────────
    # CRIAÇÃO DE LUZES INDIVIDUAIS
    # ─────────────────────────────────────────────────────────────

    def _criar_luz(self, nome: str, tipo: str, posicao: tuple,
                   energia: float, cor=(1.0, 1.0, 1.0),
                   tamanho=1.0, sombra=True) -> bpy.types.Object:
        """Cria uma luz genérica. Uso interno."""

        tipo_blender = {
            'area': 'AREA',
            'ponto': 'POINT',
            'sol': 'SUN',
            'spot': 'SPOT'
        }.get(tipo, 'AREA')

        bpy.ops.object.light_add(type=tipo_blender, location=posicao)
        luz = bpy.context.active_object
        luz.name = nome
        luz.data.energy = energia
        luz.data.color = cor
        luz.data.use_shadow = sombra

        if tipo == 'area':
            luz.data.size = tamanho
        elif tipo == 'ponto':
            luz.data.shadow_soft_size = tamanho
        elif tipo == 'spot':
            luz.data.spot_size = math.radians(45)
            luz.data.spot_blend = 0.15

        self.luzes[nome] = luz
        return luz

    def key(self, nome="Key_Light", posicao=(-2, 3, 4),
            energia=80, cor=(1.0, 0.97, 0.9), tamanho=1.0) -> bpy.types.Object:
        """
        Key Light — luz principal. A mais importante da cena.
        Define a direção predominante da iluminação.
        
        Posição recomendada: 45° lateral + 45° acima do sujeito.
        Cor quente (1.0, 0.97, 0.9) = luz do dia / estúdio profissional.
        """
        luz = self._criar_luz(nome, 'area', posicao, energia, cor, tamanho)
        # Apontar para a origem
        luz.rotation_euler = (math.radians(55), 0, math.radians(-35))
        print(f"   💡 Key: {nome} | {energia}W | {cor}")
        return luz

    def fill(self, nome="Fill_Light", posicao=(3, 2, 2),
             energia=30, cor=(0.85, 0.9, 1.0), tamanho=2.0) -> bpy.types.Object:
        """
        Fill Light — preenchimento das sombras.
        Energia menor que a Key (razão 1:3 a 1:8).
        Cor levemente azulada (complementa a key quente).
        """
        luz = self._criar_luz(nome, 'area', posicao, energia, cor, tamanho)
        luz.rotation_euler = (math.radians(40), 0, math.radians(35))
        print(f"   💡 Fill: {nome} | {energia}W | suave")
        return luz

    def rim(self, nome="Rim_Light", posicao=(0, -3, 3),
            energia=60, cor=(0.9, 0.95, 1.0), tamanho=0.5) -> bpy.types.Object:
        """
        Rim Light — contorno. Separa o sujeito do fundo.
        Posição: atrás e acima do sujeito.
        Cor mais fria que a key para contraste.
        """
        luz = self._criar_luz(nome, 'area', posicao, energia, cor, tamanho)
        luz.rotation_euler = (math.radians(-50), 0, 0)
        print(f"   💡 Rim: {nome} | {energia}W | contorno")
        return luz

    def ambiente(self, nome="BG_Light", posicao=(0, 0, 5),
                 energia=10, cor=(0.7, 0.8, 1.0), tamanho=10.0) -> bpy.types.Object:
        """
        Luz de ambiente geral. Elimina sombras duras indesejadas.
        Area light grande e suave, acima da cena.
        """
        luz = self._criar_luz(nome, 'area', posicao, energia, cor, tamanho)
        luz.rotation_euler = (math.radians(90), 0, 0)
        return luz

    def ring_light(self, nome="Ring", posicao=(0, 1.5, 1.5),
                   energia=50, cor=(0.9, 0.87, 0.8),
                   tamanho=0.7) -> bpy.types.Object:
        """
        Ring Light — assinatura visual de podcasts e criadores.
        Cria reflexo característico circular nos olhos.
        """
        luz = self._criar_luz(nome, 'area', posicao, energia, cor, tamanho)
        luz.rotation_euler = (math.radians(-20), 0, 0)
        luz.data.shape = 'DISK'  # Circular
        print(f"   💡 Ring: {nome} | {cor}")
        return luz

    def sol(self, nome="Sol", rotacao=(math.radians(55), 0, math.radians(45)),
            energia=3.0, cor=(1.0, 0.95, 0.85)) -> bpy.types.Object:
        """Luz solar direcional para cenas externas."""
        bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
        luz = bpy.context.active_object
        luz.name = nome
        luz.data.energy = energia
        luz.data.color = cor
        luz.rotation_euler = rotacao
        self.luzes[nome] = luz
        return luz

    def ponto_emissivo(self, nome="Point", posicao=(0, 0, 3),
                       energia=100, cor=(1.0, 0.6, 0.1),
                       raio=0.1) -> bpy.types.Object:
        """Ponto de luz — explosão, lâmpada, partícula de energia."""
        return self._criar_luz(nome, 'ponto', posicao, energia, cor, raio)

    # ─────────────────────────────────────────────────────────────
    # PRESETS NARRATIVOS COMPLETOS
    # ─────────────────────────────────────────────────────────────

    def preset(self, nicho: str, **kwargs):
        """
        Aplica um preset de iluminação completo por nicho narrativo.
        
        nicho: 'luxo' | 'saude' | 'tech' | 'natureza' | 'alimentos' | 
               'cosmos' | 'acao' | 'surreal' | 'podcast' | 'produto'
               'exterior_dia' | 'exterior_noite' | 'drama' | 'horror'
        """
        presets = {
            "luxo":          self._preset_luxo,
            "saude":         self._preset_saude,
            "tech":          self._preset_tech,
            "natureza":      self._preset_natureza,
            "alimentos":     self._preset_alimentos,
            "cosmos":        self._preset_cosmos,
            "acao":          self._preset_acao,
            "surreal":       self._preset_surreal,
            "podcast":       self._preset_podcast,
            "produto":       self._preset_produto,
            "exterior_dia":  self._preset_exterior_dia,
            "exterior_noite":self._preset_exterior_noite,
            "drama":         self._preset_drama,
            "horror":        self._preset_horror,
        }

        func = presets.get(nicho)
        if func:
            print(f"\n💡 ILUMINAÇÃO: Preset '{nicho}'")
            func(**kwargs)
            print(f"   {len(self.luzes)} luzes criadas\n")
        else:
            print(f"⚠️ Preset '{nicho}' não encontrado. Disponíveis: {list(presets.keys())}")

    def _preset_luxo(self, **kwargs):
        """Preto + dourado. Comerciais premium, relógios, perfumes, joias."""
        self.key("Key_Luxo", posicao=(-2.5, 2, 4),   energia=100, cor=(1.0, 0.88, 0.6))
        self.fill("Fill_Luxo", posicao=(3, 2, 2),      energia=20,  cor=(0.7, 0.7, 0.8))
        self.rim("Rim_Luxo",  posicao=(0.5, -2.5, 3), energia=90,  cor=(1.0, 0.9, 0.6))
        # Destaque de baixo (glamour light)
        self._criar_luz("Glamour_Luxo", 'area', (0, 0.5, -0.5), 30, (1.0, 0.85, 0.5), 0.5)
        self._setup_world((0.01, 0.01, 0.01))

    def _preset_saude(self, **kwargs):
        """Branco + azul claro. Medicina, farmácia, bem-estar, fitness."""
        self.key("Key_Saude", posicao=(-2, 3, 4),   energia=80,  cor=(0.95, 0.97, 1.0))
        self.fill("Fill_Saude", posicao=(3, 2, 3),   energia=50,  cor=(0.9, 0.95, 1.0))
        self.rim("Rim_Saude", posicao=(0, -2, 2.5),  energia=40,  cor=(0.7, 0.9, 1.0))
        self.ambiente("Amb_Saude", energia=20, cor=(0.9, 0.95, 1.0))
        self._setup_world((0.8, 0.9, 1.0), strength=0.5)

    def _preset_tech(self, **kwargs):
        """Escuro + cian neon. Tecnologia, IA, games, cyberpunk."""
        self.key("Key_Tech", posicao=(-2, 2.5, 3),  energia=60,  cor=(0.0, 0.8, 1.0))
        self.fill("Fill_Tech", posicao=(3, 1.5, 2),  energia=15,  cor=(0.0, 0.4, 0.8))
        self.rim("Rim_Tech", posicao=(0, -2, 3),     energia=80,  cor=(0.0, 1.0, 0.8))
        # Luz de chão neon
        self._criar_luz("Floor_Tech", 'area', (0, 0, -0.3), 20, (0.0, 0.5, 1.0), 3.0)
        self._setup_world((0.02, 0.02, 0.05))

    def _preset_natureza(self, **kwargs):
        """Verde + amber. Natureza, sustentabilidade, orgânicos, saúde natural."""
        self.sol("Sol_Natureza", rotacao=(math.radians(60), 0, math.radians(30)),
                 energia=2.5, cor=(1.0, 0.95, 0.8))
        self.fill("Fill_Natureza", posicao=(3, 2, 3), energia=30, cor=(0.6, 0.9, 0.5))
        self.ambiente("Amb_Natureza", energia=15, cor=(0.6, 0.85, 0.5))
        self._setup_world((0.3, 0.6, 0.3), strength=0.4)

    def _preset_alimentos(self, **kwargs):
        """Quente + vibrante. Gastronomia, bebidas, restaurantes, delivery."""
        self.key("Key_Food", posicao=(-2, 2, 4),   energia=100, cor=(1.0, 0.88, 0.7))
        self.fill("Fill_Food", posicao=(2, 1.5, 2), energia=40,  cor=(1.0, 0.9, 0.8))
        self.rim("Rim_Food", posicao=(0, -2, 3),    energia=70,  cor=(1.0, 0.7, 0.3))
        # Destaque underlight (mesa brilhante)
        self._criar_luz("Under_Food", 'area', (0, 0.5, 0.1), 25, (0.9, 0.7, 0.4), 1.5)
        self._setup_world((0.05, 0.03, 0.02))

    def _preset_cosmos(self, **kwargs):
        """Preto + nebulosa. Espaço, astronomia, sci-fi, documentários."""
        # Luz estelar distante suave
        self._criar_luz("Star_Key", 'area', (-5, 3, 5), 40, (0.8, 0.85, 1.0), 0.3)
        self._criar_luz("Nebula_Fill", 'area', (4, 2, 2), 15, (0.4, 0.1, 0.8), 5.0)
        self._criar_luz("Star_Rim", 'area', (0, -4, 2), 30, (0.9, 0.9, 1.0), 0.2)
        self._setup_world((0.0, 0.0, 0.01))

    def _preset_acao(self, **kwargs):
        """Escuro + laranja chamas. Ação, explosões, batalhas, suspense."""
        self.key("Key_Acao", posicao=(-2, 1, 3),   energia=120, cor=(1.0, 0.5, 0.1))
        self.rim("Rim_Acao", posicao=(0, -2, 2),    energia=100, cor=(1.0, 0.6, 0.1))
        self._criar_luz("Flash_Acao", 'ponto', (0, 0.5, 0.5), 200, (1.0, 0.3, 0.0), 0.2)
        self._criar_luz("Fill_Escuro", 'area', (3, 2, 2), 5, (0.2, 0.1, 0.05), 3.0)
        self._setup_world((0.03, 0.02, 0.01))

    def _preset_surreal(self, **kwargs):
        """Teal + magenta. Arte surreal, fantasma, dimensão alternativa."""
        self.key("Key_Surreal", posicao=(-2, 2, 3),  energia=50, cor=(0.0, 1.0, 0.9))
        self.fill("Fill_Surreal", posicao=(3, 1, 2),  energia=30, cor=(1.0, 0.0, 0.6))
        self.rim("Rim_Surreal", posicao=(0, -2, 3),   energia=60, cor=(0.6, 0.0, 1.0))
        self._setup_world((0.03, 0.0, 0.05))

    def _preset_podcast(self, posicao_a=(-1.0, 0.8, 1.5),
                        posicao_b=(1.0, 0.8, 1.5), **kwargs):
        """
        Ring lights para podcast — dois personagens em talk show.
        Boomer = warm (quente) | Kev = cool (frio), ou genérico A/B.
        """
        # Ring light do personagem A (quente)
        ring_a_pos = (posicao_a[0], posicao_a[1] + 1.5, posicao_a[2] + 0.2)
        self.ring_light("Ring_A", posicao=ring_a_pos, energia=55, cor=(0.9, 0.85, 0.7))

        # Ring light do personagem B (frio)
        ring_b_pos = (posicao_b[0], posicao_b[1] + 1.5, posicao_b[2] + 0.2)
        self.ring_light("Ring_B", posicao=ring_b_pos, energia=55, cor=(0.7, 0.85, 0.9))

        # Fill geral suave
        self.fill("Fill_Podcast", posicao=(0, -4, 3.5), energia=15, cor=(0.85, 0.88, 1.0), tamanho=4.0)

        # Mood azul de fundo
        self._criar_luz("BG_Mood", 'area', (0, 2.8, 1.0), 8, (0.1, 0.25, 0.8), 5.0)

        # Luz vermelha sutil do sign ON AIR
        self._criar_luz("OnAir_Light", 'ponto', (0, 2.0, 2.8), 5, (1.0, 0.1, 0.0), 0.1)

        self._setup_world((0.02, 0.02, 0.03))

    def _preset_produto(self, cor_key=(1.0, 0.97, 0.9), **kwargs):
        """
        Iluminação profissional de produto para fundo escuro.
        3-point clássico otimizado para materialidade do produto.
        """
        self.key("Key_Produto", posicao=(-2.5, 2, 4), energia=100, cor=cor_key, tamanho=0.8)
        self.fill("Fill_Produto", posicao=(3, 2, 2),    energia=30,  cor=(0.9, 0.92, 1.0), tamanho=2.0)
        self.rim("Rim_Produto", posicao=(0.5, -2.5, 3), energia=80,  cor=(0.95, 0.95, 1.0), tamanho=0.3)
        # Underlight para reflexo na superfície
        self._criar_luz("Under_Produto", 'area', (0, 0, -0.2), 20, (0.8, 0.85, 1.0), 2.0)
        self._setup_world((0.01, 0.01, 0.01))

    def _preset_exterior_dia(self, hora=14, **kwargs):
        """Sol do dia com bounce light. Para qualquer cena externa."""
        angulo_sol = math.radians(max(0, 90 - hora * 6))
        self.sol("Sol_Dia", rotacao=(angulo_sol, 0, math.radians(45)), energia=4.0, cor=(1.0, 0.97, 0.9))
        # Bounce light do céu
        self.ambiente("Sky_Bounce", posicao=(0, 0, 10), energia=30, cor=(0.6, 0.75, 1.0), tamanho=20.0)
        self._setup_world((0.5, 0.7, 1.0), strength=0.6)

    def _preset_exterior_noite(self, **kwargs):
        """Noite urbana — lua + luz da cidade."""
        self.sol("Lua", rotacao=(math.radians(80), 0, math.radians(200)),
                 energia=0.3, cor=(0.85, 0.88, 1.0))
        # Luz da cidade (laranja ambientral)
        self.ambiente("City_Glow", posicao=(0, 0, 3), energia=15, cor=(0.8, 0.4, 0.1), tamanho=20.0)
        self._setup_world((0.02, 0.02, 0.04))

    def _preset_drama(self, **kwargs):
        """Chiaroscuro intenso — drama, suspense, filmes noir."""
        self.key("Key_Drama", posicao=(-1, 2, 4),  energia=150, cor=(1.0, 0.95, 0.85), tamanho=0.3)
        self.rim("Rim_Drama", posicao=(0.5, -2, 3), energia=40,  cor=(0.7, 0.75, 1.0), tamanho=0.2)
        self._setup_world((0.005, 0.005, 0.005))

    def _preset_horror(self, **kwargs):
        """Luz única fria de baixo — terror/thriller."""
        self._criar_luz("Horror_Under", 'area', (0, 0.5, -0.3), 80, (0.5, 0.65, 1.0), 1.5)
        self.rim("Rim_Horror", posicao=(0, -2, 2), energia=20, cor=(0.4, 0.5, 1.0))
        self._setup_world((0.0, 0.0, 0.02))

    # ─────────────────────────────────────────────────────────────
    # ANIMAÇÃO DE LUZ
    # ─────────────────────────────────────────────────────────────

    def animar_intensidade(self, nome_luz: str, keyframes: list):
        """
        Anima a intensidade de uma luz ao longo do tempo.
        
        Args:
            nome_luz: Nome da luz criada
            keyframes: Lista de tuplas [(frame, energia), ...]
        
        Exemplo:
            luzes.animar_intensidade("Ring_A", [(1, 0), (24, 55), (720, 55)])
        """
        luz = self.luzes.get(nome_luz)
        if not luz:
            print(f"⚠️ Luz '{nome_luz}' não encontrada")
            return

        for frame, energia in keyframes:
            bpy.context.scene.frame_set(frame)
            luz.data.energy = energia
            luz.data.keyframe_insert(data_path="energy")

    def pulsar(self, nome_luz: str, energia_min=20, energia_max=80,
               periodo_frames=24, frame_inicio=1, frame_fim=240):
        """
        Animação de luz pulsante (neon, sinal, vida).
        Útil para signs ON AIR, neo, hologramas.
        """
        luz = self.luzes.get(nome_luz)
        if not luz:
            return

        for f in range(frame_inicio, frame_fim + 1, periodo_frames // 2):
            bpy.context.scene.frame_set(f)
            energia = energia_max if (f // (periodo_frames // 2)) % 2 == 0 else energia_min
            luz.data.energy = energia
            luz.data.keyframe_insert(data_path="energy")

    # ─────────────────────────────────────────────────────────────
    # UTILITÁRIOS
    # ─────────────────────────────────────────────────────────────

    def _setup_world(self, cor_bg=(0.02, 0.02, 0.02), strength=0.3):
        """Configura a cor de fundo do mundo (ambiente)."""
        scene = bpy.context.scene
        if not scene.world:
            scene.world = bpy.data.worlds.new("FGS_World")
        scene.world.use_nodes = True
        bg = scene.world.node_tree.nodes.get("Background")
        if bg:
            bg.inputs['Color'].default_value = (*cor_bg, 1.0)
            bg.inputs['Strength'].default_value = strength

    def limpar_luzes(self):
        """Remove todas as luzes criadas pelo sistema."""
        for nome, luz in self.luzes.items():
            bpy.data.objects.remove(luz, do_unlink=True)
        self.luzes.clear()
        print("✅ Todas as luzes removidas")

    def listar_luzes(self):
        """Lista todas as luzes ativas."""
        print(f"\n💡 LUZES CRIADAS ({len(self.luzes)}):")
        for nome, luz in self.luzes.items():
            print(f"   {nome} → {luz.data.energy}W | {tuple(round(c,2) for c in luz.data.color)}")
