import os


class Memento:
    """
    Clase Memento: representa un estado anterior de FileWriterUtility.

    Atributos:
        file (str): Nombre del archivo asociado al estado.
        content (str): Contenido del archivo en el estado.
    """
    def __init__(self, file, content):
        self.file = file
        self.content = content


class FileWriterUtility:
    """
    Clase FileWriterUtility: gestiona la escritura de archivos y mantiene un historial de estados anteriores.

    Atributos:
        file (str): Nombre del archivo actual.
        content (str): Contenido actual del archivo.
        history (list): Lista para almacenar los estados anteriores (Mementos).
    """
    def __init__(self, file):
        self.file = file
        self.content = ""
        self.history = []  # Lista para almacenar los estados anteriores

    def write(self, string):
        """Añade texto al contenido del archivo."""
        self.content += string

    def save(self):
        """Guarda el estado actual del archivo en el historial."""
        if len(self.history) >= 4:  # Limita el historial a 4 estados
            del self.history[0]  # Elimina el estado más antiguo si hay más de 4
        self.history.append(Memento(self.file, self.content))  # Agrega el nuevo estado a la historia

    def undo(self, num_states=1):
        """
        Deshace uno o más estados anteriores y restaura el archivo al estado anterior.

        Args:
            num_states (int): Número de estados anteriores a deshacer. Por defecto, deshace solo el último estado.
        """
        if num_states > len(self.history):
            num_states = len(self.history)
        for _ in range(num_states):
            if self.history:
                memento = self.history.pop()  # Obtiene el último estado
                self.file = memento.file
                self.content = memento.content


class FileWriterCaretaker:
    """
    Clase FileWriterCaretaker: gestiona las operaciones de guardado y deshacer.

    Métodos:
        save(writer): Guarda el estado actual del escritor.
        undo(writer, num_states=1): Deshace uno o más estados anteriores del escritor.
    """
    def save(self, writer):
        """Guarda el estado actual del escritor."""
        writer.save()

    def undo(self, writer, num_states=1):
        """
        Deshace uno o más estados anteriores del escritor.

        Args:
            writer (FileWriterUtility): Instancia del escritor cuyo estado se deshace.
            num_states (int): Número de estados anteriores a deshacer. Por defecto, deshace solo el último estado.
        """
        writer.undo(num_states)


if __name__ == '__main__':
    os.system("clear")
    print("Crea un objeto que gestionará la versión anterior")
    caretaker = FileWriterCaretaker()

    print("Crea el objeto cuyo estado se quiere preservar")
    writer = FileWriterUtility("GFG.txt")

    print("Se graba algo en el objeto y se salva")
    writer.write("Clase de IS2 en UADER\n")
    print(writer.content + "\n\n")
    caretaker.save(writer)

    print("Se graba información adicional")
    writer.write("Material adicional de la clase de patrones\n")
    print(writer.content + "\n\n")
    caretaker.save(writer)

    print("Se graba información adicional II")
    writer.write("Material adicional de la clase de patrones II\n")
    print(writer.content + "\n\n")
    caretaker.save(writer)

    print("Se graba información adicional III")
    writer.write("Material adicional de la clase de patrones III\n")
    print(writer.content + "\n\n")
    caretaker.save(writer)

    print("Se graba información adicional IV")
    writer.write("Material adicional de la clase de patrones IV\n")
    print(writer.content + "\n\n")
    caretaker.save(writer)

    print("Se invoca al <undo> para recuperar el inmediato anterior")
    caretaker.undo(writer)
    print("Se muestra el estado actual")
    print(writer.content + "\n\n")

    print("Se invoca al <undo> para recuperar los 2 estados anteriores")
    caretaker.undo(writer, 2)
    print("Se muestra el estado actual")
    print(writer.content + "\n\n")

    print("Se invoca al <undo> para recuperar los 3 estados anteriores")
    caretaker.undo(writer, 3)
    print("Se muestra el estado actual")
    print(writer.content + "\n\n")

    print("Se invoca al <undo> para recuperar los 4 estados anteriores")
    caretaker.undo(writer, 4)
    print("Se muestra el estado actual")
    print(writer.content + "\n\n")