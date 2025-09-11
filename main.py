from src import solucion_secuencial,solucion_multihilos, solucion_multiprocessing
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os
import sys
import argparse
plt.style.use('ggplot')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Script de Múltiplicación de matrices a pedal.")
    parser.add_argument("matrix_size", help="Dimensiones de las matrices cuadradas a múltiplicar")
    #parser.add_argument("edad", type=int)
    args = parser.parse_args()
    matrix_size = int(args.matrix_size)
    elapsed_time_secuential = solucion_secuencial(matrix_size)

    times_solucion_multihilos = solucion_multihilos(matrix_size)
    times_solucion_multiprocessing = solucion_multiprocessing(matrix_size)
    path_solution_mpi = './src/SolucionMPI.py'
    subprocess.run(['mpiexec', '-n', '2', sys.executable, path_solution_mpi,args.matrix_size],check=True)
    subprocess.run(['mpiexec', '-n', '4', sys.executable, path_solution_mpi,args.matrix_size],check=True)
    subprocess.run(['mpiexec', '-n', '6', sys.executable, path_solution_mpi,args.matrix_size],check=True)
    subprocess.run(['mpiexec', '-n', '8', sys.executable, path_solution_mpi,args.matrix_size],check=True)

    times_solution_mpi = []
    file_path = "resultado_mpi.txt"
    with open(file_path, "r") as file:
        content = file.read()
        times_solution_mpi = [float(x) for x in content[:-1].split(',')]

    os.remove(file_path)

########### Tiempos de ejecución y sus respectivas gráficas ##############
    t_1 = 8 # Tiempo que emplea el algoritmo ejecutandose secuencial
    n_hilos_procesos = np.array([1,2,4,6,8])
    t_paralelo_hilos = np.array([elapsed_time_secuential]+times_solucion_multihilos)
    t_paralelo_multiprocessing = np.array([elapsed_time_secuential]+times_solucion_multiprocessing)
    t_paralelo_mpi = np.array([elapsed_time_secuential]+times_solution_mpi)

    y_label = "Tiempo Ejecución (s)"
    plt.plot(n_hilos_procesos, t_paralelo_hilos)
    plt.xticks(n_hilos_procesos)
    plt.ylabel(y_label)
    plt.xlabel("Número de hilos [n]")
    plt.title('Tiempo Ejecución (s) Estrategia Multihilos')
    plt.figure() ##Para separar figuras

    plt.plot(n_hilos_procesos, t_paralelo_multiprocessing)
    plt.xticks(n_hilos_procesos)
    plt.ylabel(y_label)
    plt.xlabel("Número de procesos [n]")
    plt.title('Tiempo Ejecución (s) Estrategia Multiprocessing')
    plt.figure() ##Para separar figuras

    plt.plot(n_hilos_procesos, t_paralelo_mpi)
    plt.xticks(n_hilos_procesos)
    plt.ylabel(y_label)
    plt.xlabel("Número de nodos(procesos) MPI [n]")
    plt.title('Tiempo Ejecución (s) Estrategia MPI')
    plt.figure() ##Para separar figuras

    plt.plot(n_hilos_procesos, t_paralelo_hilos, label ="Multithreads")
    plt.plot(n_hilos_procesos, t_paralelo_multiprocessing, label ="Multiprocessing")
    plt.plot(n_hilos_procesos, t_paralelo_mpi, label ="MPI")
    
    plt.xticks(n_hilos_procesos)
    plt.ylabel(y_label)
    plt.xlabel("Número de hilos/procesos/procesos MPI [n]")
    plt.title('Comparación Tiempo Ejecución (s) Estrategias Paralelas')
    plt.legend()
    plt.figure() ##Para separar figuras
########### Cálculo de la Aceleración y sus respectivas gráficas ##############
    acel = elapsed_time_secuential / t_paralelo_hilos
    acel_multiprocessing = elapsed_time_secuential / t_paralelo_multiprocessing
    acel_mpi = elapsed_time_secuential / t_paralelo_mpi

    print("Aceleración máxima hilos:", max(acel))
    print("Aceleración máxima multiprocessing:", max(acel_multiprocessing))
    print("Aceleración máxima MPI:", max(acel_mpi))

    y_label = "Aceleración [X]"
    plt.plot(n_hilos_procesos, acel)
    plt.xticks(n_hilos_procesos)
    plt.ylabel(y_label)
    plt.xlabel("Número de hilos [n]")
    plt.title('Aceleración [X] Estrategia Multihilos')
    plt.figure() ##Para separar figuras

    plt.plot(n_hilos_procesos, acel_multiprocessing)
    plt.xticks(n_hilos_procesos)
    plt.ylabel(y_label)
    plt.xlabel("Número de procesos [n]")
    plt.title('Aceleración [X] Estrategia Multiprocessing')
    plt.figure() ##Para separar figuras

    plt.plot(n_hilos_procesos, acel_mpi)
    plt.xticks(n_hilos_procesos)
    plt.ylabel(y_label)
    plt.xlabel("Número de nodos(procesos) MPI [n]")
    plt.title('Aceleración [X] Estrategia MPI')
    plt.figure() ##Para separar figuras

    plt.plot(n_hilos_procesos, acel, label ="Multithreads")
    plt.plot(n_hilos_procesos, acel_multiprocessing, label ="Multiprocessing")
    plt.plot(n_hilos_procesos, acel_mpi, label ="MPI")
    
    plt.xticks(n_hilos_procesos)
    plt.ylabel(y_label)
    plt.xlabel("Número de hilos/procesos/procesos MPI [n]")
    plt.title('Comparación Aceleración [X] Estrategias Paralelas')
    plt.legend()
    plt.figure() ##Para separar figuras

    ########### Cálculo de la Eficiencia y sus respectivas gráficas ##############
    eficiencia_hilos = acel/n_hilos_procesos
    eficiencia_multiprocessing = acel_multiprocessing/n_hilos_procesos
    eficiencia_mpi = acel_mpi/n_hilos_procesos
    print("Eficiencia hilos:",eficiencia_hilos)
    print("Eficiencia multiprocessing:",eficiencia_multiprocessing)
    print("Eficiencia MPI:",eficiencia_mpi)
    y_label = "Eficiencia"
    plt.plot(n_hilos_procesos,eficiencia_hilos,'-o')
    plt.xlabel('Número de hilos')
    plt.ylabel(y_label)
    plt.title('Eficiencia de un algoritmo paralelo Multihilos')
    plt.figure() ##Para separar figuras
    plt.plot(n_hilos_procesos,eficiencia_multiprocessing,'-o')
    plt.xlabel('Número de procesos')
    plt.ylabel(y_label)
    plt.title('Eficiencia de un algoritmo paralelo Multiprocessing')
    plt.figure() ##Para separar figuras
    plt.plot(n_hilos_procesos,eficiencia_mpi,'-o')
    plt.xlabel('Número de procesos MPI')
    plt.ylabel(y_label)
    plt.title('Eficiencia de un algoritmo paralelo MPI')
    plt.figure() ##Para separar figuras

    plt.plot(n_hilos_procesos, eficiencia_hilos, label ="Multithreads")
    plt.plot(n_hilos_procesos, eficiencia_multiprocessing, label ="Multiprocessing")
    plt.plot(n_hilos_procesos, eficiencia_mpi, label ="MPI")
    
    plt.xticks(n_hilos_procesos)
    plt.ylabel(y_label)
    plt.xlabel("Número de hilos/procesos/procesos MPI [n]")
    plt.title('Comparación Eficiencias Estrategias Paralelas')
    plt.legend()
    plt.show()
