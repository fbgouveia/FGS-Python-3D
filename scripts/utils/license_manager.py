# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: license_manager.py                                 ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝

Gerenciador de Tiers e Licenciamento Imperial.
Define as permissões de uso de GPU e qualidade de render.
"""

class ImperialTier:
    BASIC = "BASIC"      # Overlay 2D, Eevee, HD
    PRO = "PRO"          # Cinematic, 4K, Cycles (Medium)
    ENTERPRISE = "ENT"   # Ultra High, Max Samples, White Label

class LicenseManager:
    def __init__(self, key="FREE_TRIAL"):
        self.key = key
        self.tier = self._validate_tier()

    def _validate_tier(self):
        # Mock de validação - no futuro conectará com API Central Privada
        if self.key.startswith("PRO_"):
            return ImperialTier.PRO
        elif self.key.startswith("ENT_"):
            return ImperialTier.ENTERPRISE
        return ImperialTier.BASIC

    def can_use_cycles(self):
        return self.tier in [ImperialTier.PRO, ImperialTier.ENTERPRISE]

    def get_max_samples(self):
        if self.tier == ImperialTier.ENTERPRISE: return 1024
        if self.tier == ImperialTier.PRO: return 256
        return 64 # Eevee ou Cycles Low para Basic

    def get_max_resolution(self):
        if self.tier == ImperialTier.ENTERPRISE: return (3840, 2160)
        if self.tier == ImperialTier.PRO: return (1920, 1080)
        return (1280, 720)

    def is_white_label(self):
        return self.tier == ImperialTier.ENTERPRISE

    def audit_request(self, engine, resolution):
        """Verifica se o pedido de render está dentro do Tier pago."""
        if engine == 'CYCLES' and not self.can_use_cycles():
            print(f"⚠️ [LICENSE] Engine CYCLES bloqueado para Tier {self.tier}. Revertendo para EEVEE.")
            return False
            
        max_res = self.get_max_resolution()
        if resolution[0] > max_res[0] or resolution[1] > max_res[1]:
            print(f"⚠️ [LICENSE] Resolução ultrapassa limite do Tier {self.tier}. Revertendo para {max_res}.")
            return False
            
        return True

if __name__ == "__main__":
    mgr = LicenseManager("PRO_GOUVEIA_2026")
    print(f"Chave: {mgr.key} | Tier: {mgr.tier}")
    print(f"Samples Permitidos: {mgr.get_max_samples()}")
    print(f"Can use Cycles: {mgr.can_use_cycles()}")
