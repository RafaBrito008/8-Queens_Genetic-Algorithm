import numpy as np
import random
import tkinter as tk
from tkinter import Canvas

# Constantes
DIMENSION = 8  # Dimensiones del tablero (8x8 para el problema de las 8 reinas)
SIZE = 50  # Tamaño de cada celda en el tablero
COLOR_QUEEN = "red"  # Color de la reina
FONT_QUEEN = ("Arial", int(SIZE / 1.5))  # Fuente y tamaño de la reina

INDIVIDUOS = 250  # Número de individuos en la población
GENERACIONES = 1000  # Número máximo de generaciones
PROB_MUTACION = 0.2  # Probabilidad de mutación


# Función que calcula cuántas reinas se atacan entre sí.
def fitness(individuo):
    ataques = 0  # Inicializar contador de reinas que se atacan.
    for i in range(len(individuo)):
        for j in range(i + 1, len(individuo)):
            # Si dos reinas están en la misma fila, se atacan.
            if individuo[i] == individuo[j]:
                ataques += 1
            # Si dos reinas están en diagonal, se atacan.
            elif abs(individuo[i] - individuo[j]) == abs(i - j):
                ataques += 1
    return ataques  # Retorna el total de ataques (mientras más bajo, mejor es el individuo).


# Función que elige dos padres basado en su aptitud.
def seleccionar_padres(poblacion, probabilidades):
    indices = np.random.choice(len(poblacion), size=2, p=probabilidades)
    return poblacion[indices[0]], poblacion[indices[1]]


# Crea dos nuevos individuos combinando partes de dos padres.
def crossover(padre1, padre2):
    punto_corte = np.random.randint(1, len(padre1))  # Selecciona un punto de corte aleatorio.
    # Crea dos nuevos individuos combinando las partes de los padres.
    hijo1 = np.concatenate([padre1[:punto_corte], padre2[punto_corte:]])
    hijo2 = np.concatenate([padre2[:punto_corte], padre1[punto_corte:]])
    return hijo1, hijo2


# Introduce una variación aleatoria en un individuo.
def mutar(individuo):
    indice = np.random.randint(len(individuo))
    valor = np.random.randint(len(individuo))
    individuo[indice] = valor
    return individuo


# Clase para visualizar el tablero y la solución encontrada.
class Chessboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8 Reinas con Algoritmo Genético")
        self.canvas = Canvas(self, width=SIZE * DIMENSION, height=SIZE * DIMENSION)
        self.canvas.pack(pady=20)

    # Dibuja el tablero con la solución.
    def draw_board_with_solution(self, solution):
        # Dibuja las celdas del tablero.
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                x1, y1 = col * SIZE, row * SIZE
                x2, y2 = x1 + SIZE, y1 + SIZE
                color = "white" if (row + col) % 2 == 0 else "black"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                
        # Dibuja las reinas en sus respectivas posiciones.
        for col, row in enumerate(solution):
            x, y = (col + 0.5) * SIZE, (row + 0.5) * SIZE
            self.canvas.create_text(x, y, text="♛", font=FONT_QUEEN, fill=COLOR_QUEEN)
        self.mainloop()


# Función principal que ejecuta el algoritmo genético.
def algoritmo_genetico():
    # Genera una población inicial aleatoria.
    poblacion = [np.random.permutation(8) for _ in range(INDIVIDUOS)]
    for generacion in range(GENERACIONES):
        # Calcula la aptitud de cada individuo.
        fit_values = [fitness(ind) for ind in poblacion]

        # Calcula probabilidades de selección basadas en la aptitud.
        probabilidades = [1 / i if i != 0 else 1 for i in fit_values]
        s = sum(probabilidades)
        probabilidades = [i / s for i in probabilidades]

        nuevos_individuos = []
        # Genera nuevos individuos a través del crossover.
        for _ in range(INDIVIDUOS // 2):
            padre1, padre2 = seleccionar_padres(poblacion, probabilidades)
            hijo1, hijo2 = crossover(padre1, padre2)
            nuevos_individuos.extend([hijo1, hijo2])

        poblacion = nuevos_individuos

        # Realiza mutación en un individuo con cierta probabilidad.
        if random.random() < PROB_MUTACION:
            indice = np.random.randint(0, len(poblacion))
            individuo_a_mutar = poblacion[indice]
            mutar(individuo_a_mutar)

        # Si encuentra una solución óptima (sin ataques), la muestra y termina.
        fit_values = [fitness(ind) for ind in poblacion]
        mejor_fit = min(fit_values)
        if mejor_fit == 0:
            print(f"Generación {generacion + 1} -> Se ha encontrado una solución")
            solucion = poblacion[fit_values.index(mejor_fit)]
            print(solucion + 1)  # Se suma 1 para que las posiciones comiencen desde 1 en lugar de 0.
            app = Chessboard()
            app.draw_board_with_solution(solucion)
            break
        else:
            print(f"Generación {generacion + 1} -> Menor número de ataques = {mejor_fit}")


if __name__ == "__main__":
    algoritmo_genetico()
