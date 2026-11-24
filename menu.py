import re

from temas.metodos_numericos import AnalisisNumerico
from temas.clases_objetos import demostrar_clases_objetos
from temas.herencia import demostrar_herencia
from temas.metodos_raices import MetodosRaices


def leer_float(mensaje):
    while True:
        try:
            return float(input(mensaje).strip())
        except ValueError:
            print("Entrada invalida. Ingrese un numero real.")


def leer_lista_numeros(mensaje):
    while True:
        entrada = input(mensaje).strip()
        try:
            valores = [float(valor) for valor in re.split(r"[\s,]+", entrada) if valor]
            if not valores:
                raise ValueError
            return valores
        except ValueError:
            print("Entrada invalida. Ingrese numeros separados por comas o espacios.")


def leer_datos_interpolacion():
    x_puntos = leer_lista_numeros("Ingrese los valores x (separados por comas): ")
    y_puntos = leer_lista_numeros("Ingrese los valores y (separados por comas): ")
    if len(x_puntos) != len(y_puntos):
        raise ValueError("Debe ingresar la misma cantidad de valores x e y.")
    return x_puntos, y_puntos


def leer_sistema():
    while True:
        try:
            dimension = int(input("Ingrese la dimension de la matriz A: ").strip())
            if dimension <= 0:
                raise ValueError
            break
        except ValueError:
            print("La dimension debe ser un entero positivo.")

    matriz = []
    for indice in range(dimension):
        while True:
            fila = leer_lista_numeros(
                f"Ingrese la fila {indice + 1} de A ({dimension} valores): "
            )
            if len(fila) == dimension:
                matriz.append(fila)
                break
            print(f"La fila debe contener exactamente {dimension} valores.")

    while True:
        vector = leer_lista_numeros(f"Ingrese el vector b ({dimension} valores): ")
        if len(vector) == dimension:
            return matriz, vector
        print(f"El vector b debe tener exactamente {dimension} valores.")


def mostrar_demostracion(solver):
    x_datos = [1.0, 2.0, 3.0, 4.0]
    y_datos = [1.0, 4.0, 9.0, 16.0]
    punto = 2.5

    print("\n--- DEMOSTRACION DE METODOS NUMERICOS ---")
    print(f"Lagrange: {solver.lagrange(x_datos, y_datos, punto):.6f}")

    raiz, iteraciones = solver.newton_raphson(
        lambda x: x**2 - 5, lambda x: 2 * x, 2.0
    )
    print(f"Newton-Raphson: raiz={raiz:.6f}, iteraciones={iteraciones}")

    resultado, coeficientes = solver.diferencias_divididas(
        x_datos, y_datos, punto
    )
    print(
        f"Diferencias divididas: {resultado:.6f}, "
        f"coeficientes={coeficientes}"
    )

    pendiente, ordenada, estimado = solver.minimos_cuadrados(
        [1, 2, 3, 4, 5], [2.1, 3.9, 6.2, 8.0, 9.9], x_eval=6.0
    )
    print(
        f"Minimos cuadrados: y = {pendiente:.4f}x + ({ordenada:.4f}), "
        f"y(6)={estimado:.4f}"
    )

    matriz = [
        [10.0, -1.0, 2.0],
        [-1.0, 11.0, -1.0],
        [2.0, -1.0, 10.0],
    ]
    vector = [6.0, 25.0, -11.0]
    solucion, iteraciones = solver.gauss_seidel(matriz, vector)
    print(
        f"Gauss-Seidel: {[round(valor, 6) for valor in solucion]} "
        f"({iteraciones} iteraciones)"
    )

    solucion, iteraciones = solver.jacobi(matriz, vector)
    print(
        f"Jacobi: {[round(valor, 6) for valor in solucion]} "
        f"({iteraciones} iteraciones)"
    )


def menu():
    solver = AnalisisNumerico(tolerancia=1e-6, max_iter=100)
    solver_raices = MetodosRaices(max_iter=100)
    acciones_raices = {
        "1": solver_raices.biseccion,
        "2": solver_raices.punto_fijo,
        "3": solver_raices.falsa_posicion,
        "4": solver_raices.newton_raphson,
        "5": solver_raices.secante,
    }

    while True:
        print("\n==== MENU PRINCIPAL - ANALISIS NUMERICO ====")
        print("1. Metodo de biseccion")
        print("2. Metodo de punto fijo")
        print("3. Metodo de falsa posicion")
        print("4. Newton-Raphson (funcion ingresada)")
        print("5. Metodo de la secante")
        print("6. Interpolacion de Lagrange")
        print("7. Newton-Raphson (ejemplo x^2 - 5)")
        print("8. Diferencias divididas de Newton")
        print("9. Minimos cuadrados")
        print("10. Gauss-Seidel")
        print("11. Jacobi")
        print("12. Demostracion de clases, objetos y herencia")
        print("13. Ejecutar demostracion numerica completa")
        print("14. Salir")

        try:
            opcion = input("Seleccione una opcion: ").strip()
            if opcion in acciones_raices:
                acciones_raices[opcion]()
            elif opcion == "6":
                x_puntos, y_puntos = leer_datos_interpolacion()
                x_eval = leer_float("Ingrese el valor de x a evaluar: ")
                resultado = solver.lagrange(x_puntos, y_puntos, x_eval)
                print(f"Resultado de Lagrange: {resultado:.6f}")
            elif opcion == "7":
                x0 = leer_float("Ingrese el valor inicial x0: ")
                raiz, iteraciones = solver.newton_raphson(
                    lambda x: x**2 - 5, lambda x: 2 * x, x0
                )
                print(f"Raiz aproximada: {raiz:.6f}")
                print(f"Iteraciones: {iteraciones}")
            elif opcion == "8":
                x_puntos, y_puntos = leer_datos_interpolacion()
                x_eval = leer_float("Ingrese el valor de x a evaluar: ")
                resultado, coeficientes = solver.diferencias_divididas(
                    x_puntos, y_puntos, x_eval
                )
                print(f"Resultado: {resultado:.6f}")
                print(f"Coeficientes: {coeficientes}")
            elif opcion == "9":
                x_puntos, y_puntos = leer_datos_interpolacion()
                x_eval = leer_float("Ingrese el valor de x para predecir: ")
                pendiente, ordenada, estimado = solver.minimos_cuadrados(
                    x_puntos, y_puntos, x_eval=x_eval
                )
                print(f"Pendiente m: {pendiente:.6f}")
                print(f"Ordenada al origen b: {ordenada:.6f}")
                print(f"Valor estimado: {estimado:.6f}")
            elif opcion in ("10", "11"):
                matriz, vector = leer_sistema()
                metodo = solver.gauss_seidel if opcion == "10" else solver.jacobi
                solucion, iteraciones = metodo(matriz, vector)
                nombre = "Gauss-Seidel" if opcion == "10" else "Jacobi"
                print(f"Solucion por {nombre}: {[round(v, 6) for v in solucion]}")
                print(f"Iteraciones: {iteraciones}")
            elif opcion == "12":
                demostrar_clases_objetos()
                demostrar_herencia()
            elif opcion == "13":
                mostrar_demostracion(solver)
            elif opcion == "14":
                print("Saliendo del programa.")
                return
            else:
                print("Opcion no valida. Seleccione un numero del 1 al 14.")
        except (EOFError, KeyboardInterrupt):
            print("\nEjecucion finalizada.")
            return
        except (ValueError, ZeroDivisionError) as error:
            print(f"Error: {error}")
