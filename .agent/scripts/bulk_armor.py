# -*- coding: utf-8 -*-
import os
import re

HEADER_TEMPLATE = """# -*- coding: utf-8 -*-
\"\"\"
╔══════════════════════════════════════════════════════════════╗
║   © 2026 FELIPE GOUVEIA STUDIO — PROPRIEDADE PRIVADA        ║
║   ADMINISTRAÇÃO: CLARA GOUVEIA | GOVERNANÇA: LORENA GOUVEIA ║
║   --------------------------------------------------------   ║
║   Script: {filename}                                        ║
║   Status: BLINDADO POR DIREITOS AUTORAIS                    ║
╚══════════════════════════════════════════════════════════════╝
\"\"\"
"""

def apply_armor(directory):
    for root, dirs, files in os.walk(directory):
        if "_archive" in root or "node_modules" in root or ".git" in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if "© 2026 FELIPE GOUVEIA STUDIO" in content:
                        print(f"Skipping (Already Armored): {file}")
                        continue
                    
                    # Remove existing shebang or encoding if we are going to replace it
                    content_clean = re.sub(r'^#\s*-\*-\s*coding:.*-\*-\s*\n', '', content)
                    content_clean = re.sub(r'^#!\/usr\/bin\/env python.*\n', '', content_clean)
                    
                    header = HEADER_TEMPLATE.format(filename=file)
                    new_content = header + "\n" + content_clean.lstrip()
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Armor Applied: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        target_dirs = [sys.argv[1]]
    else:
        target_dirs = [
            r"d:\Blender\blenderscripts\scripts",
            r"d:\Blender\blenderscripts"
        ]
        
    print(f"Starting Massive Armor Protocol...")
    for target in target_dirs:
        if os.path.exists(target):
            print(f"Armoring directory: {target}")
            apply_armor(target)
    
    # Manifest Armor (only if in main project)
    manifest_dir = r"d:\Blender\blenderscripts\manifests"
    if os.path.exists(manifest_dir) and (len(sys.argv) == 1 or "blenderscripts" in sys.argv[1]):
        import json
        for file in os.listdir(manifest_dir):
            if file.endswith(".json"):
                p = os.path.join(manifest_dir, file)
                try:
                    with open(p, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    data["_copyright"] = "© 2026 FELIPE GOUVEIA STUDIO - PROPRIEDADE PRIVADA - ADMINISTRAÇÃO CLARA GOUVEIA"
                    
                    with open(p, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4, ensure_ascii=False)
                    print(f"JSON Armored: {file}")
                except:
                    pass

    print("Done.")
