import numpy as np
import random
import tkinter as tk
from tkinter import Canvas

DIMENSION = 8
SIZE = 50
COLOR_QUEEN = "red"
FONT_QUEEN = ("Arial", int(SIZE / 1.5))


def fitness(individuo):
    ataques = 0
    for i in range(len(individuo)):
        for j in range(i + 1, len(individuo)):
            if individuo[i] == individuo[j]:
                ataques += 1
            elif abs(individuo[i] - individuo[j]) == abs(i - j):
                ataques += 1
    return 28 - ataques


def seleccionar_padres(poblacion, probabilidades):
    indices = np.random.choice(len(poblacion), size=2, p=probabilidades)
    return poblacion[indices[0]], poblacion[indices[1]]


def crossover(padre1, padre2):
    punto_corte = np.random.randint(1, len(padre1))
    hijo1 = np.concatenate([padre1[:punto_corte], padre2[punto_corte:]])
    hijo2 = np.concatenate([padre2[:punto_corte], padre1[punto_corte:]])
    return hijo1, hijo2


def mutar(individuo):
    indice = np.random.randint(len(individuo))
    valor = np.random.randint(len(individuo))
    individuo[indice] = valor
    return individuo


class Chessboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8 Reinas con Algoritmo Genético")
        self.canvas = Canvas(self, width=SIZE * DIMENSION, height=SIZE * DIMENSION)
        self.canvas.pack(pady=20)

    def draw_board_with_solution(self, solution):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                x1, y1 = col * SIZE, row * SIZE
                x2, y2 = x1 + SIZE, y1 + SIZE

                color = "white" if (row + col) % 2 == 0 else "black"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        for col, row in enumerate(solution):
            x, y = (col + 0.5) * SIZE, (row + 0.5) * SIZE
            self.canvas.create_text(x, y, text="♛", font=FONT_QUEEN, fill=COLOR_QUEEN)

        self.mainloop()


def algoritmo_genetico():
    num_poblacion = 500
    generaciones = 100
    prob_mutacion = 0.05

    poblacion = [np.random.permutation(8) for _ in range(num_poblacion)]

    for generacion in range(generaciones):
        fit_values = [fitness(ind) for ind in poblacion]
        total_fit = sum(fit_values)
        probabilidades = [i / total_fit for i in fit_values]
        probabilidades = [i/sum(probabilidades) for i in probabilidades]

        nuevos_individuos = []

        for _ in range(num_poblacion // 2):
            padre1, padre2 = seleccionar_padres(poblacion, probabilidades)
            hijo1, hijo2 = crossover(padre1, padre2)
            nuevos_individuos.extend([hijo1, hijo2])

        poblacion = nuevos_individuos

        if random.random() < prob_mutacion:
            indice = np.random.randint(0, len(poblacion))
            individuo_a_mutar = poblacion[indice]
            mutar(individuo_a_mutar)

        fit_values = [fitness(ind) for ind in poblacion]
        mejor_fit = max(fit_values)
        if mejor_fit == 28:
            print(f"Generación {generacion + 1}: Solución encontrada!")
            solucion = poblacion[fit_values.index(mejor_fit)]
            print(solucion)
            app = Chessboard()
            app.draw_board_with_solution(solucion)
            break
        else:
            print(f"Generación {generacion + 1}: Mejor fitness = {mejor_fit}")


if __name__ == "__main__":
    algoritmo_genetico()
