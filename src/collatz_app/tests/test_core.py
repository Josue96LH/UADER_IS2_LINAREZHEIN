"""
Tests para collatz_app.core
"""

import pytest
from collatz_app.core import collatz


def test_collatz_valido():
    assert collatz(6) == 8


def test_collatz_minimo():
    assert collatz(1) == 0


def test_collatz_invalido_tipo():
    with pytest.raises(ValueError):
        collatz("abc")


def test_collatz_fuera_rango():
    with pytest.raises(ValueError):
        collatz(2000)
