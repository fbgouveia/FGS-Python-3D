import bpy
eevee = bpy.context.scene.eevee
print("--- START EEVEE ---")
for p in dir(eevee):
    if not p.startswith("_"):
        print(p)
print("--- END EEVEE ---")
