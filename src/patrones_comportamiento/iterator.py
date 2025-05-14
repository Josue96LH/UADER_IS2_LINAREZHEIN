class ReverseIterator:
    """Clase que implementa un iterador para recorrer una cadena en sentido inverso."""

    def __init__(self, data):
        """
        Inicializa el iterador con la cadena de caracteres y establece el índice inicial al final de la cadena.

        Args:
            data (str): La cadena de caracteres a recorrer en sentido inverso.
        """
        self.data = data
        self.index = len(data)

    def __iter__(self):
        """Devuelve el propio objeto iterador."""
        return self

    def __next__(self):
        """
        Devuelve el siguiente carácter en la cadena en sentido inverso.

        Returns:
            str: El siguiente carácter en la cadena.

        Raises:
            StopIteration: Cuando se ha alcanzado el final de la cadena.
        """
        if self.index <= 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]


class ForwardIterator:
    """Clase que implementa un iterador para recorrer una cadena en sentido directo."""

    def __init__(self, data):
        """
        Inicializa el iterador con la cadena de caracteres y establece el índice inicial al inicio de la cadena.

        Args:
            data (str): La cadena de caracteres a recorrer en sentido directo.
        """
        self.data = data
        self.index = 0

    def __iter__(self):
        """Devuelve el propio objeto iterador."""
        return self

    def __next__(self):
        """
        Devuelve el siguiente carácter en la cadena en sentido directo.

        Returns:
            str: El siguiente carácter en la cadena.

        Raises:
            StopIteration: Cuando se ha alcanzado el final de la cadena.
        """
        if self.index >= len(self.data):
            raise StopIteration
        self.index += 1
        return self.data[self.index - 1]


class BidirectionalIterator:
    """Clase que permite obtener iteradores para recorrer una cadena en ambos sentidos."""

    def __init__(self, data):
        """
        Inicializa la clase con la cadena de caracteres.

        Args:
            data (str): La cadena de caracteres a recorrer en ambos sentidos.
        """
        self.forward_iterator = ForwardIterator(data)
        self.reverse_iterator = ReverseIterator(data)

    def forward(self):
        """
        Devuelve un iterador para recorrer la cadena en sentido directo.

        Returns:
            ForwardIterator: Iterador para recorrer la cadena en sentido directo.
        """
        return self.forward_iterator

    def reverse(self):
        """
        Devuelve un iterador para recorrer la cadena en sentido inverso.

        Returns:
            ReverseIterator: Iterador para recorrer la cadena en sentido inverso.
        """
        return self.reverse_iterator


# Ejemplo de uso:
cadena = "Hola Pedro"

# Iteración en sentido directo
print("Sentido directo:")
for char in BidirectionalIterator(cadena).forward():
    print(char)

# Iteración en sentido inverso
print("\nSentido inverso:")
for char in BidirectionalIterator(cadena).reverse():
    print(char)