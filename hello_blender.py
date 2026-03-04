import bpy

def main():
    # Exemplo simples: Adiciona um cubo à cena
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    print("Cubo adicionado com sucesso!")

if __name__ == "__main__":
    main()
