"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: elevenlabs_voice_gen.py                           ║
║   Função: Gera vozes dos personagens via ElevenLabs API     ║
║   Roda: FORA do Blender (no terminal PowerShell)            ║
╚══════════════════════════════════════════════════════════════╝

COMO USAR:
  # Primeiro uso — configura API key:
  python scripts/utils/elevenlabs_voice_gen.py --setup

  # Gerar vozes de um episódio completo:
  python scripts/utils/elevenlabs_voice_gen.py --ep 01

  # Gerar apenas uma fala de teste:
  python scripts/utils/elevenlabs_voice_gen.py --test "Olá, eu sou o Boomer!" --char boomer

REQUISITOS:
  pip install elevenlabs python-dotenv
"""

import os
import json
import argparse
import time
from pathlib import Path

# Tentar importar ElevenLabs — instala se não tiver
try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import VoiceSettings
except ImportError:
    print("📦 Instalando ElevenLabs SDK...")
    os.system("pip install elevenlabs")
    from elevenlabs.client import ElevenLabs
    from elevenlabs import VoiceSettings

try:
    from dotenv import load_dotenv
except ImportError:
    os.system("pip install python-dotenv")
    from dotenv import load_dotenv


# ═══════════════════════════════════════════════════════════════
# CONFIGURAÇÕES DOS PERSONAGENS
# ═══════════════════════════════════════════════════════════════

# Caminhos do projeto
BASE_DIR = Path("D:/Blender/blenderscripts")
AUDIO_RAW_DIR = BASE_DIR / "audio" / "raw"
AUDIO_SCRIPTS_DIR = BASE_DIR / "audio" / "scripts"
ENV_FILE = BASE_DIR / ".env"

# Configurações de voz por personagem
# Para encontrar o voice_id: site elevenlabs.io → Voices → copiar ID
PERSONAGENS = {
    "boomer": {
        "nome_display": "Boomer",
        "voice_id": "COLE_AQUI_O_VOICE_ID_DO_BOOMER",  # Trocar pelo ID real
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.75,       # Voz consistente (0.0-1.0)
            "similarity_boost": 0.85, # Fidelidade à voz base
            "style": 0.30,           # Estilo expressivo (0.0-1.0)
            "use_speaker_boost": True
        },
        "speed": 0.90,               # Velocidade da fala (0.5-2.0)
        "descricao": "Urso, voz grave, calma, experiente"
    },
    "kev": {
        "nome_display": "Kev",
        "voice_id": "COLE_AQUI_O_VOICE_ID_DO_KEV",  # Trocar pelo ID real
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.45,       # Mais variação — ele é expressivo
            "similarity_boost": 0.80,
            "style": 0.55,           # Mais personalidade
            "use_speaker_boost": True
        },
        "speed": 1.10,               # Ligeiramente mais rápido
        "descricao": "Raposa, voz jovem, energética, animada"
    }
}


def configurar_api():
    """Configuração inicial — salva API key no .env."""
    print("\n🔧 CONFIGURAÇÃO INICIAL — ElevenLabs API")
    print("=" * 50)
    print("1. Acesse: https://elevenlabs.io")
    print("2. Faça login → Profile → API Keys")
    print("3. Copie sua API Key\n")
    
    api_key = input("🔑 Cole sua API Key aqui: ").strip()
    
    if not api_key:
        print("❌ API Key não pode ser vazia!")
        return False
    
    # Salvar no .env
    env_content = f'ELEVENLABS_API_KEY="{api_key}"\n'
    with open(ENV_FILE, 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ API Key salva em: {ENV_FILE}")
    
    # Criar pastas necessárias
    AUDIO_RAW_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "audio" / "lipsync").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "audio" / "final").mkdir(parents=True, exist_ok=True)
    
    print("✅ Pastas de áudio criadas")
    
    # Testar conexão
    print("\n🧪 Testando conexão com ElevenLabs...")
    load_dotenv(ENV_FILE)
    client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    
    try:
        voices = client.voices.get_all()
        print(f"✅ Conexão OK! {len(voices.voices)} vozes disponíveis na sua conta.")
        print("\n📋 Suas vozes disponíveis:")
        for v in voices.voices[:10]:  # Mostrar até 10
            print(f"   • {v.name} — ID: {v.voice_id}")
        print("\n💡 Copie os IDs acima e coloque em PERSONAGENS{} no início do script.")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return False
    
    return True


def gerar_voz(texto: str, personagem: str, output_path: Path, client: ElevenLabs) -> bool:
    """
    Gera um arquivo WAV de áudio para um personagem.
    
    Args:
        texto: O que o personagem vai falar
        personagem: "boomer" ou "kev"
        output_path: Onde salvar o arquivo WAV
        client: Cliente ElevenLabs já autenticado
    
    Returns:
        True se gerado com sucesso
    """
    config = PERSONAGENS.get(personagem)
    if not config:
        print(f"❌ Personagem '{personagem}' não encontrado!")
        return False
    
    print(f"🎙️ Gerando voz de {config['nome_display']}: \"{texto[:50]}...\"")
    
    try:
        # Gerar áudio via API
        audio_generator = client.generate(
            text=texto,
            voice=config["voice_id"],
            model=config["model_id"],
            voice_settings=VoiceSettings(
                stability=config["voice_settings"]["stability"],
                similarity_boost=config["voice_settings"]["similarity_boost"],
                style=config["voice_settings"]["style"],
                use_speaker_boost=config["voice_settings"]["use_speaker_boost"]
            )
        )
        
        # Salvar como WAV
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            for chunk in audio_generator:
                f.write(chunk)
        
        # Verificar se arquivo foi criado
        if output_path.exists() and output_path.stat().st_size > 0:
            tamanho_kb = output_path.stat().st_size / 1024
            print(f"   ✅ Salvo: {output_path.name} ({tamanho_kb:.1f} KB)")
            return True
        else:
            print(f"   ❌ Arquivo vazio ou não criado")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao gerar voz: {e}")
        return False


def parsear_dialogo(arquivo_dialogo: Path) -> list:
    """
    Lê o arquivo de diálogo e retorna lista de falas.
    
    Formato esperado:
        BOOMER: Texto da fala | [1.5]
        KEV: Outra fala | [0.8]
        [AMBOS: risada] → ignorado (sem fala)
    
    Returns:
        Lista de dicts: [{"personagem": "boomer", "texto": "...", "pausa": 1.5}]
    """
    falas = []
    
    if not arquivo_dialogo.exists():
        print(f"❌ Arquivo de diálogo não encontrado: {arquivo_dialogo}")
        return []
    
    with open(arquivo_dialogo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    for i, linha in enumerate(linhas):
        linha = linha.strip()
        
        # Ignorar comentários e linhas vazias
        if not linha or linha.startswith('#'):
            continue
        
        # Ignorar ações entre colchetes ([AMBOS:...])
        if linha.startswith('['):
            continue
        
        # Parsear "PERSONAGEM: texto | [pausa]"
        if ':' in linha:
            partes = linha.split(':', 1)
            personagem_raw = partes[0].strip().lower()
            resto = partes[1].strip()
            
            # Extrair pausa se existir
            pausa = 0.5  # padrão
            if '| [' in resto:
                texto_partes = resto.split('| [')
                texto = texto_partes[0].strip()
                try:
                    pausa = float(texto_partes[1].replace(']', '').strip())
                except:
                    pausa = 0.5
            else:
                texto = resto
            
            # Remover ações entre colchetes dentro do texto
            import re
            texto = re.sub(r'\[.*?\]', '', texto).strip()
            
            if texto and personagem_raw in PERSONAGENS:
                falas.append({
                    "index": i,
                    "personagem": personagem_raw,
                    "texto": texto,
                    "pausa_depois": pausa
                })
    
    return falas


def gerar_episodio(numero_ep: str, client: ElevenLabs):
    """
    Gera todos os arquivos de áudio de um episódio completo.
    
    Args:
        numero_ep: Número do episódio ("01", "02", etc.)
        client: Cliente ElevenLabs autenticado
    """
    print(f"\n🎬 GERANDO VOZES — EPISÓDIO {numero_ep}")
    print("=" * 50)
    
    # Ler arquivo de diálogo
    arquivo_dialogo = AUDIO_SCRIPTS_DIR / f"ep{numero_ep}_dialogo.txt"
    falas = parsear_dialogo(arquivo_dialogo)
    
    if not falas:
        print(f"❌ Nenhuma fala encontrada em: {arquivo_dialogo}")
        print(f"💡 Crie o arquivo: {arquivo_dialogo}")
        print("   Formato: BOOMER: texto da fala | [1.5]")
        return
    
    print(f"📋 {len(falas)} falas encontradas\n")
    
    # Gerar arquivo WAV para cada fala
    sucesso = 0
    falha = 0
    manifest = []  # Para o Rhubarb e o Blender
    
    for fala in falas:
        personagem = fala["personagem"]
        idx = fala["index"]
        
        # Nome do arquivo: boomer_ep01_001.wav
        nome_arquivo = f"{personagem}_ep{numero_ep}_{idx:03d}.wav"
        output_path = AUDIO_RAW_DIR / nome_arquivo
        
        ok = gerar_voz(fala["texto"], personagem, output_path, client)
        
        if ok:
            sucesso += 1
            manifest.append({
                "arquivo": str(output_path),
                "personagem": personagem,
                "texto": fala["texto"],
                "pausa_depois": fala["pausa_depois"],
                "index": idx
            })
        else:
            falha += 1
        
        # Respeitar rate limit da API (0.5s entre requests)
        time.sleep(0.5)
    
    # Salvar manifest para uso pelo Rhubarb e Blender
    manifest_path = AUDIO_RAW_DIR / f"ep{numero_ep}_manifest.json"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*50}")
    print(f"✅ Concluído: {sucesso} gerados | {falha} falhas")
    print(f"📄 Manifest: {manifest_path}")
    print(f"\n⏭️  PRÓXIMO PASSO:")
    print(f"   python scripts/utils/rhubarb_runner.py --ep {numero_ep}")
    print(f"{'='*50}\n")


def gerar_teste(texto: str, personagem: str, client: ElevenLabs):
    """Gera um áudio de teste rápido para validar a voz de um personagem."""
    output_path = AUDIO_RAW_DIR / f"TEST_{personagem}.wav"
    AUDIO_RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🧪 TESTE DE VOZ — {personagem.upper()}")
    ok = gerar_voz(texto, personagem, output_path, client)
    
    if ok:
        print(f"\n✅ Áudio de teste salvo em: {output_path}")
        print(f"💡 Abra o arquivo para escutar a voz do {personagem.title()}")
        # Tentar abrir automaticamente no Windows
        os.startfile(str(output_path))
    else:
        print("❌ Falha no teste. Verifique o Voice ID e a API Key.")


def main():
    parser = argparse.ArgumentParser(description="FGS — Gerador de Vozes ElevenLabs")
    parser.add_argument('--setup', action='store_true', help='Configuração inicial')
    parser.add_argument('--ep', type=str, help='Número do episódio (ex: 01)')
    parser.add_argument('--test', type=str, help='Texto para teste de voz')
    parser.add_argument('--char', type=str, default='boomer', help='Personagem para teste (boomer/kev)')
    
    args = parser.parse_args()
    
    if args.setup:
        configurar_api()
        return
    
    # Carregar API key
    load_dotenv(ENV_FILE)
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not api_key or api_key == '""':
        print("❌ API Key não configurada!")
        print("   Execute primeiro: python scripts/utils/elevenlabs_voice_gen.py --setup")
        return
    
    client = ElevenLabs(api_key=api_key.strip('"'))
    
    if args.test:
        gerar_teste(args.test, args.char, client)
    elif args.ep:
        gerar_episodio(args.ep, client)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
