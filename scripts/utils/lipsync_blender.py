"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: lipsync_blender.py                                 ║
║   Função: Aplica dados de lip sync nos personagens           ║
║           do Blender via Shape Keys                          ║
║   Roda: DENTRO do Blender (cole na aba Scripting)           ║
╚══════════════════════════════════════════════════════════════╝

COMO USAR:
  1. Certifique-se de ter rodado ANTES (no terminal):
     - elevenlabs_voice_gen.py --ep 01  (gerou os WAVs)
     - rhubarb_runner.py --ep 01        (gerou os JSONs)
  
  2. Abra o Blender com a cena do Boomer & Kev já criada
  3. Vá para aba "Scripting"
  4. Cole este script e clique ▶ Run Script

  O script vai:
  - Criar Shape Keys nas bocas dos personagens (se não existirem)
  - Aplicar keyframes de lip sync na timeline
  - Importar áudio no Video Sequence Editor
"""

import bpy
import json
import os
import math
from pathlib import Path


# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÕES — Ajustar por episódio
# ═══════════════════════════════════════════════════════════════
NUMERO_EPISODIO = "01"
BASE_DIR = Path("D:/Blender/blenderscripts")
LIPSYNC_DIR = BASE_DIR / "audio" / "lipsync"
AUDIO_RAW_DIR = BASE_DIR / "audio" / "raw"

# Nome do arquivo de keyframes gerado pelo rhubarb_runner.py
KEYFRAMES_FILE = LIPSYNC_DIR / f"ep{NUMERO_EPISODIO}_blender_keyframes.json"

# Partes da boca de cada personagem (objetos do Blender)
# Estes nomes devem corresponder aos objetos criados no boomer_kev_ep01.py
BOCAS = {
    "boomer": "Boomer_Focinho",   # Objeto que representa a boca do Boomer
    "kev": "Kev_Focinho"           # Objeto que representa a boca do Kev
}


# ═══════════════════════════════════════════════════════════════
# SHAPE KEYS — Posições de boca para lip sync estilizado
# ═══════════════════════════════════════════════════════════════

# Cada shape key = uma posição de boca = variação da malha
# Para personagens esféricos simples, usamos escala Z e Y do objeto
SHAPE_KEY_TRANSFORMS = {
    "mouth_closed": {
        "scale_z": 0.3,    # Achatado verticalmente
        "scale_y": 0.7,
        "location_z": 0.0
    },
    "mouth_rest": {
        "scale_z": 0.5,
        "scale_y": 0.7,
        "location_z": 0.0
    },
    "mouth_open_small": {
        "scale_z": 0.65,
        "scale_y": 0.85,
        "location_z": -0.01
    },
    "mouth_open_wide": {
        "scale_z": 1.0,
        "scale_y": 1.0,
        "location_z": -0.02
    },
    "mouth_oo": {
        "scale_z": 0.8,
        "scale_y": 0.6,    # Mais estreito (arredondado)
        "location_z": -0.01
    },
    "mouth_smile": {
        "scale_z": 0.45,
        "scale_y": 1.1,    # Mais largo (sorriso)
        "location_z": 0.0
    },
    "mouth_open_smile": {
        "scale_z": 0.75,
        "scale_y": 1.05,
        "location_z": -0.015
    }
}

# Shape key padrão quando não há fala
DEFAULT_SHAPE_KEY = "mouth_rest"


def criar_shape_keys_para_personagem(nome_objeto: str, personagem: str):
    """
    Cria Shape Keys no objeto de boca do personagem.
    
    Para objetos simples (esfera), Shape Keys = variações de escala/posição.
    Para malhas complexas com boca modelada = deformações de vértices.
    """
    obj = bpy.data.objects.get(nome_objeto)
    if not obj:
        print(f"⚠️ Objeto '{nome_objeto}' não encontrado. Pulando Shape Keys.")
        return False
    
    # Ativar o objeto
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Verificar se já tem Shape Keys
    if not obj.data.shape_keys:
        # Criar Shape Key base ("Basis")
        obj.shape_key_add(name="Basis", from_mix=False)
        print(f"   Basis criado para {nome_objeto}")
    
    # Criar uma Shape Key para cada posição de boca
    for sk_nome, transforms in SHAPE_KEY_TRANSFORMS.items():
        sk_nome_completo = f"{personagem}_{sk_nome}"
        
        # Verificar se já existe
        if obj.data.shape_keys.key_blocks.get(sk_nome_completo):
            continue
        
        # Criar nova a partir da base
        sk = obj.shape_key_add(name=sk_nome_completo, from_mix=False)
        print(f"   ✅ Shape Key criada: {sk_nome_completo}")
    
    print(f"✅ Shape Keys criadas para: {nome_objeto}")
    return True


def aplicar_lipsync_via_escala(keyframes_data: list, personagem: str):
    """
    Aplica lip sync usando animação de escala do objeto de boca.
    
    Esta é uma abordagem alternativa quando o objeto não tem Shape Keys de vértices.
    Funciona muito bem para personagens esféricos estilizados (como Boomer & Kev).
    
    Args:
        keyframes_data: Lista de keyframes do JSON do Rhubarb processado
        personagem: "boomer" ou "kev"
    """
    nome_objeto = BOCAS.get(personagem)
    if not nome_objeto:
        print(f"⚠️ Boca de '{personagem}' não configurada em BOCAS")
        return
    
    obj = bpy.data.objects.get(nome_objeto)
    if not obj:
        print(f"⚠️ Objeto '{nome_objeto}' não encontrado na cena")
        return
    
    # Escala base do objeto (posição de descanso)
    scale_base_x = obj.scale.x
    scale_base_y = obj.scale.y
    scale_base_z = obj.scale.z
    
    print(f"🎭 Aplicando lip sync em: {nome_objeto}")
    
    # Filtrar keyframes deste personagem
    kfs_personagem = [kf for kf in keyframes_data if personagem in kf.get("shape_key", "")]
    
    # Agrupar por frame (pegar o de maior value por frame)
    frames_unicos = {}
    for kf in kfs_personagem:
        frame = kf["frame"]
        if frame not in frames_unicos or kf["value"] > frames_unicos[frame]["value"]:
            frames_unicos[frame] = kf
    
    # Aplicar keyframes de escala
    aplicados = 0
    for frame, kf in sorted(frames_unicos.items()):
        shape_key_nome = kf["shape_key"].replace(f"{personagem}_", "")
        value = kf["value"]
        
        transforms = SHAPE_KEY_TRANSFORMS.get(shape_key_nome, SHAPE_KEY_TRANSFORMS[DEFAULT_SHAPE_KEY])
        
        # Calcular nova escala baseada no shape key
        nova_scale_z = scale_base_z * transforms["scale_z"]
        nova_scale_y = scale_base_y * transforms["scale_y"]
        loc_offset_z = transforms["location_z"]
        
        # Interpolar com o value (0-1)
        final_z = scale_base_z + (nova_scale_z - scale_base_z) * value
        final_y = scale_base_y + (nova_scale_y - scale_base_y) * value
        
        # Inserir keyframe
        bpy.context.scene.frame_set(frame)
        obj.scale.z = final_z
        obj.scale.y = final_y
        obj.location.z += loc_offset_z * value
        
        obj.keyframe_insert(data_path="scale", index=2)  # Z
        obj.keyframe_insert(data_path="scale", index=1)  # Y
        obj.keyframe_insert(data_path="location", index=2)  # Z location
        
        # Suavizar interpolação
        if obj.animation_data and obj.animation_data.action:
            for fcurve in obj.animation_data.action.fcurves:
                if fcurve.data_path in ["scale", "location"]:
                    for kp in fcurve.keyframe_points:
                        if kp.co[0] == frame:
                            kp.interpolation = 'SINE'
        
        aplicados += 1
    
    print(f"   ✅ {aplicados} keyframes de escala aplicados para {personagem}")


def importar_audio_blender(numero_ep: str):
    """
    Importa os arquivos de áudio do episódio no Video Sequence Editor (VSE) do Blender.
    O VSE permite sincronizar o áudio com a animação.
    """
    scene = bpy.context.scene
    
    # Ativar o uso de sequências
    if not scene.sequence_editor:
        scene.sequence_editor_create()
    
    vse = scene.sequence_editor
    
    # Ler manifest para saber a ordem e timing dos áudios
    manifest_path = AUDIO_RAW_DIR / f"ep{numero_ep}_manifest.json"
    if not manifest_path.exists():
        print(f"⚠️ Manifest não encontrado: {manifest_path}")
        return
    
    with open(str(manifest_path), 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    print(f"\n🔊 Importando áudio no VSE — {len(manifest)} faixas")
    
    frame_atual = 1
    canal = {
        "boomer": 1,  # Canal 1 = Boomer
        "kev": 2      # Canal 2 = Kev
    }
    
    for entrada in manifest:
        wav_path = entrada["arquivo"]
        personagem = entrada["personagem"]
        pausa = entrada.get("pausa_depois", 0.5)
        
        if not Path(wav_path).exists():
            print(f"   ⚠️ Áudio não encontrado: {wav_path}")
            continue
        
        try:
            # Adicionar strip de áudio no VSE
            bpy.ops.sequencer.sound_strip_add(
                filepath=wav_path,
                frame_start=frame_atual,
                channel=canal.get(personagem, 1)
            )
            
            print(f"   ✅ Frame {frame_atual}: {personagem} — {Path(wav_path).name}")
            
            # Avançar frame baseado na duração estimada + pausa
            try:
                import wave
                with wave.open(wav_path, 'r') as wf:
                    duracao_frames = int(wf.getnframes() / wf.getframerate() * 24)
            except:
                duracao_frames = 48  # Padrão: 2 segundos
            
            frame_atual += duracao_frames + int(pausa * 24)
            
        except Exception as e:
            print(f"   ❌ Erro ao importar {wav_path}: {e}")
    
    # Ativar áudio no render
    scene.render.ffmpeg.audio_codec = 'AAC'
    scene.render.ffmpeg.audio_bitrate = 192
    
    print(f"✅ Áudio importado no VSE | Frame total: {frame_atual}")


def verificar_arquivos_necessarios(numero_ep: str) -> bool:
    """Verifica se todos os arquivos necessários existem antes de prosseguir."""
    ok = True
    
    # Verificar keyframes
    if not KEYFRAMES_FILE.exists():
        print(f"❌ Keyframes não encontrados: {KEYFRAMES_FILE}")
        print(f"   Execute: python scripts/utils/rhubarb_runner.py --ep {numero_ep}")
        ok = False
    
    # Verificar manifest
    manifest = AUDIO_RAW_DIR / f"ep{numero_ep}_manifest.json"
    if not manifest.exists():
        print(f"⚠️ Manifest não encontrado: {manifest}")
        print(f"   Execute: python scripts/utils/elevenlabs_voice_gen.py --ep {numero_ep}")
        ok = False
    
    return ok


def aplicar_lipsync_completo():
    """
    Função principal — aplica lip sync completo para todos os personagens.
    Deve ser chamada com a cena do episódio já aberta no Blender.
    """
    print("\n" + "=" * 60)
    print("  FGS — LIP SYNC ENGINE")
    print(f"  Episódio {NUMERO_EPISODIO}")
    print("=" * 60)
    
    # Verificar arquivos
    if not verificar_arquivos_necessarios(NUMERO_EPISODIO):
        print("\n❌ Arquivos necessários não encontrados. Verifique acima.")
        return
    
    # Carregar dados de keyframes
    with open(str(KEYFRAMES_FILE), 'r') as f:
        dados = json.load(f)
    
    keyframes = dados.get("keyframes", [])
    print(f"📊 {len(keyframes)} keyframes carregados")
    
    # Criar Shape Keys para cada personagem
    print("\n🔧 Criando Shape Keys...")
    for personagem, nome_objeto in BOCAS.items():
        criar_shape_keys_para_personagem(nome_objeto, personagem)
    
    # Aplicar lip sync via escala (funciona sem mesh complexa)
    print("\n🎭 Aplicando animação de lip sync...")
    for personagem in BOCAS.keys():
        aplicar_lipsync_via_escala(keyframes, personagem)
    
    # Importar áudio no VSE
    print("\n🔊 Importando áudio...")
    importar_audio_blender(NUMERO_EPISODIO)
    
    # Atualizar cena
    bpy.context.view_layer.update()
    
    print("\n" + "=" * 60)
    print("  ✅ LIP SYNC APLICADO COM SUCESSO!")
    print("")
    print("  COMO VERIFICAR:")
    print("  1. Pressione Space para dar Play na timeline")
    print("  2. As bocas vão se mover sincronizadas com o áudio")
    print("  3. Use Numpad 0 → ver pela câmera")
    print("")
    print("  SE PRECISAR AJUSTAR:")
    print("  - Edite SHAPE_KEY_TRANSFORMS para alterar posições")
    print("  - Reexecute este script para aplicar novamente")
    print("=" * 60 + "\n")


# ═══════════════════════════════════════════════════════════════
# EXECUÇÃO
# ═══════════════════════════════════════════════════════════════
aplicar_lipsync_completo()
