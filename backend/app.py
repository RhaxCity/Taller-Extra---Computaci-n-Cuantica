import base64
from io import BytesIO
from flask import Flask, request, jsonify
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import random
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Implementación del algoritmo de búsqueda cuántica de Grover
def grover_search(n, target, max_attempts=100, shots=4096):
    """
    Implementa el algoritmo de búsqueda de Grover para buscar un target en una lista de 2^n elementos.
    """
    sim = AerSimulator()

    # Validar y convertir el target
    if isinstance(target, str) and target.isdigit():
        target = int(target)
    elif isinstance(target, str):
        return {"error": "El target debe ser un número entero válido."}

    # Convertir el target a binario con n bits
    target_bin = bin(target)[2:].zfill(n)

    # Crear el oráculo de Grover que identifica el estado objetivo
    oracle = QuantumCircuit(n)
    for i, bit in enumerate(target_bin):
        if bit == "0":
            oracle.x(i)  # Flip en posiciones donde el bit objetivo es 0

    oracle.h(range(n))  # Operaciones del oráculo
    oracle.x(range(n))
    oracle.h(range(n))

    # Circuito principal de Grover
    grover_circuit = QuantumCircuit(n)
    grover_circuit.h(range(n))  # Inicializar qubits en superposición
    grover_circuit.compose(oracle, inplace=True)  # Aplicar el oráculo

    attempts = 0
    occurrence_count = 0

    # Repetir el algoritmo hasta encontrar el objetivo o agotar intentos
    while attempts < max_attempts:
        # Operador de difusión para amplificación de amplitud
        grover_circuit.h(range(n))
        grover_circuit.x(range(n))
        grover_circuit.h(n - 1)
        grover_circuit.cx(range(n - 1), n - 1)
        grover_circuit.h(n - 1)
        grover_circuit.x(range(n))
        grover_circuit.h(range(n))

        grover_circuit.measure_all()  # Medir el circuito cuántico

        # Transpilar y simular el circuito
        transpiled_circuit = transpile(grover_circuit, sim, optimization_level=2)
        result = sim.run(transpiled_circuit, shots=shots).result()
        counts = result.get_counts()

        # Imprimir los resultados para depuración
        print(f"Intento {attempts + 1}: counts = {counts}")

        # Contar las ocurrencias del target
        occurrence_count = counts.get(target_bin, 0)

        if occurrence_count > 0:
            break  # Salir si encontramos el objetivo

        attempts += 1  # Incrementar intentos si no se encuentra

    # Si no se encuentra, el número de intentos es el máximo alcanzado
    if occurrence_count == 0:
        attempts = max_attempts

    # Generar la imagen del circuito en memoria
    buffer = BytesIO()
    grover_circuit.draw(output='mpl').savefig(buffer, format='png')
    buffer.seek(0)

    # Codificar la imagen en base64
    circuit_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return occurrence_count, attempts, circuit_image_base64


# Implementación de búsqueda lineal clásica
def linear_search(data_set, target):
    """
    Busca un valor objetivo en un conjunto de datos de forma secuencial.
    """
    iterations = 0
    for i, value in enumerate(data_set):
        iterations += 1
        if value == target:
            return i, iterations
    return -1, iterations


@app.route('/grover', methods=['POST'])
def grover_endpoint():
    """
    Endpoint para realizar la búsqueda cuántica con el algoritmo de Grover.
    """
    data = request.get_json()
    n = data['n']
    target = data['target']

    # Medir el tiempo de ejecución
    start_time = time.time()

    # Llamar al algoritmo de Grover
    occurrence_count, attempts, circuit_image_base64 = grover_search(n, target)

    # Medir el tiempo transcurrido
    elapsed_time = time.time() - start_time

    # Crear la respuesta con los resultados y la imagen en base64
    return jsonify({
        "algorithm": "Grover's Search",
        "target": target,
        "occurrences": occurrence_count,  # Ocurrencias del target
        "attempts": attempts,  # Número de intentos hasta encontrarlo
        "time": elapsed_time,
        "circuit_image": circuit_image_base64  # Imagen codificada en base64
    })


@app.route('/linear', methods=['POST'])
def linear_endpoint():
    """
    Endpoint para realizar la búsqueda lineal clásica.
    """
    data = request.get_json()
    n = data['n']
    target = data['target']

    # Crear un conjunto de datos de tamaño 2^n
    data_set = [random.randint(0, 1000) for _ in range(2**n)]

    # Asegurar que el target esté en el conjunto de datos en una posición aleatoria
    random_position = random.randint(0, len(data_set) - 1)
    data_set[random_position] = target

    # Medir el tiempo de ejecución
    start_time = time.time()

    # Llamar a la búsqueda lineal
    index, iterations = linear_search(data_set, target)

    # Medir el tiempo transcurrido
    elapsed_time = time.time() - start_time

    return jsonify({
        "algorithm": "Linear Search",
        "size": len(data_set),  # Tamaño del conjunto de datos
        "target": target,
        "index": index,  # Índice donde se encontró el target
        "iterations": iterations,  # Número de iteraciones
        "time": elapsed_time
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
