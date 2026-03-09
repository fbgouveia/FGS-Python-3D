import bpy
import sys
import os

print("--- FGS BROKER TEST ---")
print(f"Python Version: {sys.version}")
print(f"Current Dir: {os.getcwd()}")
print(f"Script Path: {__file__}")

# Test adding path
UTILS_DIR = r"d:\Blender\blenderscripts\scripts\utils"
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

print(f"Path added: {UTILS_DIR in sys.path}")

try:
    import scene_setup
    print("✅ scene_setup imported!")
except Exception as e:
    print(f"❌ Error importing scene_setup: {e}")

print("--- END TEST ---")
