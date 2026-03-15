# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: bridge_engine.py                                  ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝

Imperial Bridge Engine – Heart of deterministic scene execution.
"""

import json
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
import bpy
from typing import Dict, Any, List

# Local utilities
try:
    from .animation_engine import AnimationEngine
    from .scene_factory import SceneFactory
    from .audio_manager import AudioManager
    from .character_factory import CharacterFactory
    from .materials_library import MaterialLibrary
    from .scene_setup import (
        setup_scene,
        adicionar_luz_sol,
        adicionar_iluminacao_3_pontos,
        configurar_camera_padrao,
        limpar_cena,
    )
    from .lighthouse_3d import Lighthouse3D
    from .license_manager import LicenseManager
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from animation_engine import AnimationEngine
    from scene_factory import SceneFactory
    from audio_manager import AudioManager
    from character_factory import CharacterFactory
    from materials_library import MaterialLibrary
    from scene_setup import (
        setup_scene,
        adicionar_luz_sol,
        adicionar_iluminacao_3_pontos,
        configurar_camera_padrao,
        limpar_cena,
    )
    from lighthouse_3d import Lighthouse3D
    from license_manager import LicenseManager

def _validate_manifest(manifest: dict) -> None:
    required_top = {"metadata", "scene", "characters"}
    missing = required_top - manifest.keys()
    if missing:
        raise ValueError(f"Missing required top-level keys: {missing}")

class BridgeEngine:
    def __init__(self, manifest_path: str):
        self.manifest_path = Path(manifest_path).resolve()
        self.manifest = None
        self.license_mgr = None
        self.log_path = self.manifest_path.with_name(f"{self.manifest_path.stem}_log.json")
        self.logger = {
            "created_characters": [],
            "applied_animations": [],
            "status": "initialized",
            "quality_score": 0,
            "render_engine": "",
            "tier": "UNKNOWN"
        }

    def load_manifest(self):
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)
        _validate_manifest(self.manifest)
        
        meta = self.manifest.get("metadata", {})
        license_key = meta.get("license_key", "FREE_TRIAL")
        self.license_mgr = LicenseManager(license_key)
        
        self.logger["load_time"] = datetime.utcnow().isoformat() + "Z"
        self.logger["status"] = "manifest_loaded"
        self.logger["tier"] = self.license_mgr.tier

    def execute(self):
        if self.manifest is None:
            self.load_manifest()

        print(f"🚀 [CLARA GOUVEIA] Administrando Manifesto: {self.manifest['metadata']['project_name']}")
        limpar_cena()

        scene_cfg = self.manifest["scene"]
        engine_name = scene_cfg.get("engine", "EEVEE").upper()
        res_x = scene_cfg.get("resolution_x", 1920)
        res_y = scene_cfg.get("resolution_y", 1080)

        # License Audit
        if not self.license_mgr.audit_request(engine_name, (res_x, res_y)):
            engine_name = "EEVEE" if not self.license_mgr.can_use_cycles() else engine_name
            max_res = self.license_mgr.get_max_resolution()
            res_x, res_y = min(res_x, max_res[0]), min(res_y, max_res[1])

        setup_scene(
            fps=scene_cfg.get("fps", 24),
            resolucao_x=res_x,
            resolucao_y=res_y,
            duracao_segundos=scene_cfg["duration_seconds"]
        )
        
        bpy.context.scene.render.engine = engine_name
        self.logger["render_engine"] = engine_name

        mat_lib = MaterialLibrary()
        scene_factory = SceneFactory(mat_lib)
        env_cfg = self.manifest.get("environment", {})
        if env_cfg:
            scene_factory.criar(env_cfg.get("type", "void"), **env_cfg.get("params", {}))

        factory = CharacterFactory(mat_lib)
        anim_engine = AnimationEngine()

        # Dispatcher: mapeia tipo de animação → método correto do AnimationEngine
        _ANIM = {
            "mover":               lambda o, p: anim_engine.mover(o, **p),
            "rotacionar":          lambda o, p: anim_engine.rotacionar(o, **p),
            "escalar":             lambda o, p: anim_engine.escalar(o, **p),
            "flutuar":             lambda o, p: anim_engine.flutuar(o, **p),
            "tremer":              lambda o, p: anim_engine.tremer(o, **p),
            "respiracao":          lambda o, p: anim_engine.respiracao(o, **p),
            "orbitar":             lambda o, p: anim_engine.orbitar(o, **p),
            "cair_kikando":        lambda o, p: anim_engine.cair_kikando(o, **p),
            "caminhar_procedural": lambda o, p: anim_engine.caminhar_procedural(o, **p),
        }

        for char in self.manifest["characters"]:
            obj = factory.criar(
                nome=char["name"],
                tipo=char.get("type", "animal"),
                **char.get("params", {})
            )
            if obj:
                self.logger["created_characters"].append(char["name"])
                for anim in char.get("animations", []):
                    anim_type = anim["type"]
                    anim_fn = _ANIM.get(anim_type)
                    if anim_fn:
                        anim_fn(obj, anim.get("params", {}))
                        self.logger["applied_animations"].append(f"{char['name']}:{anim_type}")
                    else:
                        print(f"⚠️ [Bridge] Animação desconhecida: '{anim_type}'")

        # 4. Final Quality Audit
        audit = Lighthouse3D()
        passed, score = audit.audit_scene()
        self.logger["quality_score"] = score
        
        if not passed:
            audit.harden_render()

        # 5. Memory Cleanup (Imperial Hardening)
        # Removes orphaned data (meshes, materials, images) from RAM
        bpy.data.orphans_purge()
        print("🧹 [Bridge Engine] Orfãos purgados. VRAM protegida.")

        self.logger["status"] = "execution_finished"
        self._save_log()

    def _save_log(self):
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(self.logger, f, indent=4)
        print(f"📄 Log salvo em: {self.log_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        engine = BridgeEngine(sys.argv[1])
        engine.execute()
