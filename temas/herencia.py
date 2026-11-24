from temas.clases_objetos import Figura


class Circulo(Figura):
    def __init__(self, radio):
        super().__init__("circulo")
        self.radio = radio

    def describir(self):
        return f"{super().describir()} con radio {self.radio}"

    def calcular_area(self):
        return 3.141592653589793 * self.radio**2


def demostrar_herencia():
    circulo = Circulo(3)
    print("\n--- HERENCIA Y SUPER() ---")
    print(circulo.describir())
    print(f"Area: {circulo.calcular_area():.2f}")
