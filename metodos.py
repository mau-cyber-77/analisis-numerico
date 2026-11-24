import sympy as sp
from tabulate import tabulate

x = sp.symbols("x")
MAX_ITERACIONES = 100


def evaluar(f_expr, x_val):
    """Evalúa la expresión simbólica f_expr en x_val."""
    return float(f_expr.subs(x, x_val).evalf())


def calcular_error(nuevo, anterior):
    """Calcula el error relativo aproximado sin dividir entre cero."""
    if nuevo == 0:
        return abs(nuevo - anterior)
    return abs((nuevo - anterior) / nuevo)


def imprimir_tabla(encabezados, filas):
    print("\n" + tabulate(
        filas, headers=encabezados, tablefmt="fancy_grid", floatfmt=".6f"
    ))


def validar_intervalo(f_expr, xi, xd):
    """Valida el intervalo y retorna f(xi), f(xd), o (None, None) si falla."""
    if xi >= xd:
        print("Error: xi debe ser menor que xd.")
        return None, None

    try:
        fxi = evaluar(f_expr, xi)
        fxd = evaluar(f_expr, xd)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        print(f"Error al evaluar la función: {error}")
        return None, None

    if fxi == 0:
        print(f"La raíz es xi = {xi}")
        return fxi, fxd
    if fxd == 0:
        print(f"La raíz es xd = {xd}")
        return fxi, fxd
    if fxi * fxd > 0:
        print("Error: La función no cambia de signo en el intervalo [xi, xd].")
        return None, None
    return fxi, fxd


def biseccion(f_expr, xi, xd, tol):
    fxi, fxd = validar_intervalo(f_expr, xi, xd)
    if fxi is None:
        return None
    if fxi == 0:
        return xi
    if fxd == 0:
        return xd

    filas = []
    xr_anterior = None
    raiz = None

    for i in range(1, MAX_ITERACIONES + 1):
        xr = (xi + xd) / 2
        fxr = evaluar(f_expr, xr)
        error = None if xr_anterior is None else calcular_error(xr, xr_anterior)
        filas.append([i, xi, xd, xr, fxr, error if error is not None else "-"])
        raiz = xr

        if fxr == 0 or abs(fxr) < tol or (error is not None and error < tol):
            break
        if fxi * fxr < 0:
            xd, fxd = xr, fxr
        else:
            xi, fxi = xr, fxr
        xr_anterior = xr

    imprimir_tabla(["Iteración", "xi", "xd", "xr", "f(xr)", "Error Relativo"], filas)
    return raiz


def falsa_posicion(f_expr, xi, xd, tol):
    fxi, fxd = validar_intervalo(f_expr, xi, xd)
    if fxi is None:
        return None
    if fxi == 0:
        return xi
    if fxd == 0:
        return xd

    filas = []
    xr_anterior = None
    raiz = None

    for i in range(1, MAX_ITERACIONES + 1):
        denominador = fxi - fxd
        if denominador == 0:
            print("Error: División por cero en falsa posición.")
            break
        xr = xd - (fxd * (xi - xd)) / denominador
        fxr = evaluar(f_expr, xr)
        error = None if xr_anterior is None else calcular_error(xr, xr_anterior)
        filas.append([i, xi, xd, xr, fxr, error if error is not None else "-"])
        raiz = xr

        if fxr == 0 or abs(fxr) < tol or (error is not None and error < tol):
            break
        if fxi * fxr < 0:
            xd, fxd = xr, fxr
        else:
            xi, fxi = xr, fxr
        xr_anterior = xr

    imprimir_tabla(["Iteración", "xi", "xd", "xr", "f(xr)", "Error Relativo"], filas)
    return raiz


def punto_fijo(g_expr, x0, tol):
    filas = []
    xi = x0
    raiz = None
    convergio = False

    for i in range(1, MAX_ITERACIONES + 1):
        try:
            xr = evaluar(g_expr, xi)
        except (TypeError, ValueError, ZeroDivisionError) as error:
            print(f"Error al evaluar g(x): {error}")
            break
        error = None if i == 1 else calcular_error(xr, xi)
        filas.append([i, xi, xr, error if error is not None else "-"])
        raiz = xr
        if error is not None and error < tol:
            convergio = True
            break
        xi = xr

    imprimir_tabla(["Iteración", "xi", "xr = g(xi)", "Error Relativo"], filas)
    if not convergio:
        print(f"Advertencia: no convergió en {MAX_ITERACIONES} iteraciones.")
    return raiz


def newton_raphson(f_expr, x0, tol):
    df_expr = sp.diff(f_expr, x)
    print(f"\nDerivada calculada automáticamente: f'(x) = {df_expr}")
    filas = []
    xi = x0
    raiz = None

    for i in range(1, MAX_ITERACIONES + 1):
        try:
            fxi = evaluar(f_expr, xi)
            dfxi = evaluar(df_expr, xi)
        except (TypeError, ValueError, ZeroDivisionError) as error:
            print(f"Error al evaluar la función: {error}")
            break
        if abs(dfxi) < 1e-14:
            print("Error: La derivada es cero o demasiado pequeña.")
            break

        xr = xi - fxi / dfxi
        error = None if i == 1 else calcular_error(xr, xi)
        filas.append([i, xi, fxi, dfxi, xr, error if error is not None else "-"])
        raiz = xr
        if abs(fxi) < tol or (error is not None and error < tol):
            break
        xi = xr

    imprimir_tabla(["Iteración", "xi", "f(xi)", "f'(xi)", "xr", "Error Relativo"], filas)
    return raiz


def secante(f_expr, x0, x1, tol):
    filas = []
    xi_anterior, xi = x0, x1
    raiz = None

    for i in range(1, MAX_ITERACIONES + 1):
        fxi = evaluar(f_expr, xi)
        fxi_anterior = evaluar(f_expr, xi_anterior)
        denominador = fxi_anterior - fxi
        if abs(denominador) < 1e-14:
            print("Error: División por cero en la fórmula de la secante.")
            break

        xr = xi - fxi * (xi_anterior - xi) / denominador
        fxr = evaluar(f_expr, xr)
        error = None if i == 1 else calcular_error(xr, xi)
        filas.append([i, xi_anterior, xi, xr, fxr, error if error is not None else "-"])
        raiz = xr
        if abs(fxr) < tol or (error is not None and error < tol):
            break
        xi_anterior, xi = xi, xr

    imprimir_tabla(["Iteración", "x(i-1)", "xi", "xr (Nuevo)", "f(xr)", "Error Relativo"], filas)
    return raiz


def obtener_expresion(texto):
    permitidos = {
        "x": x, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
        "exp": sp.exp, "log": sp.log, "sqrt": sp.sqrt, "pi": sp.pi,
    }
    return sp.sympify(texto, locals=permitidos)


def obtener_float(mensaje, positivo=False):
    try:
        valor = float(input(mensaje))
        if positivo and valor <= 0:
            raise ValueError
        return valor
    except ValueError:
        print("Error: introduce un número válido.")
        return None


def menu():
    print("=== MÉTODOS DE ANÁLISIS NUMÉRICO ===")
    try:
        f_expr = obtener_expresion(input("Introduce la función f(x) (ej. x**3 - 4*x - 9): "))
    except (sp.SympifyError, SyntaxError):
        print("Función inválida. Usa, por ejemplo, x**2, sin(x) o exp(x).")
        return

    print("\nSelecciona el error de tolerancia deseado:")
    print("1. 0.001\n2. 0.0001\n3. Otro")
    op_tol = input("Opción: ")
    if op_tol == "1":
        tol = 0.001
    elif op_tol == "2":
        tol = 0.0001
    else:
        tol = obtener_float("Introduce el error (ej. 0.00001): ", positivo=True)
        if tol is None:
            return

    print("\nSelecciona el método a utilizar:")
    print("1. Bisección\n2. Falsa Posición\n3. Punto Fijo\n4. Newton-Raphson\n5. Secante")
    metodo = input("Opción: ")

    if metodo in ["1", "2"]:
        xi = obtener_float("Introduce el límite inferior (xi): ")
        xd = obtener_float("Introduce el límite superior (xd): ")
        if xi is None or xd is None:
            return
        if metodo == "1":
            print(f"\nMétodo de Bisección para f(x) = {f_expr}")
            biseccion(f_expr, xi, xd, tol)
        else:
            print(f"\nMétodo de Falsa Posición para f(x) = {f_expr}")
            falsa_posicion(f_expr, xi, xd, tol)
    elif metodo == "3":
        try:
            g_expr = obtener_expresion(input("Introduce la función despejada g(x): "))
        except (sp.SympifyError, SyntaxError):
            print("Función g(x) inválida.")
            return
        x0 = obtener_float("Introduce el valor inicial (xi): ")
        if x0 is not None:
            print(f"\nMétodo de Punto Fijo para g(x) = {g_expr}")
            punto_fijo(g_expr, x0, tol)
    elif metodo in ["4", "5"]:
        x0 = obtener_float("Introduce el primer valor inicial (xi): ")
        if x0 is None:
            return
        if metodo == "4":
            print(f"\nMétodo de Newton-Raphson para f(x) = {f_expr}")
            newton_raphson(f_expr, x0, tol)
        else:
            x1 = obtener_float("Introduce el segundo valor inicial (xi): ")
            if x1 is not None:
                print(f"\nMétodo de la Secante para f(x) = {f_expr}")
                secante(f_expr, x0, x1, tol)
    else:
        print("Opción no válida.")


if __name__ == "__main__":
    menu()
