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

Purpose
-------
* Load a high-fidelity JSON manifesto.
* Validate it against a minimal schema.
* Build characters through CharacterFactory.
* Apply animation blocks (head_bob, risada, rotation, location).
* Configure the render engine, resolution, FPS and duration.
* Emit a concise execution log (JSON) for audit & debugging.

Author : @nvidia – Imperial Core Governor
Created: 2026-03-14
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
except ImportError:
    # Fallback for direct execution or different path structures
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

def _validate_manifest(manifest: dict) -> None:
    """Light-weight validation of the manifest structure."""
    required_top = {"metadata", "scene", "characters"}
    missing = required_top - manifest.keys()
    if missing:
        raise ValueError(f"Missing required top-level keys: {missing}")

    if "project_name" not in manifest["metadata"]:
        raise ValueError("metadata.project_name is mandatory")

    if "duration_seconds" not in manifest["scene"]:
        raise ValueError("scene.duration_seconds is mandatory")
    
    if not isinstance(manifest["characters"], list):
        raise ValueError("characters must be a list")

class BridgeEngine:
    """Deterministic execution engine for Imperial 3D manifests."""

    def __init__(self, manifest_path: str):
        self.manifest_path = Path(manifest_path).resolve()
        self.manifest = None
        self.log_path = self.manifest_path.with_name(f"{self.manifest_path.stem}_log.json")
        self.logger: Dict[str, Any] = {
            "created_characters": [],
            "applied_animations": [],
            "warnings": [],
            "status": "initialized",
            "audio_applied": False,
            "quality_score": 0,
            "render_engine": ""
        }

    def load_manifest(self):
        """Read and parse the JSON manifesto."""
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)
        _validate_manifest(self.manifest)
        self.logger["load_time"] = datetime.utcnow().isoformat() + "Z"
        self.logger["status"] = "manifest_loaded"

    def execute(self):
        """High-level orchestration of scene building."""
        if self.manifest is None:
            self.load_manifest()

        # Type assertion for Pyre
        assert self.manifest is not None

        print(f"🚀 [CLARA GOUVEIA] Administrando Manifesto: {self.manifest['metadata']['project_name']}")

        # 0. Clean scene
        limpar_cena()

        # 1. Global Scene Setup
        scene_cfg = self.manifest["scene"]
        setup_scene(
            fps=scene_cfg.get("fps", 24),
            resolucao_x=scene_cfg.get("resolution_x", 1920),
            resolucao_y=scene_cfg.get("resolution_y", 1080),
            duracao_segundos=scene_cfg["duration_seconds"]
        )
        
        engine_name = scene_cfg.get("engine", "EEVEE").upper()
        bpy.context.scene.render.engine = engine_name
        self.logger["render_engine"] = engine_name

        # 2. Build Environment
        mat_lib = MaterialLibrary()
        scene_factory = SceneFactory(mat_lib)
        env_cfg = self.manifest.get("environment", {})
        if env_cfg:
            tipo_env = env_cfg.get("type", "void")
            print(f"   🏙️ Building Environment: {tipo_env}")
            scene_factory.criar_cenario(tipo_env, **env_cfg.get("params", {}))
            self.logger["environment"] = tipo_env

        # 3. Build Characters
        factory = CharacterFactory(mat_lib)
        anim_engine = AnimationEngine()
        created_chars = {}

        for char in self.manifest["characters"]:
            name = char["name"]
            preset = char["preset"]
            pos = tuple(char.get("position", (0, 0, 0)))
            
            # Additional overrides
            overrides = char.get("overrides", {})
            
            # Build using preset or direct creation
            if preset.upper() == "MAESTRE_HERO":
                objs = factory.criar_master_hero(posicao=pos, **overrides)
            else:
                objs = factory.criar_preset(preset, posicao=pos, **overrides)
            
            created_chars[name] = objs
            self.logger["created_characters"].append(name)

        # 3. Apply Animation Specs
        for anim in self.manifest.get("animations", []):
            target = anim["target"]
            atype = anim["type"]
            start = anim.get("start_frame", 1)
            end = anim.get("end_frame", int(scene_cfg["duration_seconds"] * scene_cfg.get("fps", 24)))
            params = anim.get("params", {})

            if target not in created_chars:
                self.logger["warnings"].append(f"Animation target '{target}' not found.")
                continue

            if atype == "head_bob":
                factory.head_bob(nome=target, frame_inicio=start, frame_fim=end, **params)
            elif atype == "risada":
                factory.risada(nome=target, frame_inicio=start, **params)
            elif atype == "caminhar":
                obj = bpy.data.objects.get(target)
                anim_engine.caminhar_procedural(obj, **params)
            elif atype == "orbitar":
                obj = bpy.data.objects.get(target)
                alvo = tuple(params.get("look_at", (0,0,0)))
                raio = params.get("radius", 5.0)
                altura = params.get("height", 2.0)
                anim_engine.orbitar(obj, alvo, raio, altura, frame_inicio=start, frame_fim=end)
            
            self.logger["applied_animations"].append({"target": target, "type": atype})

        # 5. Audio
        audio_cfg = self.manifest.get("audio", {})
        if audio_cfg:
            audio_manager = AudioManager()
            bgm = audio_cfg.get("bgm")
            if bgm:
                audio_manager.adicionar_bgm(
                    bgm["path"], 
                    volume=bgm.get("volume", 0.5),
                    fade_in=bgm.get("fade_in", 2.0),
                    fade_out=bgm.get("fade_out", 2.0)
                )
            
            for sfx in audio_cfg.get("sfx", []):
                audio_manager.adicionar_sfx(
                    sfx["path"],
                    frame_inicio=sfx.get("frame", 1),
                    volume=sfx.get("volume", 1.0)
                )
            self.logger["audio_applied"] = True

        # 4. Camera & Lights
        adicionar_iluminacao_3_pontos()
        cam_cfg = self.manifest.get("camera", {})
        configurar_camera_padrao(
            posicao=tuple(cam_cfg.get("position", (0, -5, 2))),
            alvo=tuple(cam_cfg.get("look_at", (0, 0, 1))),
            fov_graus=cam_cfg.get("fov", 45)
        )

        # 6. Quality Audit (Lighthouse 3D)
        lh = Lighthouse3D()
        approved, score = lh.audit_scene()
        self.logger["quality_score"] = score
        
        if not approved:
            lh.harden_render()
            _, score_new = lh.audit_scene()
            self.logger["quality_score_hardened"] = score_new

        # 7. Finalize
        self.logger["status"] = "execution_completed"
        self.logger["timestamp_utc"] = datetime.utcnow().isoformat() + "Z"
        
        with open(self.log_path, "w", encoding="utf-8") as log_f:
            json.dump(self.logger, log_f, indent=2)
        
        print(f"✅ Bridge Execution Finished. Log: {self.log_path}")

def main():
    if len(sys.argv) > 1:
        manifest_path = sys.argv[1]
    else:
        # Default for testing
        manifest_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "manifests", "test_scene.json")
    
    if os.path.exists(manifest_path):
        engine = BridgeEngine(manifest_path)
        engine.execute()
    else:
        print(f"❌ Manifest not found: {manifest_path}")

if __name__ == "__main__":
    main()
