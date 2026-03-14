# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: smoke_test_render.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

"""
╔══════════════════════════════════════════════════════════════╗
║   FELIPE GOUVEIA STUDIO — Python 3D                         ║
║   Script: smoke_test_render.py                               ║
║   Função: Teste mínimo de render (GUI e headless)            ║
║   LAYER 1 — Task 1.1                                         ║
╚══════════════════════════════════════════════════════════════╝

USAGE (GUI — Blender Scripting tab):
    Paste and Run Script

USAGE (Headless — PowerShell):
    D:\Blender\blenderscripts\tools\blender\blender.exe -b -P D:\Blender\blenderscripts\scripts\tests\smoke_test_render.py

ACCEPTANCE CRITERIA:
    - File exists: renders/tests/smoke_test_YYYYMMDD_HHMMSS.png
    - File size > 10KB (not blank)
    - Exit code 0 (headless)
"""

import bpy
import os
import sys
import json
from datetime import datetime

# ── Output path ──────────────────────────────────────────────
OUTPUT_DIR  = "D:/Blender/blenderscripts/renders/tests"
TIMESTAMP   = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = f"{OUTPUT_DIR}/smoke_test_{TIMESTAMP}.png"
REPORT_FILE = f"{OUTPUT_DIR}/smoke_test_{TIMESTAMP}_report.json"

report = {
    "timestamp": TIMESTAMP,
    "status": "FAIL",
    "steps": [],
    "output_file": OUTPUT_FILE,
    "output_size_bytes": 0,
    "errors": []
}

def log(msg, ok=True):
    symbol = "✅" if ok else "❌"
    line = f"   {symbol} {msg}"
    print(line)
    report["steps"].append({"ok": ok, "msg": msg})

def fail(msg):
    log(msg, ok=False)
    report["errors"].append(msg)

# ─────────────────────────────────────────────────────────────
# STEP 1 — Ensure output directory exists
# ─────────────────────────────────────────────────────────────
print("\n🔥 FGS SMOKE TEST — Layer 1")
print("=" * 50)

os.makedirs(OUTPUT_DIR, exist_ok=True)
log(f"Output dir ready: {OUTPUT_DIR}")

# ─────────────────────────────────────────────────────────────
# STEP 2 — Clean scene
# ─────────────────────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
log("Scene cleared")

# ─────────────────────────────────────────────────────────────
# STEP 3 — Build minimal scene
# ─────────────────────────────────────────────────────────────

# Scene settings
scene = bpy.context.scene
scene.render.fps = 24
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.frame_start = 1
scene.frame_end = 1

# World background (dark gradient)
world = bpy.data.worlds.new("FGS_World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs["Color"].default_value = (0.02, 0.02, 0.05, 1.0)
    bg.inputs["Strength"].default_value = 0.5
log("Scene configured: 1280x720 @ 24fps, 1 frame")

# Object — FGS branded cube
mesh = bpy.data.meshes.new("FGS_Cube_Mesh")
obj  = bpy.data.objects.new("FGS_Cube", mesh)
scene.collection.objects.link(obj)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.mode_set(mode='OBJECT')

import bmesh
bm = bmesh.new()
bmesh.ops.create_cube(bm, size=1.5)
bm.to_mesh(mesh)
bm.free()
log("Object created: cube 1.5m")

# Material — metallic black (FGS signature)
mat = bpy.data.materials.new("FGS_Smoke_Metal")
mat.use_nodes = True
nodes = mat.node_tree.nodes
nodes.clear()
principled = nodes.new("ShaderNodeBsdfPrincipled")
output     = nodes.new("ShaderNodeOutputMaterial")
mat.node_tree.links.new(principled.outputs["BSDF"], output.inputs["Surface"])
principled.inputs["Base Color"].default_value  = (0.01, 0.01, 0.01, 1.0)
principled.inputs["Metallic"].default_value    = 1.0
principled.inputs["Roughness"].default_value   = 0.08
obj.data.materials.append(mat)
log("Material applied: FGS metallic black")

# Rotation for visual interest
obj.rotation_euler = (0.5, 0.3, 0.8)
bpy.ops.object.transform_apply(rotation=False)

# Key Light
key_data = bpy.data.lights.new("Key_Light", type='AREA')
key_data.energy = 800
key_data.size   = 3.0
key_obj  = bpy.data.objects.new("Key_Light", key_data)
scene.collection.objects.link(key_obj)
key_obj.location       = (4, -4, 5)
key_obj.rotation_euler = (0.8, 0.0, 0.8)

# Rim Light
rim_data = bpy.data.lights.new("Rim_Light", type='AREA')
rim_data.energy = 1200
rim_data.size   = 2.0
rim_data.color  = (0.4, 0.6, 1.0)
rim_obj  = bpy.data.objects.new("Rim_Light", rim_data)
scene.collection.objects.link(rim_obj)
rim_obj.location       = (-4, 3, 3)
rim_obj.rotation_euler = (-0.8, 0.0, -2.4)
log("Lights added: Key (800W area) + Rim (1200W blue area)")

# Camera
cam_data = bpy.data.cameras.new("FGS_Camera")
cam_data.lens = 85
cam_data.dof.use_dof = True
cam_data.dof.focus_object = obj
cam_data.dof.aperture_fstop = 2.8
cam_obj  = bpy.data.objects.new("FGS_Camera", cam_data)
scene.collection.objects.link(cam_obj)
cam_obj.location       = (4, -4, 2.5)
cam_obj.rotation_euler = (1.1, 0.0, 0.8)
scene.camera = cam_obj
log("Camera: 85mm, f/2.8 DOF")

# ─────────────────────────────────────────────────────────────
# STEP 4 — Configure render engine
# ─────────────────────────────────────────────────────────────

# Use EEVEE for speed (smoke test = prove pipeline, not quality)
scene.render.engine = 'BLENDER_EEVEE_NEXT'

# Output
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode  = 'RGB'
scene.render.filepath = OUTPUT_FILE

# GPU detection
try:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.get_devices()
    has_gpu = any(
        d.type in ('CUDA', 'OPTIX', 'HIP', 'METAL', 'ONEAPI')
        for d in prefs.devices
    )
    log(f"GPU detected: {has_gpu}")
except Exception as e:
    log(f"GPU check skipped: {e}", ok=True)

log(f"Render engine: EEVEE NEXT")
log(f"Output path: {OUTPUT_FILE}")

# ─────────────────────────────────────────────────────────────
# STEP 5 — Pre-render validation
# ─────────────────────────────────────────────────────────────

errors_found = 0

if not scene.camera:
    fail("No active camera set")
    errors_found += 1
else:
    log("Camera: active ✓")

objects_visible = [o for o in scene.objects if o.type == 'MESH']
if not objects_visible:
    fail("No mesh objects in scene")
    errors_found += 1
else:
    log(f"Mesh objects visible: {len(objects_visible)}")

lights_present = [o for o in scene.objects if o.type == 'LIGHT']
if not lights_present:
    fail("No lights in scene")
    errors_found += 1
else:
    log(f"Lights present: {len(lights_present)}")

if errors_found:
    print(f"\n❌ Pre-render validation FAILED ({errors_found} errors). Aborting.")
    report["status"] = "FAIL_PREVALIDATION"
    with open(REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=2)
    sys.exit(1)

log("Pre-render validation PASSED")

# ─────────────────────────────────────────────────────────────
# STEP 6 — RENDER
# ─────────────────────────────────────────────────────────────
print("\n🎬 Rendering...")
try:
    bpy.ops.render.render(write_still=True)
    log("bpy.ops.render.render() completed")
except Exception as e:
    fail(f"Render failed: {e}")
    report["status"] = "FAIL_RENDER"
    with open(REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=2)
    sys.exit(1)

# ─────────────────────────────────────────────────────────────
# STEP 7 — Post-render validation
# ─────────────────────────────────────────────────────────────
if not os.path.exists(OUTPUT_FILE):
    fail(f"Output file NOT found: {OUTPUT_FILE}")
    report["status"] = "FAIL_NO_OUTPUT"
    with open(REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=2)
    sys.exit(1)

file_size = os.path.getsize(OUTPUT_FILE)
report["output_size_bytes"] = file_size

MIN_SIZE = 10_000  # 10KB — if less, it's likely blank/black
if file_size < MIN_SIZE:
    fail(f"Output too small ({file_size} bytes) — likely blank render")
    report["status"] = "FAIL_BLANK_OUTPUT"
    with open(REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=2)
    sys.exit(1)

log(f"Output file exists: {file_size:,} bytes ✓")

# ─────────────────────────────────────────────────────────────
# STEP 8 — SUCCESS
# ─────────────────────────────────────────────────────────────
report["status"] = "PASS"
with open(REPORT_FILE, 'w') as f:
    json.dump(report, f, indent=2)

print("\n" + "=" * 50)
print("✅ SMOKE TEST PASSED")
print(f"   Output : {OUTPUT_FILE}")
print(f"   Size   : {file_size:,} bytes")
print(f"   Report : {REPORT_FILE}")
print("=" * 50)
