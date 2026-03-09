"""
Felipe Gouveia Studio - Snapshot Tool
Gera um preview estático de um frame específico do Masterpiece V7.
"""
import bpy
import os

# Caminho do script Masterpiece V7 para pegar as mesmas configurações
V7_SCRIPT = r"D:\Blender\blenderscripts\scripts\commercials\nike_multiverse_v7_sales_power.py"

# Executar o setup da cena chamando as funções do script original
exec(open(V7_SCRIPT, encoding='utf-8').read())

# Configurar para renderizar apenas o FRAME 70 (The Reveal)
bpy.context.scene.frame_set(70)
output_snapshot = r"D:\Blender\blenderscripts\renders\drafts\V7_SNAPSHOT_FRAME_70.png"
bpy.context.scene.render.filepath = output_snapshot
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Renderizar 1 frame (Cycles)
print(f"🎬 [Snapshot] Renderizando Frame 70 em Alta Qualidade...")
bpy.ops.render.render(write_still=True)
print(f"✅ Snapshot salvo em: {output_snapshot}")
