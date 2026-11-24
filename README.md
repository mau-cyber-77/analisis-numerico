# Análisis numérico

El programa reúne los métodos de búsqueda de raíces y los métodos numéricos del
parcial 2 en un solo menú.

## Ejecución

Desde la carpeta del proyecto, ejecuta:

```text
python main.py
```

`main.py` inicia el programa y `menu.py` contiene el único menú interactivo.

## Temas

Los módulos con los ejercicios están en `temas/`:

- `metodos_raices.py`: bisección, punto fijo, falsa posición, Newton-Raphson y
  secante, organizados en la clase `MetodosRaices`.
- `metodos_numericos.py`: interpolación, mínimos cuadrados y sistemas lineales.
  La clase `AnalisisNumerico` usa `__init__`, `self` y métodos de instancia.
- `clases_objetos.py` y `herencia.py`: ejercicios de clases, creación de
  objetos, llamadas a métodos, herencia y `super()`.

Las pruebas automatizadas están en `tests/` y se ejecutan con
`python -m pytest`.