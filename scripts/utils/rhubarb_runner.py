"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: rhubarb_runner.py                                  ║
║   Função: Processa WAVs com Rhubarb para gerar dados         ║
║           de lip sync (fonemas por frame)                    ║
║   Roda: FORA do Blender (no terminal PowerShell)            ║
╚══════════════════════════════════════════════════════════════╝

COMO USAR:
  # Processar todos os WAVs de um episódio:
  python scripts/utils/rhubarb_runner.py --ep 01

  # Processar um único arquivo WAV:
  python scripts/utils/rhubarb_runner.py --wav audio/raw/boomer_ep01_001.wav

PRÉ-REQUISITO:
  Rhubarb instalado em: D:/Blender/blenderscripts/tools/rhubarb/rhubarb.exe
  Download: https://github.com/DanielSWolf/rhubarb-lip-sync/releases
"""

import os
import json
import subprocess
import argparse
from pathlib import Path
import time


# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÕES
# ═══════════════════════════════════════════════════════════════

BASE_DIR = Path("D:/Blender/blenderscripts")
RHUBARB_EXE = BASE_DIR / "tools" / "rhubarb" / "rhubarb.exe"
AUDIO_RAW_DIR = BASE_DIR / "audio" / "raw"
LIPSYNC_DIR = BASE_DIR / "audio" / "lipsync"
FPS = 24  # Deve coincidir com o FPS do projeto Blender


# Mapeamento de fonemas Rhubarb → Shape Keys do Blender
# Para personagens estilizados (cartoon) usamos versão simplificada
PHONEME_TO_SHAPEKEY = {
    "A": "mouth_closed",       # M, B, P — boca fechada
    "B": "mouth_smile",        # Ee, I — sorriso largo
    "C": "mouth_open_small",   # E, Eh — levemente aberta
    "D": "mouth_open_smile",   # Ai, I — aberta com sorriso
    "E": "mouth_open_small",   # L, Th, K, S — dentes (mapeado para small)
    "F": "mouth_open_small",   # F, V — labio inferior (mapeado para small)
    "G": "mouth_oo",           # Oo, Q — boca arredondada
    "H": "mouth_open_wide",    # Ah, Oh — muito aberta
    "X": "mouth_rest"          # Silêncio — levemente aberta
}

# Shape keys e seus pesos máximos (entre 0.0 e 1.0)
SHAPEKEY_MAX_VALUES = {
    "mouth_closed":     1.0,
    "mouth_rest":       0.3,
    "mouth_open_small": 0.6,
    "mouth_open_wide":  1.0,
    "mouth_oo":         0.8,
    "mouth_smile":      0.9,
    "mouth_open_smile": 0.7
}


def verificar_rhubarb() -> bool:
    """Verifica se o Rhubarb está instalado corretamente."""
    if not RHUBARB_EXE.exists():
        print(f"❌ Rhubarb não encontrado em: {RHUBARB_EXE}")
        print("\n📥 COMO INSTALAR:")
        print("1. Acesse: https://github.com/DanielSWolf/rhubarb-lip-sync/releases")
        print("2. Baixe: rhubarb-lip-sync-X.X.X-windows.zip")
        print(f"3. Extraia em: {RHUBARB_EXE.parent}")
        print(f"4. Verifique que existe: {RHUBARB_EXE}")
        return False
    
    # Testar execução
    try:
        result = subprocess.run(
            [str(RHUBARB_EXE), "--version"],
            capture_output=True, text=True, timeout=10
        )
        print(f"✅ Rhubarb encontrado: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Erro ao executar Rhubarb: {e}")
        return False


def processar_wav(wav_path: Path, texto: str = None) -> Path | None:
    """
    Processa um arquivo WAV com o Rhubarb e gera JSON com phonemes.
    
    Args:
        wav_path: Caminho do arquivo WAV
        texto: Texto falado no áudio (melhora a precisão do Rhubarb)
    
    Returns:
        Path do JSON gerado, ou None em caso de erro
    """
    LIPSYNC_DIR.mkdir(parents=True, exist_ok=True)
    
    # Nome do JSON = mesmo nome do WAV mas na pasta lipsync
    json_path = LIPSYNC_DIR / wav_path.with_suffix('.json').name
    
    print(f"🔄 Processando: {wav_path.name}")
    
    # Montar comando do Rhubarb
    cmd = [
        str(RHUBARB_EXE),
        str(wav_path),
        "--outputFormat", "json",
        "--output", str(json_path),
        "--machineReadable",   # Sem output visual (mais rápido)
        "--quiet"              # Sem logs desnecessários
    ]
    
    # Adicionar texto se disponível (melhora muito a precisão)
    if texto:
        # Salvar texto temporariamente
        txt_temp = LIPSYNC_DIR / f"_temp_{wav_path.stem}.txt"
        with open(txt_temp, 'w', encoding='utf-8') as f:
            f.write(texto)
        cmd.extend(["--dialogFile", str(txt_temp)])
    
    try:
        inicio = time.time()
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=120  # 2 min max
        )
        duracao = time.time() - inicio
        
        if result.returncode == 0 and json_path.exists():
            # Verificar se JSON é válido
            with open(json_path, 'r') as f:
                dados = json.load(f)
            
            n_mouthcues = len(dados.get("mouthCues", []))
            print(f"   ✅ {json_path.name} | {n_mouthcues} fonemas | {duracao:.1f}s")
            
            # Limpar temp
            if texto and txt_temp.exists():
                txt_temp.unlink()
            
            return json_path
        else:
            print(f"   ❌ Erro no Rhubarb: {result.stderr[:200]}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"   ❌ Timeout — áudio muito longo ou Rhubarb travado")
        return None
    except Exception as e:
        print(f"   ❌ Erro inesperado: {e}")
        return None


def rhubarb_json_para_blender(json_path: Path, personagem: str, frame_offset: int = 0) -> list:
    """
    Converte o JSON do Rhubarb para formato de keyframes do Blender.
    
    Args:
        json_path: Caminho do JSON gerado pelo Rhubarb
        personagem: "boomer" ou "kev" (para nomear os shape keys)
        frame_offset: Frame de início desta fala na timeline do Blender
    
    Returns:
        Lista de dicts: [{frame, shape_key_name, value}]
    """
    with open(json_path, 'r') as f:
        dados = json.load(f)
    
    keyframes = []
    all_shape_keys = list(set(PHONEME_TO_SHAPEKEY.values()))
    
    for cue in dados.get("mouthCues", []):
        # Converter tempo (segundos) para frame
        frame = int(cue["start"] * FPS) + frame_offset
        phoneme = cue["value"]
        shape_key = PHONEME_TO_SHAPEKEY.get(phoneme, "mouth_rest")
        
        # Prefixar com nome do personagem (ex: "boomer_mouth_closed")
        shape_key_full = f"{personagem}_{shape_key}"
        
        # Zerear todos os shape keys neste frame
        for sk in all_shape_keys:
            keyframes.append({
                "frame": frame,
                "shape_key": f"{personagem}_{sk}",
                "value": 0.0
            })
        
        # Ativar o shape key correto
        max_val = SHAPEKEY_MAX_VALUES.get(shape_key, 0.8)
        keyframes.append({
            "frame": frame,
            "shape_key": shape_key_full,
            "value": max_val
        })
    
    # Adicionar frame de fechamento (após última fala)
    if dados.get("mouthCues"):
        last_cue = dados["mouthCues"][-1]
        last_frame = int(last_cue["end"] * FPS) + frame_offset + 5
        for sk in all_shape_keys:
            keyframes.append({
                "frame": last_frame,
                "shape_key": f"{personagem}_{sk}",
                "value": 0.0 if sk != "mouth_rest" else 0.2
            })
    
    return keyframes


def processar_episodio(numero_ep: str):
    """
    Processa todos os WAVs de um episódio usando o manifest.
    Gera JSONs do Rhubarb + arquivo de keyframes para o Blender.
    """
    print(f"\n🎬 PROCESSANDO LIP SYNC — EPISÓDIO {numero_ep}")
    print("=" * 55)
    
    # Verificar Rhubarb
    if not verificar_rhubarb():
        return
    
    # Ler manifest do episódio
    manifest_path = AUDIO_RAW_DIR / f"ep{numero_ep}_manifest.json"
    if not manifest_path.exists():
        print(f"❌ Manifest não encontrado: {manifest_path}")
        print(f"   Execute primeiro: python scripts/utils/elevenlabs_voice_gen.py --ep {numero_ep}")
        return
    
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    print(f"📋 {len(manifest)} falas para processar\n")
    
    # Calcular offset de frames (uma fala começa onde a outra termina + pausa)
    todos_keyframes = []
    frame_atual = 1
    sucesso = 0
    falha = 0
    
    for entrada in manifest:
        wav_path = Path(entrada["arquivo"])
        personagem = entrada["personagem"]
        texto = entrada.get("texto", "")
        pausa_depois = entrada.get("pausa_depois", 0.5)
        
        if not wav_path.exists():
            print(f"⚠️ WAV não encontrado: {wav_path.name}")
            falha += 1
            continue
        
        # Processar com Rhubarb
        json_path = processar_wav(wav_path, texto)
        
        if json_path:
            # Converter para keyframes do Blender
            keyframes = rhubarb_json_para_blender(json_path, personagem, frame_atual)
            todos_keyframes.extend(keyframes)
            
            # Calcular duração do áudio para avançar o offset
            try:
                import wave
                with wave.open(str(wav_path), 'r') as wav_file:
                    duracao_seg = wav_file.getnframes() / wav_file.getframerate()
            except:
                duracao_seg = 2.0  # Estimativa padrão
            
            frame_atual += int(duracao_seg * FPS) + int(pausa_depois * FPS)
            sucesso += 1
        else:
            falha += 1
    
    # Salvar todos os keyframes em um único JSON para o Blender
    output_keyframes = LIPSYNC_DIR / f"ep{numero_ep}_blender_keyframes.json"
    with open(output_keyframes, 'w', encoding='utf-8') as f:
        json.dump({
            "fps": FPS,
            "total_frames": frame_atual,
            "keyframes": todos_keyframes
        }, f, indent=2)
    
    print(f"\n{'='*55}")
    print(f"✅ Processados: {sucesso} | Falhas: {falha}")
    print(f"📄 Keyframes: {output_keyframes}")
    print(f"📊 Total de frames: {frame_atual} ({frame_atual/FPS:.1f}s)")
    print(f"\n⏭️  PRÓXIMO PASSO:")
    print(f"   No Blender → cole o script: scripts/youtube/boomer_kev_ep{numero_ep}.py")
    print(f"   O script importará automaticamente os dados de lip sync.")
    print(f"{'='*55}\n")


def main():
    parser = argparse.ArgumentParser(description="FGS — Rhubarb Lip Sync Runner")
    parser.add_argument('--ep', type=str, help='Número do episódio (ex: 01)')
    parser.add_argument('--wav', type=str, help='Processar um WAV específico')
    parser.add_argument('--check', action='store_true', help='Verificar instalação do Rhubarb')
    
    args = parser.parse_args()
    
    if args.check:
        verificar_rhubarb()
    elif args.wav:
        wav = Path(args.wav)
        processar_wav(wav)
    elif args.ep:
        processar_episodio(args.ep)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
