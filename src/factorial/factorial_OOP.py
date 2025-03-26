import sys


class Factorial:
    def __init__(self):
        pass

    def calculate_factorial(self, num):
        if num < 0:
            print("El factorial de un número negativo no existe")
            return None
        elif num == 0:
            return 1
        else:
            fact = 1
            while num > 1:
                fact *= num
                num -= 1
            return fact

    def run(self, min_num, max_num):
        if min_num < 0 or max_num < 0:
            print("Los números deben ser positivos.")
            return

        if min_num > max_num:
            print("El número mínimo no puede ser mayor que el número máximo.")
            return

        print("Factoriales:")
        for num in range(min_num, max_num + 1):
            factorial = self.calculate_factorial(num)
            if factorial is not None:
                print(f"El factorial de {num} es {factorial}")


# Comprobar si se proporciona un rango desde la línea de comandos o solicitarlo al usuario
if len(sys.argv) < 3:
    min_range = int(input("Ingrese el número mínimo del rango: "))
    max_range = int(input("Ingrese el número máximo del rango: "))
else:
    min_range = int(sys.argv[1])
    max_range = int(sys.argv[2])

# Ejemplo de uso:
factorial_calculator = Factorial()
factorial_calculator.run(min_range, max_range)
