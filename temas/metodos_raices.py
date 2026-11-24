import sympy as sp


class MetodosRaices:
    """Métodos iterativos para encontrar raíces de funciones."""

    def __init__(self, max_iter=100):
        self.max_iter = max_iter
        self.x = sp.symbols("x")

    def convert_expression(self, raw_value):
        if raw_value is None:
            raise ValueError("La expresión no puede estar vacía.")

        expr = str(raw_value).strip()
        if not expr:
            raise ValueError("La expresión no puede estar vacía.")

        expr = expr.replace("^", "**").replace("X", "x")

        try:
            parsed = sp.sympify(expr, locals={"x": self.x})
        except (sp.SympifyError, TypeError, ValueError) as exc:
            raise ValueError(f"Expresión inválida: {raw_value}") from exc

        if parsed.free_symbols - {self.x}:
            raise ValueError("La expresión solo debe depender de x.")
        if not parsed.free_symbols:
            raise ValueError("La función debe depender de x para resolver la ecuación.")

        return parsed

    def read_float(self, prompt):
        while True:
            try:
                return float(input(prompt).strip())
            except ValueError:
                print("Entrada inválida. Debe ser un número real.")

    def _leer_funcion(self):
        try:
            return self.convert_expression(input("Introduzca f(x): "))
        except ValueError as exc:
            print(f"Error: {exc}")
            return None

    def biseccion(self):
        funcion = self._leer_funcion()
        if funcion is None:
            return

        xi = self.read_float("Introduzca el valor de xi: ")
        xd = self.read_float("Introduzca el valor de xd: ")
        error_deseado = self.read_float("Introduzca el error deseado: ")
        funcion_numerica = sp.lambdify(self.x, funcion, "math")

        if xi >= xd:
            print("Error: xi debe ser menor que xd.")
            return
        if error_deseado <= 0:
            print("Error: el error deseado debe ser mayor que 0.")
            return

        f_xi = funcion_numerica(xi)
        f_xd = funcion_numerica(xd)
        if f_xi == 0:
            print(f"xi = {xi}")
            return
        if f_xd == 0:
            print(f"xd = {xd}")
            return
        if f_xi * f_xd > 0:
            print("Error: no cambia de signo.")
            return

        print("\nIteracion        xi             xd             xm             error")
        for iteracion in range(1, self.max_iter + 1):
            xm = (xi + xd) / 2
            f_xm = funcion_numerica(xm)
            error = abs(xd - xi) / 2
            print(
                f"{iteracion:5d}   {xi:12.6f}   {xd:12.6f}   "
                f"{xm:12.6f}   {error:12.6f}"
            )
            if f_xm == 0 or error <= error_deseado:
                break
            if f_xi * f_xm < 0:
                xd = xm
                f_xd = f_xm
            else:
                xi = xm
                f_xi = f_xm

        print(f"\nvalor aprx: {xm}")
        print(f"f({xm}) = {funcion_numerica(xm)}")

    def punto_fijo(self):
        try:
            funcion = self.convert_expression(input("Introduzca f(x): "))
            despeje = self.convert_expression(input("despejada de f(x)=0: "))
        except ValueError as exc:
            print(f"Error: {exc}")
            return

        x0 = self.read_float("Introduzca el valor de x0: ")
        error_deseado = self.read_float("Introduzca el error deseado: ")
        if error_deseado <= 0:
            print("Error: el error deseado debe ser mayor que 0.")
            return

        funcion_numerica = sp.lambdify(self.x, funcion, "math")
        despeje_numerico = sp.lambdify(self.x, despeje, "math")
        print(f"g({x0}) = {despeje_numerico(x0)}")
        print("\nIteracion          x                 g(x)              error")
        for iteracion in range(1, self.max_iter + 1):
            x1 = despeje_numerico(x0)
            error = abs(x1 - x0)
            print(
                f"{iteracion:5d}   {x0:16.8f}   {x1:16.8f}   "
                f"{error:12.8f}"
            )
            if error <= error_deseado or funcion_numerica(x1) == 0:
                print(f"\nvalor aprx: {x1}")
                return
            x0 = x1

        print(f"\nEl metodo no convergio en {self.max_iter} iteraciones.")

    def falsa_posicion(self):
        funcion = self._leer_funcion()
        if funcion is None:
            return

        xi = self.read_float("Introduzca el valor de xi: ")
        xd = self.read_float("Introduzca el valor de xd: ")
        error_deseado = self.read_float("Introduzca el error deseado: ")
        if xi >= xd:
            print("Error: xi debe ser menor que xd.")
            return
        if error_deseado <= 0:
            print("Error: el error deseado debe ser mayor que 0.")
            return

        funcion_numerica = sp.lambdify(self.x, funcion, "math")
        f_xi = funcion_numerica(xi)
        f_xd = funcion_numerica(xd)
        if f_xi == 0:
            print(f"xi = {xi}")
            return
        if f_xd == 0:
            print(f"xd = {xd}")
            return
        if f_xi * f_xd > 0:
            print("Error: no cambia de signo.")
            return

        xm_anterior = None
        print("\nIteracion        xi             xd             xm             error")
        for iteracion in range(1, self.max_iter + 1):
            denominador = f_xd - f_xi
            if denominador == 0:
                print("Error: no se puede calcular la falsa posicion.")
                return

            xm = (xi * f_xd - xd * f_xi) / denominador
            f_xm = funcion_numerica(xm)
            error = abs(xm - xm_anterior) if xm_anterior is not None else abs(f_xm)
            print(
                f"{iteracion:5d}   {xi:12.6f}   {xd:12.6f}   "
                f"{xm:12.6f}   {error:12.6f}"
            )
            if f_xm == 0 or error <= error_deseado:
                print(f"\nvalor aprx: {xm}")
                print(f"f({xm}) = {f_xm}")
                return

            if f_xi * f_xm < 0:
                xd = xm
                f_xd = f_xm
            else:
                xi = xm
                f_xi = f_xm
            xm_anterior = xm

        print(f"\nEl metodo no convergio en {self.max_iter} iteraciones.")

    def newton_raphson(self):
        funcion = self._leer_funcion()
        if funcion is None:
            return

        derivada = sp.diff(funcion, self.x)
        x0 = self.read_float("Introduzca el valor de x0: ")
        error_deseado = self.read_float("Introduzca el error deseado: ")
        if error_deseado <= 0:
            print("Error: el error deseado debe ser mayor que 0.")
            return

        funcion_numerica = sp.lambdify(self.x, funcion, "math")
        derivada_numerica = sp.lambdify(self.x, derivada, "math")
        print(f"f'({x0}) = {derivada_numerica(x0)}")
        print("\nIteracion          x                 f(x)              error")
        for iteracion in range(1, self.max_iter + 1):
            f_x0 = funcion_numerica(x0)
            derivada_x0 = derivada_numerica(x0)
            if derivada_x0 == 0:
                print("Error: la derivada es cero.")
                return

            x1 = x0 - f_x0 / derivada_x0
            error = abs(x1 - x0)
            print(
                f"{iteracion:5d}   {x0:16.8f}   {f_x0:16.8f}   "
                f"{error:12.8f}"
            )
            if error <= error_deseado or funcion_numerica(x1) == 0:
                print(f"\nvalor aprx: {x1}")
                return
            x0 = x1

        print(f"\nEl metodo no convergio en {self.max_iter} iteraciones.")

    def secante(self):
        funcion = self._leer_funcion()
        if funcion is None:
            return

        funcion_numerica = sp.lambdify(self.x, funcion, "math")
        x0 = self.read_float("Introduzca el valor de x0: ")
        x1 = self.read_float("Introduzca el valor de x1: ")
        if x0 == x1:
            print("Error: x0 y x1 deben ser diferentes.")
            return

        error_deseado = self.read_float("Introduzca el error deseado: ")
        if error_deseado <= 0:
            print("Error: el error deseado debe ser mayor que 0.")
            return

        print(
            "\nIter |        x0         |        x1         |      f(x0)      |"
            "       f(x1)       |        x(i+1)       |       error"
        )
        print(
            "-----|-------------------|-------------------|-------------------|"
            "-------------------|-------------------|----------------"
        )
        for iteracion in range(1, self.max_iter + 1):
            f_x0 = funcion_numerica(x0)
            f_x1 = funcion_numerica(x1)
            denominador = f_x1 - f_x0
            if denominador == 0:
                print("Error: no se puede continuar; el denominador es cero.")
                return

            x2 = x1 - f_x1 * (x1 - x0) / denominador
            error = abs(x2 - x1)
            print(
                f"{iteracion:5d} | {x0:>17.8f} | {x1:>17.8f} | "
                f"{f_x0:>17.8f} | {f_x1:>17.8f} | {x2:>17.8f} | "
                f"{error:>15.8e}"
            )
            if error <= error_deseado or funcion_numerica(x2) == 0:
                print(f"\nvalor aprx: {x2}")
                print(f"f({x2}) = {funcion_numerica(x2)}")
                return
            x0, x1 = x1, x2

        print(f"\nEl metodo no convergio en {self.max_iter} iteraciones.")
