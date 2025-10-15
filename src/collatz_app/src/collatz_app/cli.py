"""
CLI de la aplicación Collatz.
Permite ingresar un número entero y calcular las iteraciones hasta 1.
"""

import click
from collatz_app.core import collat


@click.command()
@click.option(
    "--numero",
    prompt="Ingrese un número entero positivo (máx 1999)",
    type=int,
    help="Número entero positivo para evaluar."
)
def main(numero: int) -> None:
    """Función principal que ejecuta la lógica de Collatz."""
    try:
        iteraciones = collatz(numero)
        click.echo(f"\nEl número de iteraciones para {numero} es {iteraciones}\n")
    except ValueError as error:
        click.echo(f"Error: {error}")


if __name__ == "__main__":
    main()
