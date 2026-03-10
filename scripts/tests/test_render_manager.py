import sys
import bpy

sys.path.append("D:/Blender/blenderscripts/scripts/utils")
from render_manager import RenderManager

def test_presets():
    print("\n--- TEST RENDER MANAGER HEADLESS ---")
    rm = RenderManager()
    presets = ['draft', 'youtube', 'short_reel', 'comercial', 'cinema', 'print', 'animatic', 'tiktok', 'instagram_quad']
    
    for p in presets:
        try:
            rm.preset(p)
            print(f"✅ Preset {p} applied successfully.")
        except Exception as e:
            print(f"❌ Preset {p} FAILED: {e}")

if __name__ == "__main__":
    test_presets()
