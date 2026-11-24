import pytest

from temas.metodos_raices import MetodosRaices


def test_convert_expression_accepts_caret_notation():
    solver = MetodosRaices()
    expr = solver.convert_expression("x^2 - 2")
    assert str(expr) == "x**2 - 2"


def test_convert_expression_rejects_empty_input():
    solver = MetodosRaices()
    with pytest.raises(ValueError):
        solver.convert_expression("   ")


def test_read_float_retries_after_non_numeric_input(monkeypatch, capsys):
    solver = MetodosRaices()
    entradas = iter(["abc", "2.5"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(entradas))

    assert solver.read_float("valor: ") == 2.5
    assert "Entrada inválida" in capsys.readouterr().out


def test_biseccion_converges_to_root(monkeypatch, capsys):
    solver = MetodosRaices()
    entradas = iter(["x^2 - 2", "1", "2", "0.001"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(entradas))

    solver.biseccion()

    output = capsys.readouterr().out
    aproximacion = float(output.split("valor aprx: ")[1].splitlines()[0])
    assert abs(aproximacion - 2**0.5) <= 0.001
