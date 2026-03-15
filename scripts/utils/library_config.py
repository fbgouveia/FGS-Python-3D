# -*- coding: utf-8 -*-
"""
FGS LIBRARY CONFIG — Livraria de Acesso Rápido
Felipe Gouveia | 2026-03-15

Mapeia D:\Graphic Designer Resources\ para as categorias do Blenderscripts.
Fonte de verdade para TODOS os scripts que precisam de assets externos.
"""

import pathlib
import os
import json

# === FONTE DE VERDADE ===
# A biblioteca mãe — 477GB de assets profissionais
LIBRARY_ROOT = pathlib.Path(r"D:\Graphic Designer Resources")

# === GOOGLE DRIVE MIRROR ===
# Quando Google Drive Desktop está em Stream mode, acessar por aqui
GDRIVE_LIBRARY = pathlib.Path(r"G:\My Drive\FGS_LIBRARY")

# === MAPEAMENTO: Blenderscripts → Graphic Designer Resources ===
LIBRARY_MAP = {
    # HDRI e Iluminação
    "hdri":             LIBRARY_ROOT / "HDRI",
    "lighting":         LIBRARY_ROOT / "LUTS",

    # Vídeo e Motion
    "stock_video":      LIBRARY_ROOT / "Stock Video",
    "stock_video_collections": LIBRARY_ROOT / "Stock Video Collections",
    "motion_graphics":  LIBRARY_ROOT / "Motion Graphics",
    "broll":            LIBRARY_ROOT / "Stock Video",

    # VFX e Efeitos
    "vfx_packs":        LIBRARY_ROOT / "Effects",
    "overlays":         LIBRARY_ROOT / "Overlays",
    "transitions":      LIBRARY_ROOT / "Transitions",
    "backgrounds":      LIBRARY_ROOT / "Backgrounds",

    # Texto e UI
    "fonts":            LIBRARY_ROOT / "Fonts",
    "titles":           LIBRARY_ROOT / "TITLES",
    "lower_thirds":     LIBRARY_ROOT / "Lower Third Pack",
    "call_outs":        LIBRARY_ROOT / "Call Outs",

    # Templates de Software
    "templates_ae":     LIBRARY_ROOT / "After Effects",
    "templates_premiere": LIBRARY_ROOT / "PremierePro",

    # Áudio
    "music":            LIBRARY_ROOT / "MUSIC",
    "sfx":              LIBRARY_ROOT / "Sound Effects",
    "epidemic_sound":   LIBRARY_ROOT / "Epidemic Sound",

    # Identidade e Branding
    "logos":            LIBRARY_ROOT / "Logos",
    "icons":            LIBRARY_ROOT / "ICONS",
    "thumbnails":       LIBRARY_ROOT / "Thumbnails",

    # Grading
    "luts":             LIBRARY_ROOT / "LUTS",
    "codecs":           LIBRARY_ROOT / "CODECS",
}


def get_library_path(category: str, use_gdrive: bool = False) -> pathlib.Path:
    """
    Retorna o caminho correto para uma categoria da biblioteca.
    
    Args:
        category: Nome da categoria (ex: 'hdri', 'music', 'stock_video')
        use_gdrive: Se True, usa o mirror do Google Drive
    
    Returns:
        pathlib.Path para a pasta da categoria
    
    Exemplo:
        path = get_library_path('hdri')
        # D:\Graphic Designer Resources\HDRI
    """
    if use_gdrive and GDRIVE_LIBRARY.exists():
        gdrive_cat = GDRIVE_LIBRARY / category.upper()
        if gdrive_cat.exists():
            return gdrive_cat

    path = LIBRARY_MAP.get(category.lower())
    if path is None:
        raise KeyError(f"Categoria '{category}' não encontrada. Disponíveis: {list(LIBRARY_MAP.keys())}")
    return path


def list_assets(category: str, extensions: list = None, limit: int = 100) -> list:
    """
    Lista assets disponíveis em uma categoria.
    
    Args:
        category: Categoria da biblioteca
        extensions: Filtrar por extensão (ex: ['.mp4', '.mov'])
        limit: Máximo de arquivos retornados
    
    Returns:
        Lista de pathlib.Path dos arquivos encontrados
    """
    folder = get_library_path(category)
    if not folder.exists():
        return []

    files = []
    try:
        for f in folder.rglob("*"):
            if f.is_file():
                if extensions is None or f.suffix.lower() in extensions:
                    files.append(f)
                    if len(files) >= limit:
                        break
    except PermissionError:
        pass
    return files


def find_asset(name: str, category: str = None) -> pathlib.Path | None:
    """
    Busca um asset específico por nome (ou parte do nome).
    
    Args:
        name: Nome do arquivo (parcial aceito)
        category: Limitar a busca a uma categoria específica
    
    Returns:
        Caminho do primeiro arquivo encontrado ou None
    """
    search_paths = [LIBRARY_MAP[cat] for cat in LIBRARY_MAP] if category is None else [get_library_path(category)]

    for folder in search_paths:
        if not folder.exists():
            continue
        for f in folder.rglob(f"*{name}*"):
            if f.is_file():
                return f
    return None


def get_random_asset(category: str, extensions: list = None) -> pathlib.Path | None:
    """
    Retorna um asset aleatório de uma categoria.
    Útil para: música de fundo aleatória, B-roll aleatório, etc.
    """
    import random
    assets = list_assets(category, extensions, limit=500)
    if not assets:
        return None
    return random.choice(assets)


def library_status() -> dict:
    """
    Verifica quais categorias da biblioteca estão disponíveis localmente.
    """
    status = {}
    for cat, path in LIBRARY_MAP.items():
        status[cat] = {
            "path": str(path),
            "exists": path.exists(),
            "gdrive_available": (GDRIVE_LIBRARY / cat.upper()).exists()
        }
    return status


if __name__ == "__main__":
    print("=== FGS LIBRARY STATUS ===")
    s = library_status()
    for cat, info in s.items():
        icon = "OK" if info["exists"] else "XX"
        gd = " [GDrive OK]" if info["gdrive_available"] else ""
        print(f"  {icon} {cat:<30} {info['path']}{gd}")