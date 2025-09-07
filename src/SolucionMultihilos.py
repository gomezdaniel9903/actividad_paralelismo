import random
import time
import threading

resultado = {}
def sequential_matrix_multiplication(A, B, hilo):
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
    resultado[hilo] = C
    return C

def generate_random_matrix(rows, cols):
    """Genera una matriz con valores flotantes aleatorios entre 0 y 1."""
    matrix = [[random.random() for _ in range(cols)] for _ in range(rows)]
    return matrix

def dividir_chunks(num_threads,matrix_size,matrix):
    x = matrix_size//num_threads
    chunks = []
    for i in range(num_threads - 1):
        chunks.append(matrix[x*i:x*i + x])
    chunks.append(matrix[(num_threads - 1)*x:])
    return chunks

def solucion_multihilos():
    global resultado
    # Pueden ajustar este valor si su máquina tiene más o menos recursos.
    # ¡Cuidado con valores muy grandes que puedan colgar su sistema!
    MATRIX_SIZE = 500
    
    print(f"Generando matrices aleatorias de {MATRIX_SIZE}x{MATRIX_SIZE}...")
    
    # Generar las dos matrices a multiplicar
    times = []
    resultados = []
    for num_threads in [2,4,6,8]:
        matrix_A = generate_random_matrix(MATRIX_SIZE, MATRIX_SIZE)
        matrix_B = generate_random_matrix(MATRIX_SIZE, MATRIX_SIZE)
        chunks_A = dividir_chunks(num_threads,MATRIX_SIZE,matrix_A)
        print("Matrices generadas. Iniciando multiplicación paralelo multihilos...")
        threads = []
        
     
        # Medir el tiempo de ejecución
        start_time = time.time()
        for thread in range(num_threads):
            h = threading.Thread(target=sequential_matrix_multiplication, name='Hilo {}'.format(str(thread)), args=(chunks_A[thread],matrix_B,thread))
            threads.append(h)
            h.start()
    
        for thread in threads:
            thread.join()

        end_time = time.time()

        matrix_global = []
        keys = list(resultado.keys())
        keys.sort()
        for key in keys:
            matrix_global += resultado[key]
        
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        resultados.append(matrix_global)
        
        
        print(f"La multiplicación secuencial ha finalizado.")
        print(f"Tiempo total de ejecución: {elapsed_time:.4f} segundos.")
        resultado = {}
    return times