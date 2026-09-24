import sympy as sp
from tabulate import tabulate

def evaluar(f_expr, x_val):
    """Evalúa la expresión simbólica f_expr en el valor x_val."""
    x = sp.symbols('x')
    return float(f_expr.subs(x, x_val))

def imprimir_tabla(encabezados, filas):
    """Imprime los datos en formato de tabla similar a Excel."""
    print("\n" + tabulate(filas, headers=encabezados, tablefmt="fancy_grid", floatfmt=".6f"))

def biseccion(f_expr, xi, xd, tol):
    x = sp.symbols('x')
    if evaluar(f_expr, xi) * evaluar(f_expr, xd) >= 0:
        print("Error: La función no cambia de signo en el intervalo [xi, xd].")
        return

    filas = []
    xr_ant = 0
    for i in range(1, 101):
        xr = (xi + xd) / 2
        fxr = evaluar(f_expr, xr)
        error = abs((xr - xr_ant) / xr) if i > 1 else 100.0
        
        filas.append([i, xi, xd, xr, fxr, error if i > 1 else "-"])
        
        if i > 1 and error < tol:
            break
            
        if evaluar(f_expr, xi) * fxr < 0:
            xd = xr
        else:
            xi = xr
        xr_ant = xr

    imprimir_tabla(["Iteración", "xi", "xd", "xr", "f(xr)", "Error Relativo"], filas)

def falsa_posicion(f_expr, xi, xd, tol):
    if evaluar(f_expr, xi) * evaluar(f_expr, xd) >= 0:
        print("Error: La función no cambia de signo en el intervalo [xi, xd].")
        return

    filas = []
    xr_ant = 0
    for i in range(1, 101):
        fxi = evaluar(f_expr, xi)
        fxd = evaluar(f_expr, xd)
        xr = xd - (fxd * (xi - xd)) / (fxi - fxd)
        fxr = evaluar(f_expr, xr)
        error = abs((xr - xr_ant) / xr) if i > 1 else 100.0
        
        filas.append([i, xi, xd, xr, fxr, error if i > 1 else "-"])
        
        if i > 1 and error < tol:
            break
            
        if fxi * fxr < 0:
            xd = xr
        else:
            xi = xr
        xr_ant = xr

    imprimir_tabla(["Iteración", "xi", "xd", "xr", "f(xr)", "Error Relativo"], filas)

def punto_fijo(g_expr, x0, tol):
    filas = []
    xi = x0
    for i in range(1, 101):
        xr = evaluar(g_expr, xi)
        error = abs((xr - xi) / xr) if i > 1 else 100.0
        
        filas.append([i, xi, xr, error if i > 1 else "-"])
        
        if i > 1 and error < tol:
            break
        xi = xr

    imprimir_tabla(["Iteración", "xi", "xr = g(xi)", "Error Relativo"], filas)

def newton_raphson(f_expr, x0, tol):
    x = sp.symbols('x')
    df_expr = sp.diff(f_expr, x) # Derivada automática
    print(f"\nDerivada calculada automáticamente: f'(x) = {df_expr}")
    
    filas = []
    xi = x0
    for i in range(1, 101):
        fxi = evaluar(f_expr, xi)
        dfxi = evaluar(df_expr, xi)
        
        if dfxi == 0:
            print("Error: La derivada es cero. División por cero.")
            break
            
        xr = xi - (fxi / dfxi)
        error = abs((xr - xi) / xr) if i > 1 else 100.0
        
        filas.append([i, xi, fxi, dfxi, xr, error if i > 1 else "-"])
        
        if i > 1 and error < tol:
            break
        xi = xr

    imprimir_tabla(["Iteración", "xi", "f(xi)", "f'(xi)", "xr", "Error Relativo"], filas)

def secante(f_expr, x0, x1, tol):
    filas = []
    xi_ant = x0
    xi = x1
    for i in range(1, 101):
        fxi = evaluar(f_expr, xi)
        fxi_ant = evaluar(f_expr, xi_ant)
        
        if fxi - fxi_ant == 0:
            print("Error: División por cero en la fórmula de la secante.")
            break
            
        xr = xi - (fxi * (xi_ant - xi)) / (fxi_ant - fxi)
        error = abs((xr - xi) / xr) if i > 1 else 100.0
        
        filas.append([i, xi_ant, xi, xr, evaluar(f_expr, xr), error if i > 1 else "-"])
        
        if i > 1 and error < tol:
            break
        
        xi_ant = xi
        xi = xr

    imprimir_tabla(["Iteración", "x(i-1)", "xi", "xr (Nuevo)", "f(xr)", "Error Relativo"], filas)

def menu():
    x = sp.symbols('x')
    print("=== MÉTODOS DE ANÁLISIS NUMÉRICO ===")
    func_str = input("Introduce la función f(x) (ej. x**3 - 4*x - 9): ")
    try:
        f_expr = sp.sympify(func_str)
    except:
        print("Función inválida. Usa sintaxis de Python (ej. x**2, sp.sin(x), sp.exp(x)).")
        return

    print("\nSelecciona el error de tolerancia deseado:")
    print("1. 0.001")
    print("2. 0.0001")
    print("3. Otro")
    op_tol = input("Opción: ")
    if op_tol == '1': tol = 0.001
    elif op_tol == '2': tol = 0.0001
    else: tol = float(input("Introduce el error (ej. 0.00001): "))

    print("\nSelecciona el método a utilizar:")
    print("1. Bisección")
    print("2. Falsa Posición")
    print("3. Punto Fijo")
    print("4. Newton-Raphson")
    print("5. Secante")
    metodo = input("Opción: ")

    if metodo in ['1', '2']:
        xi = float(input("Introduce el límite inferior (xi): "))
        xd = float(input("Introduce el límite superior (xd): "))
        if metodo == '1':
            print(f"\nMétodo de Bisección para f(x) = {f_expr}")
            biseccion(f_expr, xi, xd, tol)
        else:
            print(f"\nMétodo de Falsa Posición para f(x) = {f_expr}")
            falsa_posicion(f_expr, xi, xd, tol)

    elif metodo == '3':
        func_g_str = input("Introduce la función despejada g(x) (ej. (4*x + 9)**(1/3)): ")
        g_expr = sp.sympify(func_g_str)
        x0 = float(input("Introduce el valor inicial (xi): "))
        print(f"\nMétodo de Punto Fijo para g(x) = {g_expr}")
        punto_fijo(g_expr, x0, tol)

    elif metodo == '4':
        x0 = float(input("Introduce el valor inicial (xi): "))
        print(f"\nMétodo de Newton-Raphson para f(x) = {f_expr}")
        newton_raphson(f_expr, x0, tol)

    elif metodo == '5':
        x0 = float(input("Introduce el primer valor inicial (xi-1): "))
        x1 = float(input("Introduce el segundo valor inicial (xi): "))
        print(f"\nMétodo de la Secante para f(x) = {f_expr}")
        secante(f_expr, x0, x1, tol)
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    menu()
    