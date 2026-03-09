import socket
import json

def send_blender_command(command):
    host = 'localhost'
    port = 9876
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(json.dumps(command).encode('utf-8'))
            response = s.recv(8192)
            return json.loads(response.decode('utf-8'))
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Test command
cmd = {
    "type": "execute_code",
    "params": {
        "code": "import bpy; print('MCP Connection Active'); bpy.data.objects['Cube'].location.z += 1.0"
    }
}

print(json.dumps(send_blender_command(cmd), indent=2))
