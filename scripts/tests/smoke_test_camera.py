# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: smoke_test_camera.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import sys
import bpy

# Setup paths
UTILS_PATH = "D:/Blender/blenderscripts/scripts/utils"
if UTILS_PATH not in sys.path:
    sys.path.append(UTILS_PATH)

try:
    from camera_system import CameraSystem
    print("✅ CameraSystem imported successfully.")
    
    # Simple smoke test
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cam_sys = CameraSystem()
    
    # Test 'criar'
    cam1 = cam_sys.criar("TEST_CAM_1", posicao=(0, -5, 2))
    print(f"✅ Camera 'criar' works: {cam1.name}")
    
    # Test 'criar_camera' (the bug fix)
    cam2 = cam_sys.criar_camera("TEST_CAM_2", posicao=(5, 0, 2))
    print(f"✅ Camera 'criar_camera' alias works: {cam2.name}")
    
    if "TEST_CAM_2" in bpy.data.objects:
        print("🚀 SMOKE TEST PASSED: Camera attribute bug resolved.")
    else:
        print("❌ SMOKE TEST FAILED: Camera object not found.")
        sys.exit(1)

except Exception as e:
    print(f"❌ SMOKE TEST FAILED: Exception: {e}")
    sys.exit(1)
