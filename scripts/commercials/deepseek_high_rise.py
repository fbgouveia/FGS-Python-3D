# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: deepseek_high_rise.py                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import socket
import json

def send_blender_command(command):
    host = 'localhost'
    port = 9876
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(json.dumps(command).encode('utf-8'))
            response = s.recv(65536)
            return json.loads(response.decode('utf-8'))
    except Exception as e:
        return {"status": "error", "message": str(e)}

high_rise_script = r'''
import bpy
import bmesh
import random

# --- 1. CLEANUP ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# --- 2. MATERIALS SETUP ---
def create_pbr_material(name, color=(0.8, 0.8, 0.8, 1), metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    # Set standard parameters (Blender 4.0+ nodes names)
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Metallic'].default_value = metallic
        bsdf.inputs['Roughness'].default_value = roughness
    return mat

mat_concrete = create_pbr_material("FGS_Concrete", (0.2, 0.2, 0.2, 1), 0.0, 0.8)
mat_glass = create_pbr_material("FGS_Glass", (0.5, 0.7, 1.0, 1), 0.9, 0.05)
mat_metal = create_pbr_material("FGS_Metal", (0.7, 0.7, 0.7, 1), 1.0, 0.2)

# --- 3. MODULAR FLOOR GENERATOR ---
def create_floor(z_offset, floor_id):
    # Main Slab
    bpy.ops.mesh.primitive_cube_add(size=1, scale=(10, 10, 0.2), location=(0, 0, z_offset))
    slab = bpy.context.active_object
    slab.name = f"Floor_Slab_{floor_id}"
    slab.data.materials.append(mat_concrete)
    
    # Pillars
    pillar_locs = [(4.5, 4.5), (-4.5, 4.5), (4.5, -4.5), (-4.5, -4.5)]
    for i, loc in enumerate(pillar_locs):
        bpy.ops.mesh.primitive_cube_add(size=1, scale=(0.5, 0.5, 3), location=(loc[0], loc[1], z_offset + 1.5))
        pillar = bpy.context.active_object
        pillar.name = f"Pillar_{floor_id}_{i}"
        pillar.data.materials.append(mat_concrete)
        pillar.parent = slab
    
    # Windows (Glass Panes)
    # Side 1 (Front)
    bpy.ops.mesh.primitive_cube_add(size=1, scale=(9, 0.1, 2.5), location=(0, 4.8, z_offset + 1.5))
    window = bpy.context.active_object
    window.name = f"Window_Front_{floor_id}"
    window.data.materials.append(mat_glass)
    window.parent = slab
    
    # Frame detailing
    bpy.ops.mesh.primitive_cube_add(size=1, scale=(0.2, 0.2, 2.5), location=(0, 4.9, z_offset + 1.5))
    frame = bpy.context.active_object
    frame.data.materials.append(mat_metal)
    frame.parent = window

# --- 4. BUILD THE HIGH-RISE ---
num_floors = 15
for f in range(num_floors):
    create_floor(f * 3, f)

# --- 5. MECHANICAL ROOF ---
z_top = num_floors * 3
bpy.ops.mesh.primitive_cube_add(size=1, scale=(10, 10, 0.5), location=(0, 0, z_top))
roof = bpy.context.active_object
roof.name = "Roof_Top"
roof.data.materials.append(mat_concrete)

# Detail: Vents
for i in range(4):
    bpy.ops.mesh.primitive_cube_add(size=1, scale=(2, 2, 1.5), location=(random.uniform(-3,3), random.uniform(-3,3), z_top + 1))
    vent = bpy.context.active_object
    vent.data.materials.append(mat_metal)
    vent.parent = roof

# --- 6. PAVILION NEXT TO IT ---
bpy.ops.mesh.primitive_cube_add(size=1, scale=(10, 10, 0.2), location=(20, 0, 0))
pav_base = bpy.context.active_object
pav_base.name = "Pavilion_Base"
pav_base.data.materials.append(mat_concrete)

# Open Columns for Pavilion
for x in [-4, 4]:
    for y in [-4, 4]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=5, location=(20+x, y, 2.5))
        col = bpy.context.active_object
        col.data.materials.append(mat_metal)
        col.parent = pav_base

# --- 7. CAMERA & LIGHTS ---
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0,0, z_top / 2))
target = bpy.context.active_object

bpy.ops.object.camera_add(location=(-30, -30, z_top + 10))
cam = bpy.context.active_object
cam.data.lens = 35
constr = cam.constraints.new(type='TRACK_TO')
constr.target = target
bpy.context.scene.camera = cam

# Sun Light
bpy.ops.object.light_add(type='SUN', location=(10, 10, 50))
sun = bpy.context.active_object
sun.data.energy = 5
sun.rotation_euler = (0.7, 0, 0.7)

# --- 8. VIEWPORT SYNC (Safe) ---
try:
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].shading.type = 'RENDERED'
            with bpy.context.temp_override(area=area):
                bpy.ops.view3d.view_all(center=True)
except Exception as e:
    print(f"Viewport sync skipped: {e}")
'''

print("Executing DeepSeek-Style High-Rise Construction...")
response = send_blender_command({"type": "execute_code", "params": {"code": high_rise_script}})
print(json.dumps(response, indent=2))
