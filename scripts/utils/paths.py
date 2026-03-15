# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: paths.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — PATH MANAGER v1.0                  ║
║   Centralized Path Resolution for FGSS Pipeline             ║
╚══════════════════════════════════════════════════════════════╝
"""

import pathlib
import os

# 1. Base Project Resolution
# This ensures paths work regardless of drive letter or installation folder
BASE_DIR = pathlib.Path(__file__).resolve().parents[2]

# 2. Main Directories
AGENT_DIR = BASE_DIR / ".agent"
SCRIPTS_DIR = BASE_DIR / "scripts"
UTILS_DIR = SCRIPTS_DIR / "utils"
CHARACTERS_DIR = BASE_DIR / "characters"
SCENES_DIR = BASE_DIR / "scenes"
MOTIONS_DIR = BASE_DIR / "motions"
AUDIO_DIR = BASE_DIR / "audio"
RENDERS_DIR = BASE_DIR / "renders"

# 3. Audio Subdirectories
AUDIO_RAW = AUDIO_DIR / "raw"
AUDIO_SCRIPTS = AUDIO_DIR / "scripts"
AUDIO_LIPSYNC = AUDIO_DIR / "lipsync"
AUDIO_FINAL = AUDIO_DIR / "final"

# 4. Render Subdirectories
RENDERS_DRAFTS = RENDERS_DIR / "drafts"
RENDERS_FINALS = RENDERS_DIR / "finals"

# 5. Assets — Livraria Local do Blenderscripts (leve, versionada no git)
ASSETS_DIR        = BASE_DIR / "assets"
ASSETS_HDRI       = ASSETS_DIR / "hdri"
ASSETS_LIGHTING   = ASSETS_DIR / "lighting_presets"
ASSETS_MOTION     = ASSETS_DIR / "motion_graphics"
ASSETS_PROPS      = ASSETS_DIR / "props"
ASSETS_TEMPLATES  = ASSETS_DIR / "templates_ae"
ASSETS_VFX        = ASSETS_DIR / "vfx_packs"

# 6. Livraria Externa (Graphic Designer Resources — 477GB)
# Fonte de verdade para assets de produção profissional.
# Acesso aleatório — ambos os projetos (Blenderscripts + React Portfolio) consomem.
# Futura pipeline: Blenderscripts → renders/finals → React Portfolio (auto-inject)
LIBRARY_ROOT       = pathlib.Path(r"D:\Graphic Designer Resources")
LIBRARY_HDRI       = LIBRARY_ROOT / "HDRI"
LIBRARY_MOTION     = LIBRARY_ROOT / "Motion Graphics"
LIBRARY_VFX        = LIBRARY_ROOT / "Effects"
LIBRARY_OVERLAYS   = LIBRARY_ROOT / "Overlays"
LIBRARY_TRANSITIONS= LIBRARY_ROOT / "Transitions"
LIBRARY_STOCK      = LIBRARY_ROOT / "Stock Video"
LIBRARY_MUSIC      = LIBRARY_ROOT / "MUSIC"
LIBRARY_SFX        = LIBRARY_ROOT / "Sound Effects"
LIBRARY_FONTS      = LIBRARY_ROOT / "Fonts"
LIBRARY_LUTS       = LIBRARY_ROOT / "LUTS"
LIBRARY_TEMPLATES  = LIBRARY_ROOT / "After Effects"
LIBRARY_BACKGROUNDS= LIBRARY_ROOT / "Backgrounds"

# 7. React Portfolio (destino do output do Blenderscripts)
PORTFOLIO_ROOT     = pathlib.Path(r"D:\Felipe Gouveia\React-Portfolio")
PORTFOLIO_UPLOADS  = PORTFOLIO_ROOT / "public" / "uploads" / "renders"
PORTFOLIO_PROJECTS = PORTFOLIO_ROOT / "public" / "projects.json"

# 8. Configs
ENV_FILE = BASE_DIR / ".env"


def get_library(category: str) -> pathlib.Path:
    """
    Retorna o caminho correto da livraria para uma categoria.
    Prioriza a livraria externa (GDR 477GB).
    Fallback para assets/ local se GDR não estiver disponível.

    Categorias disponíveis:
        hdri, motion, vfx, overlays, transitions, stock,
        music, sfx, fonts, luts, templates, backgrounds

    Uso:
        from paths import get_library
        hdri_dir  = get_library("hdri")
        music_dir = get_library("music")
    """
    _map = {
        "hdri":        (LIBRARY_HDRI,        ASSETS_HDRI),
        "motion":      (LIBRARY_MOTION,      ASSETS_MOTION),
        "vfx":         (LIBRARY_VFX,         ASSETS_VFX),
        "overlays":    (LIBRARY_OVERLAYS,    ASSETS_VFX),
        "transitions": (LIBRARY_TRANSITIONS, ASSETS_VFX),
        "stock":       (LIBRARY_STOCK,       ASSETS_DIR),
        "music":       (LIBRARY_MUSIC,       AUDIO_RAW),
        "sfx":         (LIBRARY_SFX,         AUDIO_RAW),
        "fonts":       (LIBRARY_FONTS,       ASSETS_DIR),
        "luts":        (LIBRARY_LUTS,        ASSETS_DIR),
        "templates":   (LIBRARY_TEMPLATES,   ASSETS_TEMPLATES),
        "backgrounds": (LIBRARY_BACKGROUNDS, ASSETS_DIR),
    }
    primary, fallback = _map.get(category.lower(), (ASSETS_DIR, ASSETS_DIR))
    return primary if primary.exists() else fallback


def ensure_structure():
    """Ensure all required directories exist."""
    dirs = [
        AUDIO_RAW, AUDIO_SCRIPTS, AUDIO_LIPSYNC, AUDIO_FINAL,
        RENDERS_DRAFTS, RENDERS_FINALS,
        CHARACTERS_DIR, SCENES_DIR, MOTIONS_DIR,
        ASSETS_HDRI, ASSETS_LIGHTING, ASSETS_MOTION,
        ASSETS_PROPS, ASSETS_TEMPLATES, ASSETS_VFX,
        PORTFOLIO_UPLOADS,
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def get_relative_to_root(path_str):
    """Utility to resolve paths relative to project root."""
    return BASE_DIR / path_str


if __name__ == "__main__":
    print(f"FGSS Root:      {BASE_DIR}")
    print(f"Library Root:   {LIBRARY_ROOT} — exists: {LIBRARY_ROOT.exists()}")
    print(f"Portfolio Root: {PORTFOLIO_ROOT} — exists: {PORTFOLIO_ROOT.exists()}")
    ensure_structure()
    print("Structure verified.")
    print("\nLibrary quick-check:")
    for cat in ["hdri", "music", "stock", "vfx", "motion", "fonts", "luts"]:
        p = get_library(cat)
        print(f"  {cat:<15} → {p}  [{'OK' if p.exists() else 'FALLBACK'}]")
