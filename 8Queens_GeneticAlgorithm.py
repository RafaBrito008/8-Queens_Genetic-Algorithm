import tkinter as tk
from tkinter import Button, Label, Frame, messagebox
import random

DIMENSION = 8
SIZE = 50
COLORS = {"white": "white", "black": "black", "queen": "red"}
FONT_QUEEN = ("Arial", int(SIZE / 1.5))
POBLACION_INICIAL = 100
PROB_MUTACION = 0.1

# Funciones auxiliares del Algoritmo Genético


def generar_individuo():
    positions = list(range(DIMENSION))
    random.shuffle(positions)
    return positions


def seleccionar_padres(poblacion, fitnesses):
    indices = list(range(len(poblacion)))
    selected = random.choices(indices, weights=fitnesses, k=2)
    return poblacion[selected[0]], poblacion[selected[1]]


def crossover(padre1, padre2):
    punto_cruce = random.randint(0, DIMENSION - 1)
    hijo1 = padre1[:punto_cruce] + padre2[punto_cruce:]
    hijo2 = padre2[:punto_cruce] + padre1[punto_cruce:]
    return hijo1, hijo2


def mutar(individuo):
    if random.random() < PROB_MUTACION:
        col = random.randint(0, DIMENSION - 1)
        row = random.randint(0, DIMENSION - 1)
        individuo[col] = row
    return individuo


def fitness(individuo):
    # Queremos maximizar el fitness, por lo que restamos los conflictos al valor máximo posible
    return DIMENSION * (DIMENSION - 1) // 2 - count_conflicts(individuo)


def count_conflicts(positions):
    conflicts = 0
    for i in range(DIMENSION):
        for j in range(i + 1, DIMENSION):
            if j >= len(positions):  # Añade esta línea
                continue
            if positions[i] == positions[j]:
                conflicts += 1
            if abs(positions[i] - positions[j]) == abs(i - j):
                conflicts += 1
    return conflicts


class Chessboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("8 Reinas")

        self.board = [[None for _ in range(DIMENSION)] for _ in range(DIMENSION)]
        self.queens = []

        self.setup_ui()
        self.draw_board()
        self.place_queens_randomly()

    def setup_ui(self):
        # Crear el canvas para dibujar el tablero y las reinas
        self.canvas = tk.Canvas(self, width=SIZE * DIMENSION, height=SIZE * DIMENSION)
        self.canvas.pack(pady=20)

        self.control_frame = Frame(self)
        self.control_frame.pack(pady=10)

        # Botón para mezclar las reinas
        self.shuffle_button = Button(
            self.control_frame, text="Mezclar", command=self.place_queens_randomly
        )
        self.shuffle_button.grid(row=0, column=0, padx=10)

        # Botón para aplicar Hill Climbing Estocástico
        self.next_step_button = Button(
            self.control_frame, text="Siguiente", command=self.algoritmo_genetico_step
        )
        self.next_step_button.grid(row=0, column=1, padx=10)

        self.conflict_label = Label(
            self.control_frame, text="Conflictos: 0", font=("Arial", 12)
        )
        self.conflict_label.grid(row=0, column=2, padx=20)

    def update_conflict_label(self):
        positions = [
            int(self.canvas.coords(queen)[1] / SIZE - 0.5) for queen in self.queens
        ]
        conflicts = self.count_conflicts(positions)
        self.conflict_label.config(text=f"Conflictos: {conflicts}")

    def draw_board(self):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                x1, y1 = col * SIZE, row * SIZE
                x2, y2 = x1 + SIZE, y1 + SIZE

                color = "white" if (row + col) % 2 == 0 else "black"

                self.board[row][col] = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color
                )

    def place_queens_randomly(self):
        # Eliminar las reinas actuales
        for queen in self.queens:
            self.canvas.delete(queen)

        self.queens.clear()

        positions = list(range(DIMENSION))
        random.shuffle(positions)

        for col, row in enumerate(positions):
            self.place_queen(row, col)
        self.update_conflict_label()

    def place_queen(self, row, col):
        x, y = (col + 0.5) * SIZE, (row + 0.5) * SIZE
        queen = self.canvas.create_text(
            x, y, text="♛", font=("Arial", int(SIZE / 1.5)), fill="red"
        )
        self.queens.append(queen)

    def count_conflicts(self, positions):
        # Cuenta los conflictos entre reinas basado en sus posiciones
        conflicts = 0
        for i in range(DIMENSION):
            for j in range(i + 1, DIMENSION):
                if j >= len(positions):  # Añade esta línea
                    continue
                if positions[i] == positions[j]:
                    conflicts += 1
                if abs(positions[i] - positions[j]) == abs(i - j):
                    conflicts += 1
        return conflicts

    def get_neighbors(self, positions):
        # Devuelve todos los vecinos posibles (movimientos de una reina a otra fila)
        neighbors = []
        for col in range(DIMENSION):
            for row in range(DIMENSION):
                if row != positions[col]:
                    new_positions = positions.copy()
                    new_positions[col] = row
                    neighbors.append(new_positions)
        return neighbors

    def algoritmo_genetico_step(self):
        # Paso 1: Población inicial
        poblacion = [generar_individuo() for _ in range(POBLACION_INICIAL)]

        solucion = None  # Valor predeterminado

        for _ in range(100):  # 100 generaciones como criterio de detención
            fitnesses = [fitness(individuo) for individuo in poblacion]

            # Si algún individuo tiene el fitness máximo, lo encontramos
            if DIMENSION * (DIMENSION - 1) // 2 in fitnesses:
                solucion = poblacion[fitnesses.index(DIMENSION * (DIMENSION - 1) // 2)]
                break

            # Paso 2: Selección de padres
            # Paso 3: Crossover
            # Paso 4: Mutación
            nuevos_individuos = []
            for _ in range(len(poblacion) // 2):
                padre1, padre2 = seleccionar_padres(poblacion, fitnesses)
                hijo1, hijo2 = crossover(padre1, padre2)
                nuevos_individuos.append(mutar(hijo1))
                nuevos_individuos.append(mutar(hijo2))

            # Paso 5: Selección N individuos (usamos toda la nueva generación)
            poblacion = nuevos_individuos

        if solucion is not None:
            for queen in self.queens:
                self.canvas.delete(queen)
            self.queens.clear()
            for col, row in enumerate(solucion):
                self.place_queen(row, col)
            self.update_conflict_label()
        else:
            messagebox.showwarning(
                "Advertencia", "No se encontró una solución óptima en las generaciones definidas."
            )

        # Actualizar el tablero con la mejor solución encontrada
        for queen in self.queens:
            self.canvas.delete(queen)
        self.queens.clear()
        for col, row in enumerate(solucion):
            self.place_queen(row, col)

        self.update_conflict_label()


if __name__ == "__main__":
    app = Chessboard()
    app.mainloop()
