# !/usr/bin/python3
# Python program to display all the prime numbers within an interval
# Josue Linarez Hein

# Definimos el intervalo en el que queremos encontrar los números primos
lower = 1  # Límite inferior del intervalo
upper = 500  # Límite superior del intervalo

# Imprimimos un mensaje indicando el intervalo en el que estamos buscando números primos
print("Prime numbers between", lower, "and", upper, "are:")

# Iteramos sobre cada número en el rango del intervalo
for num in range(lower, upper + 1):
    # Todos los números primos son mayores que 1
    if num > 1:
        # Verificamos si el número es primo
        for i in range(2, num):
            if (num % i) == 0:  # Si el número es divisible por otro número que no sea 1 ni él mismo, no es primo
                break  # Salimos del bucle
        else:  # Si no encontramos ningún divisor, el número es primo
            print(num)  # Imprimimos el número primo
