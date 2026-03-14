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

# 5. Configs
ENV_FILE = BASE_DIR / ".env"

def ensure_structure():
    """Ensure all required directories exist."""
    dirs = [
        AUDIO_RAW, AUDIO_SCRIPTS, AUDIO_LIPSYNC, AUDIO_FINAL,
        RENDERS_DRAFTS, RENDERS_FINALS,
        CHARACTERS_DIR, SCENES_DIR, MOTIONS_DIR
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

def get_relative_to_root(path_str):
    """Utility to resolve paths relative to project root."""
    return BASE_DIR / path_str

if __name__ == "__main__":
    print(f"FGSS Root: {BASE_DIR}")
    ensure_structure()
    print("Structure verified.")
