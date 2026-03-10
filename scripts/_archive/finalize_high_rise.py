import socket
import json

def send_blender_command(command):
    host = 'localhost'
    port = 9876
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(json.dumps(command).encode('utf-8'))
            response = s.recv(16384)
            return json.loads(response.decode('utf-8'))
    except Exception as e:
        return {"status": "error", "message": str(e)}

sky_fix = r'''
import bpy

# Set up Sky Texture for professional world lighting
if not bpy.context.scene.world:
    bpy.data.worlds.new("World")
    bpy.context.scene.world = bpy.data.worlds["World"]

world = bpy.context.scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links

nodes.clear()
node_sky = nodes.new(type='ShaderNodeSkyTexture')
node_sky.sky_type = 'NISHITA'
node_sky.sun_elevation = 0.2
node_sky.sun_rotation = 1.2
node_sky.location = (-300, 0)

node_output = nodes.new(type='ShaderNodeOutputWorld')
node_output.location = (0, 0)

links.new(node_sky.outputs['Color'], node_output.inputs['Surface'])

# Final Viewport Update
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces[0].shading.type = 'RENDERED'
'''

send_blender_command({"type": "execute_code", "params": {"code": sky_fix}})

# Capture Final Result Screenshot
screenshot_path = r"D:\Blender\blenderscripts\renders\high_rise_final_v1.png"
send_blender_command({
    "type": "get_viewport_screenshot", 
    "params": {"filepath": screenshot_path, "max_size": 1024}
})

print(f"Sky finalized. Final render saved to {screenshot_path}")
