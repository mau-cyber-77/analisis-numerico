class Figura:
    def __init__(self, nombre):
        self.nombre = nombre

    def describir(self):
        return f"Figura: {self.nombre}"


def demostrar_clases_objetos():
    figura = Figura("figura base")
    print("\n--- CLASES, OBJETOS Y METODOS ---")
    print(figura.describir())
