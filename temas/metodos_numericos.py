class AnalisisNumerico:
    """Colección de métodos numéricos para interpolación, raíces y sistemas lineales."""

    def __init__(self, tolerancia=1e-6, max_iter=100):
        self.tolerancia = tolerancia
        self.max_iter = max_iter

    def _validar_lista(self, valores, nombre):
        if valores is None or len(valores) == 0:
            raise ValueError(f"{nombre} no puede estar vacío.")
        return list(valores)

    def _validar_matriz(self, A, b):
        if len(A) != len(b):
            raise ValueError("La matriz A y el vector b deben tener la misma dimensión.")

        for i, fila in enumerate(A):
            if len(fila) != len(b):
                raise ValueError(
                    f"La fila {i} de A debe tener longitud {len(b)}, pero tiene {len(fila)}."
                )
            if abs(fila[i]) < 1e-12:
                raise ZeroDivisionError(
                    f"El elemento diagonal A[{i}][{i}] es cero; el método no puede continuar."
                )

    def calcular_error_vectorial(self, x_actual, x_anterior):
        """Calcula la norma infinito de la diferencia entre dos vectores."""
        if len(x_actual) != len(x_anterior):
            raise ValueError("Los vectores deben tener la misma longitud.")
        return max(abs(a - b) for a, b in zip(x_actual, x_anterior))

    def lagrange(self, x_puntos, y_puntos, x_eval):
        """Evalúa el polinomio interpolador de Lagrange en x_eval."""
        x_puntos = self._validar_lista(x_puntos, "x_puntos")
        y_puntos = self._validar_lista(y_puntos, "y_puntos")

        if len(x_puntos) != len(y_puntos):
            raise ValueError("x_puntos e y_puntos deben tener la misma longitud.")

        n = len(x_puntos)
        resultado = 0.0

        for i in range(n):
            termino = y_puntos[i]
            for j in range(n):
                if i != j:
                    denominador = x_puntos[i] - x_puntos[j]
                    if abs(denominador) < 1e-12:
                        raise ZeroDivisionError(
                            "Hay puntos x repetidos; la interpolación de Lagrange no es válida."
                        )
                    termino *= (x_eval - x_puntos[j]) / denominador
            resultado += termino

        return resultado

    def newton_raphson(self, f, df, x0):
        """Encuentra una raíz de f(x) = 0 mediante Newton-Raphson."""
        x = float(x0)

        for iteracion in range(1, self.max_iter + 1):
            fx = f(x)
            dfx = df(x)

            if abs(dfx) < 1e-12:
                raise ValueError(
                    "La derivada es cercana a cero. El método no puede continuar."
                )

            x_nuevo = x - (fx / dfx)
            error = abs(x_nuevo - x)

            if error < self.tolerancia:
                return x_nuevo, iteracion

            x = x_nuevo

        return x, self.max_iter

    def diferencias_divididas(self, x_puntos, y_puntos, x_eval):
        """Construye el polinomio interpolador de Newton usando diferencias divididas."""
        x_puntos = self._validar_lista(x_puntos, "x_puntos")
        y_puntos = self._validar_lista(y_puntos, "y_puntos")

        if len(x_puntos) != len(y_puntos):
            raise ValueError("x_puntos e y_puntos deben tener la misma longitud.")

        n = len(x_puntos)
        tabla = [[0.0] * n for _ in range(n)]

        for i in range(n):
            tabla[i][0] = y_puntos[i]

        for j in range(1, n):
            for i in range(n - j):
                numerador = tabla[i + 1][j - 1] - tabla[i][j - 1]
                denominador = x_puntos[i + j] - x_puntos[i]
                if abs(denominador) < 1e-12:
                    raise ZeroDivisionError(
                        "Hay puntos x repetidos o mal ordenados; no se puede calcular la diferencia dividida."
                    )
                tabla[i][j] = numerador / denominador

        coeficientes = [tabla[0][j] for j in range(n)]

        resultado = coeficientes[0]
        producto = 1.0
        for i in range(1, n):
            producto *= x_eval - x_puntos[i - 1]
            resultado += coeficientes[i] * producto

        return resultado, coeficientes

    def minimos_cuadrados(self, x_puntos, y_puntos, x_eval=None):
        """Ajusta una recta y = mx + b por mínimos cuadrados."""
        x_puntos = self._validar_lista(x_puntos, "x_puntos")
        y_puntos = self._validar_lista(y_puntos, "y_puntos")

        if len(x_puntos) != len(y_puntos):
            raise ValueError("x_puntos e y_puntos deben tener la misma longitud.")

        n = len(x_puntos)
        suma_x = sum(x_puntos)
        suma_y = sum(y_puntos)
        suma_xy = sum(x * y for x, y in zip(x_puntos, y_puntos))
        suma_x2 = sum(x**2 for x in x_puntos)

        denominador = n * suma_x2 - suma_x**2
        if abs(denominador) < 1e-12:
            raise ZeroDivisionError(
                "El denominador para mínimos cuadrados es cero, la recta no está definida."
            )

        m = (n * suma_xy - suma_x * suma_y) / denominador
        b = (suma_y - m * suma_x) / n

        y_estimado = (m * x_eval + b) if x_eval is not None else None
        return m, b, y_estimado

    def gauss_seidel(self, A, b, x0=None):
        """Resuelve Ax = b por el método de Gauss-Seidel."""
        A = [list(fila) for fila in A]
        b = list(b)
        self._validar_matriz(A, b)

        n = len(b)
        x = [0.0] * n if x0 is None else [float(valor) for valor in x0]
        if len(x) != n:
            raise ValueError(f"x0 debe tener longitud {n}.")

        for iteracion in range(1, self.max_iter + 1):
            x_anterior = list(x)
            for i in range(n):
                suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
                x[i] = (b[i] - suma) / A[i][i]

            if self.calcular_error_vectorial(x, x_anterior) < self.tolerancia:
                return x, iteracion

        return x, self.max_iter

    def jacobi(self, A, b, x0=None):
        """Resuelve Ax = b por el método de Jacobi."""
        A = [list(fila) for fila in A]
        b = list(b)
        self._validar_matriz(A, b)

        n = len(b)
        x = [0.0] * n if x0 is None else [float(valor) for valor in x0]
        if len(x) != n:
            raise ValueError(f"x0 debe tener longitud {n}.")

        for iteracion in range(1, self.max_iter + 1):
            x_nuevo = [0.0] * n
            for i in range(n):
                suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
                x_nuevo[i] = (b[i] - suma) / A[i][i]

            if self.calcular_error_vectorial(x_nuevo, x) < self.tolerancia:
                return x_nuevo, iteracion

            x = x_nuevo

        return x, self.max_iter