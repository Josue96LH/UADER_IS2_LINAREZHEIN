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

# Verificar si se pasó un argumento
if len(sys.argv) < 2:
    rango = input("Ingrese un rango en el formato 'inicio-fin' (ej. 4-8): ")
else:
    rango = sys.argv[1]

# Procesar el rango
try:
    inicio, fin = map(int, rango.split('-'))
    if inicio > fin:
        print("El número de inicio debe ser menor o igual al de fin.")
    else:
        calcular_factoriales(inicio, fin)
except ValueError:
    print("Formato incorrecto. Use 'inicio-fin' con números enteros.")
