import numpy as np
import random
import matplotlib.pyplot as plt


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


def mostrar_tablero(solucion):
    tablero = np.zeros((8, 8))
    for i in range(8):
        tablero[solucion[i], i] = 1

    plt.imshow(tablero, cmap='binary')
    plt.show()


def algoritmo_genetico():
    num_poblacion = 100
    generaciones = 1000
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
            mostrar_tablero(solucion)
            break
        else:
            print(f"Generación {generacion + 1}: Mejor fitness = {mejor_fit}")


if __name__ == "__main__":
    algoritmo_genetico()
