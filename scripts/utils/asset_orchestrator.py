# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: asset_orchestrator.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — ASSET ORCHESTRATOR v1.0           ║
║   Intelligent Sorting & Extraction for Graphic Resources    ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import shutil
import zipfile
from pathlib import Path
try:
    from logger import get_logger
    from paths import BASE_DIR
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger("ORCHESTRATOR")
    BASE_DIR = Path(__file__).resolve().parents[2]

log = get_logger("ORCHESTRATOR") if 'get_logger' in globals() else logging.getLogger("ORCHESTRATOR")

# 1. Resource Categories
MAPPING = {
    ".abr": "Brushes/Photoshop",
    ".asl": "Styles/Photoshop",
    ".atn": "Actions/Photoshop",
    ".csh": "Shapes/Photoshop",
    ".grd": "Gradients/Photoshop",
    ".pat": "Patterns/Photoshop",
    ".ttf": "Fonts",
    ".otf": "Fonts",
    ".png": "Images/Overlays",
    ".jpg": "Images/Backgrounds",
    ".jpeg": "Images/Backgrounds",
    ".psd": "Source/Photoshop",
    ".blend": "Models/Blender",
    ".obj": "Models/Raw",
    ".fbx": "Models/Raw",
    ".mp4": "Overlays/Video",
    ".mov": "Overlays/Video",
}

class AssetOrchestrator:
    def __init__(self, root_dir):
        self.root = Path(root_dir)
        if not self.root.exists():
            log.warning(f"⚠️ Target dir {root_dir} does not exist. Creating...")
            self.root.mkdir(parents=True, exist_ok=True)

    def organize(self):
        """Sorts loose files into Imperial categories."""
        log.info(f"🔍 Auditing {self.root}...")
        for item in self.root.iterdir():
            if item.is_file():
                ext = item.suffix.lower()
                if ext in MAPPING:
                    target_sub = self.root / MAPPING[ext]
                    target_sub.mkdir(parents=True, exist_ok=True)
                    log.info(f"🚚 Moving {item.name} -> {MAPPING[ext]}")
                    shutil.move(str(item), str(target_sub / item.name))

    def extract_and_sort(self, zip_path):
        """Extracts a ZIP and intelligently sorts its contents."""
        zip_p = Path(zip_path)
        if not zip_p.exists():
            log.error(f"❌ ZIP not found: {zip_path}")
            return
            
        extract_to = self.root / "_temp_extract"
        extract_to.mkdir(exist_ok=True)
        
        with zipfile.ZipFile(zip_p, 'r') as zip_ref:
            log.info(f"📦 Extracting {zip_p.name}...")
            zip_ref.extractall(extract_to)
            
        # Recursive Sort
        for p in extract_to.rglob('*'):
            if p.is_file():
                ext = p.suffix.lower()
                target_sub = self.root / MAPPING.get(ext, "Other/Unsorted")
                target_sub.mkdir(parents=True, exist_ok=True)
                shutil.move(str(p), str(target_sub / p.name))
        
        # Cleanup
        shutil.rmtree(extract_to)
        log.info(f"✅ Extraction and distribution of {zip_p.name} COMPLETE.")

if __name__ == "__main__":
    # Example usage for the Commander
    # orch = AssetOrchestrator("D:/Graphic Designer Resources")
    # orch.organize()
    pass
