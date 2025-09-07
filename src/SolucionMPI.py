from mpi4py import MPI
import random
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
ntasks = comm.Get_size()


def sequential_matrix_multiplication(A, B):
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


if rank == 0:
    # Pueden ajustar este valor si su máquina tiene más o menos recursos.
    # ¡Cuidado con valores muy grandes que puedan colgar su sistema!
    MATRIX_SIZE = 500

    print(f"Generando matrices aleatorias de {MATRIX_SIZE}x{MATRIX_SIZE}...")

    # Generar las dos matrices a multiplicar
    matrix_A = generate_random_matrix(MATRIX_SIZE, MATRIX_SIZE)
    matrix_B = generate_random_matrix(MATRIX_SIZE, MATRIX_SIZE)
    chunks_A = dividir_chunks(ntasks,MATRIX_SIZE,matrix_A)
    print("Matrices generadas. Iniciando multiplicación paralelo multihilos...")
    # Medir el tiempo de ejecución
    start_time = time.time()
    for i in range(1,ntasks):
        comm.send([chunks_A[i],matrix_B], dest=i)
    part_0 = sequential_matrix_multiplication(chunks_A[0],matrix_B) ##Aquí trabaja el nodo maestro también
    resultado = {}
    resultado[0] = part_0
    for i in range(1,ntasks):
        resultado[i] = comm.recv(source=i)

    matrix_global = []
    keys = list(resultado.keys())
    keys.sort()
    for key in keys:
        matrix_global += resultado[key]

    end_time = time.time()

    elapsed_time = end_time - start_time



    print(f"La multiplicación secuencial ha finalizado.")
    print(f"Tiempo total de ejecución: {elapsed_time:.4f} segundos.")

    with open("resultado_mpi.txt", "a") as f:
        f.write(str(elapsed_time)+",")


else:
    my_part = comm.recv(source=0)
    comm.send(sequential_matrix_multiplication(my_part[0],my_part[1]), dest=0)