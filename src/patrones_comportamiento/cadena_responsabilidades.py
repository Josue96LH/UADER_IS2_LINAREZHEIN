class Handler:
    # Clase base abstracta para los manejadores en la cadena de responsabilidad.
    def __init__(self, successor=None):
        # Inicializa un nuevo manejador con un sucesor opcional en la cadena.
        self.successor = successor

    def handle_request(self, number):
        # Método para manejar la solicitud de un número.
        # Si el manejador puede manejar el número, lo procesa; de lo contrario, pasa la solicitud al siguiente manejador en la cadena.
        if not self.can_handle(number):
            if self.successor:
                self.successor.handle_request(number)
            else:
                print(f"El número {number} no fue consumido.")

    def can_handle(self, number):
        # Método abstracto que debe ser implementado por las subclases.
        # Debe devolver True si el manejador puede manejar el número dado, False de lo contrario.
        raise NotImplementedError("Debe implementar este método en las subclases.")


class PrimeHandler(Handler):
    # Clase para manejar números primos en la cadena de responsabilidad.
    def can_handle(self, number):
        # Verifica si el número dado es primo.
        return self.is_prime(number)

    def is_prime(self, number):
        # Verifica si un número es primo.
        if number < 2:
            return False
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                return False
        return True

    def handle_request(self, number):
        # Maneja la solicitud del número si es primo, de lo contrario pasa la solicitud al siguiente manejador en la cadena.
        if self.can_handle(number):
            print(f"El número {number} es primo.")
        else:
            super().handle_request(number)


class EvenHandler(Handler):
    # Clase para manejar números pares en la cadena de responsabilidad.
    def can_handle(self, number):
        # Verifica si el número dado es par.
        return number % 2 == 0

    def handle_request(self, number):
        # Maneja la solicitud del número si es par, de lo contrario pasa la solicitud al siguiente manejador en la cadena.
        if self.can_handle(number):
            print(f"El número {number} es par.")
        else:
            super().handle_request(number)


class NumberProcessor:
    # Clase para procesar números del 1 al 100 usando la cadena de responsabilidad.
    def __init__(self):
        # Inicializa un nuevo procesador con una cadena de manejadores predefinida.
        self.handler_chain = PrimeHandler(EvenHandler())

    def process_numbers(self):
        # Procesa los números del 1 al 100 pasándolos a través de la cadena de responsabilidad.       
        for number in range(1, 101):
            self.handler_chain.handle_request(number)


if __name__ == "__main__":
    processor = NumberProcessor()
    processor.process_numbers()