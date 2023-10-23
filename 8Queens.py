import tkinter as tk
from tkinter import Button, Label, Frame, messagebox
import random

DIMENSION = 8  # Dimensiones del tablero (8x8)
SIZE = 50  # Tamaño de cada casilla en píxeles
COLORS = {"white": "white", "black": "black", "queen": "red"}
FONT_QUEEN = ("Arial", int(SIZE / 1.5))


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
            self.control_frame, text="Siguiente", command=self.hill_climbing_step
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

    def hill_climbing_step(self):
        # Aplica un paso del algoritmo Hill Climbing Estocástico
        positions = [
            int(self.canvas.coords(queen)[1] / SIZE - 0.5) for queen in self.queens
        ]

        current_conflicts = self.count_conflicts(positions)

        # Verificar si hemos encontrado una solución
        if current_conflicts == 0:
            messagebox.showinfo("¡Éxito!", "El tablero está resuelto")
            return

        # Inicializa mejor conflicto con el actual
        best_conflict = current_conflicts
        best_position = None

        for neighbor in self.get_neighbors(positions):
            conflicts = self.count_conflicts(neighbor)

            # Si encontramos una solución mejor, la guardamos
            if conflicts < best_conflict:
                best_conflict = conflicts
                best_position = neighbor

                # Si el conflicto es 0, ya encontramos la mejor solución
                if best_conflict == 0:
                    break

        if best_position is None:
            # No se encontró una mejor posición, por lo que es un óptimo local
            print("Óptimo local alcanzado. Reintentando...")
            self.place_queens_randomly()
            return

        # Si la mejor posición encontrada es diferente de la actual, actualizamos el tablero
        if best_position != positions:
            for queen in self.queens:
                self.canvas.delete(queen)
            self.queens.clear()

            for col, row in enumerate(best_position):
                self.place_queen(row, col)

        self.update_conflict_label()


if __name__ == "__main__":
    app = Chessboard()
    app.mainloop()
