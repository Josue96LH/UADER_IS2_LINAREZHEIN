import numpy as np
import matplotlib.pyplot as plt

# Calcula el esfuerzo respecto a la relacion dada
def calcular_esfuerzo(S):
    return 8 * (S ** 0.95)

# calculael tiempo respecto a la relacion dada
def calcular_tiempo(E):
    return 2.4 * (E ** 0.33)

# datos del tamaño para realizar el grafico
tamaños = np.linspace(0, 10000, 500)
esfuerzos = calcular_esfuerzo(tamaños)

# datos del esfuerzo para realizar el grafico
esfuerzos_td = np.linspace(1, 500, 500)
tiempos = calcular_tiempo(esfuerzos_td)

# Realiza el grafico del esfuerzo respecto al tamaño
plt.figure(figsize=(10, 5))
plt.plot(tamaños, esfuerzos, label="Esfuerzo (E)")
plt.xlabel('Tamaño del Proyecto (S)')
plt.ylabel('Esfuerzo (E)')
plt.title('Esfuerzo (E) respecto al Tamaño (S)')
plt.legend()
plt.grid(True)
plt.savefig("esfuerzo_tamano.png")

# Realiza el grafico del tiempo calendario respecto al Esfuerzo(E)
plt.figure(figsize=(10, 5))
plt.plot(esfuerzos_td, tiempos, label="Tiempo Calendario (td)", color='blue')
plt.xlabel('Esfuerzo (E)')
plt.ylabel('Tiempo Calendario (td)')
plt.title('Tiempo Calendario (td) respecto al Esfuerzo (E)')
plt.legend()
plt.grid(True)
plt.savefig("tiempo_calendario.png")