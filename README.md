🧠 Proyecto de Paralelismo en Python
===================================

Este proyecto implementa diferentes enfoques de paralelismo para la multiplicación de matrices en Python.

-----------------------------------

⚙️ Configuración del entorno
----------------------------

Se recomienda usar un entorno virtual para manejar las dependencias de forma aislada.

1. Crear un entorno virtual

    python -m venv venv

2. Activar el entorno virtual

    - En Windows:

        venv\Scripts\activate

    - En Linux/macOS:

        source venv/bin/activate

3. Instalar dependencias

    pip install -r requirements.txt

4. Es obligatorio tener instalado el MPI en el sistema para correr el proyecto.

-----------------------------------

🚀 Ejecutar el programa principal
---------------------------------

Una vez activado el entorno y con las dependencias instaladas, ejecuta:

    python main.py
    
En caso de tener python3 se utilizaría el comando anterior con python3

-----------------------------------

📂 Estructura esperada del proyecto
-----------------------------------

    Proyecto/
    ├── main.py
    ├── requirements.txt
    ├── README.md
    └── src/
        ├── __init__.py
        ├── SolucionMultihilos.py
        ├── SolucionMultiprocessing.py
        ├── SolucionMPI.py
        └── SolucionSecuencial.py

-----------------------------------

