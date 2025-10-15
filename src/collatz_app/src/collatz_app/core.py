"""
Módulo principal: collatz_app.core
Calcula el número de iteraciones necesarias para llegar a 1 según la conjetura de Collatz.
"""

def collatz(num: int) -> int:
    """
    Calcula el número de iteraciones hasta llegar a 1.

    Args:
        num (int): número entero positivo (1 <= num <= 1999)

    Returns:
        int: cantidad de iteraciones.

    Raises:
        ValueError: si el número no es válido.
    """
    if not isinstance(num, int):
        raise ValueError("El valor debe ser un número entero.")

    if num <= 0 or num > 1999:
        raise ValueError("El número debe estar entre 1 y 1999.")

    iteraciones = 0
    while num != 1:
        if num % 2 == 0:
            num //= 2
        else:
            num = 3 * num + 1
        iteraciones += 1

    return iteraciones