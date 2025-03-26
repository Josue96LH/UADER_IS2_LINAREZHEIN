#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys

def factorial(num): 
    if num < 0: 
        return "Factorial de un número negativo no existe"
    elif num == 0: 
        return 1
    else: 
        fact = 1
        while num > 1: 
            fact *= num 
            num -= 1
        return fact 

def calcular_factoriales(inicio, fin):
    for num in range(inicio, fin + 1):
        print(f"Factorial de {num}! es {factorial(num)}")

# Definir límites predeterminados
LIMITE_INFERIOR = 1
LIMITE_SUPERIOR = 60

# Obtener el argumento o solicitarlo manualmente
if len(sys.argv) < 2:
    rango = input("Ingrese un rango en el formato 'inicio-fin', '-fin' o 'inicio-': ")
else:
    rango = sys.argv[1]

# Procesar el rango
try:
    if rango.startswith('-'):  # Caso "-hasta"
        fin = int(rango[1:])  # Extraer el número después del '-'
        inicio = LIMITE_INFERIOR
    elif rango.endswith('-'):  # Caso "desde-"
        inicio = int(rango[:-1])  # Extraer el número antes del '-'
        fin = LIMITE_SUPERIOR
    else:  # Caso "inicio-fin"
        inicio, fin = map(int, rango.split('-'))

    if inicio > fin:
        print("El número de inicio debe ser menor o igual al de fin.")
    else:
        calcular_factoriales(inicio, fin)

except ValueError:
    print("Formato incorrecto. Use 'inicio-fin', '-fin' o 'inicio-' con números enteros.")
