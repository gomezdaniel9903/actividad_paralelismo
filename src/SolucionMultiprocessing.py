# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 17:25:37 2025

@author: User
"""

import random
import time
import multiprocessing
from multiprocessing import Manager


def sequential_matrix_multiplication(A, B, procesador,resultado):
    """
    Realiza la multiplicación de dos matrices de forma secuencial.
    Asume que las dimensiones son compatibles para la multiplicación.
    """
    # Dimensiones de las matrices
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        raise ValueError("Las dimensiones de las matrices no son compatibles para la multiplicación.")

    # Inicializar la matriz resultado con ceros
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Proceso de multiplicación "a pedal"
    # Itera sobre las filas de A
    for i in range(rows_A):
        # Itera sobre las columnas de B
        for j in range(cols_B):
            # Itera sobre las filas de B (o columnas de A) para el producto punto
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    resultado[procesador] = C
    return C

def generate_random_matrix(rows, cols):
    """Genera una matriz con valores flotantes aleatorios entre 0 y 1."""
    matrix = [[random.random() for _ in range(cols)] for _ in range(rows)]
    return matrix

def dividir_chunks(num_procesos,matrix_size,matrix):
    x = matrix_size//num_procesos
    chunks = []
    for i in range(num_procesos - 1):
        chunks.append(matrix[x*i:x*i + x])
    chunks.append(matrix[(num_procesos - 1)*x:])
    return chunks

def solucion_multiprocessing(matrix_size):
    manager = Manager()
    resultado = manager.dict()
    # Pueden ajustar este valor si su máquina tiene más o menos recursos.
    # ¡Cuidado con valores muy grandes que puedan colgar su sistema!
    
    print(f"Generando matrices aleatorias de {matrix_size}x{matrix_size}...")
    times = []
    resultados = []
    # Generar las dos matrices a multiplicar
    for num_procesos in [2,4,6,8]:
        matrix_A = generate_random_matrix(matrix_size, matrix_size)
        matrix_B = generate_random_matrix(matrix_size, matrix_size)
        chunks_A = dividir_chunks(num_procesos,matrix_size,matrix_A)
        print(f"Matrices generadas. Iniciando multiplicación paralelo multiprocesos, numero procesos {num_procesos}...")
        procesos = []
        
        # Medir el tiempo de ejecución
        start_time = time.time()
        for proceso in range(num_procesos):
            p = multiprocessing.Process(target=sequential_matrix_multiplication, name='Proceso {}'.format(str(proceso)), args=(chunks_A[proceso],matrix_B,proceso,resultado))
            procesos.append(p)
            p.start()
    
        for proceso in procesos:
            proceso.join()
    
        matrix_global = []
        keys = list(resultado.keys())
        keys.sort()
        for key in keys:
        
            matrix_global += resultado[key]
            
        
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        
        times.append(elapsed_time)
        
        resultados.append(matrix_global)
        
        print(f"La multiplicación paralela multiprocessing ha finalizado.")
        print(f"Tiempo total de ejecución: {elapsed_time:.4f} segundos.")
        
        resultado = manager.dict()
    return times