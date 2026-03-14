# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: portfolio_builder.py                              ║
║   Status: MARKETING AUTOMATOR | BLINDADO                   ║
╚══════════════════════════════════════════════════════════════╝

Gerador de Portfólio Imperial.
Cria variações automáticas de um produto em múltiplos cenários cinemáticos.
"""

import os
import sys
import json

# Path injection for local imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

class PortfolioBuilder:
    def __init__(self, asset_name, asset_type="PRODUCT"):
        self.asset_name = asset_name
        self.asset_type = asset_type
        self.output_dir = r"d:\Blender\blenderscripts\manifests\portfolio"
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_showcase(self):
        """Gera uma lista de manifestos para diferentes estilos de reveal."""
        templates = [
            {"type": "luxury_showroom", "engine": "CYCLES", "samples": 256},
            {"type": "product_studio", "engine": "CYCLES", "params": {"tipo": "gradiente"}},
            {"type": "cyberpunk_street", "engine": "EEVEE", "params": {"extensao": 20}},
            {"type": "abstract_dark", "engine": "CYCLES", "samples": 512}
        ]
        
        manifests = []
        for i, t in enumerate(templates):
            manifest = {
                "metadata": {
                    "project_name": f"Portfolio_{self.asset_name}_{t['type']}",
                    "license_key": "ENT_GOUVEIA_MARKETING"
                },
                "scene": {
                    "duration_seconds": 10,
                    "fps": 24,
                    "engine": t["engine"],
                    "resolution_x": 1920,
                    "resolution_y": 1080
                },
                "environment": {
                    "type": t["type"],
                    "params": t.get("params", {})
                },
                "characters": [
                    {
                        "name": self.asset_name,
                        "type": self.asset_type,
                        "animations": [
                            {"type": "orbita_360", "params": {"velocidade": 1.0}}
                        ]
                    }
                ]
            }
            
            file_path = os.path.join(self.output_dir, f"{self.asset_name}_v{i}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=4)
            
            manifests.append(file_path)
            print(f"✨ [Portfolio] Manifesto gerado: {file_path}")
            
        return manifests

if __name__ == "__main__":
    builder = PortfolioBuilder("Luxury_Watch_X")
    builder.generate_showcase()
