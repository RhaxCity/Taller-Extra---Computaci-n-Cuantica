from flask import Flask, request, jsonify, send_from_directory
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import random
import time
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="/")

# Modificado: Aumento de iteraciones y shots
def grover_search(n, target, max_attempts=100, shots=4096):
    sim = AerSimulator()

    # Convertir el target a entero si es una cadena numérica
    if isinstance(target, str) and target.isdigit():
        target = int(target)
    elif isinstance(target, str):
        return {"error": "El target debe ser un número entero válido."}

    # Convertir el target a binario
    target = bin(target)[2:].zfill(n)  # Convertir a binario y rellenar con ceros a la izquierda hasta 'n' bits

    # Crear el oracle que marca el valor objetivo
    oracle = QuantumCircuit(n)
    for i, bit in enumerate(target):
        if bit == "0":
            oracle.x(i)  # Aplica X si el bit es 0 en el target
    oracle.h(range(n))  # Apply Hadamard to all qubits
    oracle.x(range(n))  # Apply X to all qubits
    oracle.h(range(n))  # Apply Hadamard again to complete the oracle

    # Circuito de Grover
    grover_circuit = QuantumCircuit(n)
    grover_circuit.h(range(n))  # Inicializar los qubits en estados de superposición
    grover_circuit.compose(oracle, inplace=True)  # Aplicar el oracle

    # Intentos hasta encontrar el valor objetivo
    attempts = 0
    occurrence_count = 0

    while attempts < max_attempts:
        # Operación de amplificación de amplitud (diffusion operator)
        grover_circuit.h(range(n))
        grover_circuit.x(range(n))
        grover_circuit.h(n-1)
        grover_circuit.cx(range(n-1), n-1)
        grover_circuit.h(n-1)
        grover_circuit.x(range(n))
        grover_circuit.h(range(n))

        grover_circuit.measure_all()  # Medir los qubits

        # Transpilar el circuito
        transpiled_circuit = transpile(grover_circuit, sim, optimization_level=2)

        # Ejecutar la simulación
        result = sim.run(transpiled_circuit, shots=shots).result()
        counts = result.get_counts()

        # Asegurarse de contar correctamente las ocurrencias del target
        occurrence_count = counts.get(target, 0)  # Número de veces que aparece el target

        if occurrence_count > 0:
            break  # Si encontramos el objetivo, salimos del ciclo

        attempts += 1  # Si no se encuentra, intentamos nuevamente

    return occurrence_count, attempts  # Devuelve el número de ocurrencias y el número de intentos realizados

# Búsqueda lineal
def linear_search(data_set, target):
    iterations = 0
    for i, value in enumerate(data_set):
        iterations += 1
        if value == target:
            return i, iterations  # Retorna la posición y el número de iteraciones
    return -1, iterations  # Si no se encuentra el target, retorna -1 y el número de iteraciones

@app.route('/grover', methods=['POST'])
def grover_endpoint():
    start_time = time.time()
    try:
        request_data = request.get_json()
        app.logger.info(f"Datos recibidos en /grover: {request_data}")

        # Verifica que los datos sean válidos
        if 'n' not in request_data or 'target' not in request_data:
            return jsonify({"error": "Faltan parámetros: 'n' y/o 'target'"}), 400

        n = request_data['n']
        target = request_data['target']

        # Asegurarse de que 'n' es un número entero válido y que 'target' no está vacío
        if not isinstance(n, int) or n <= 0 or not target:
            return jsonify({"error": "'n' debe ser un número entero positivo y 'target' no puede estar vacío."}), 400

        # Realizar búsqueda cuántica de Grover
        grover_result = grover_search(n, target)

        if isinstance(grover_result, dict) and 'error' in grover_result:
            return jsonify(grover_result), 400

        occurrence_count = grover_result
        elapsed_time = time.time() - start_time

        return jsonify({
            "algorithm": "Grover",
            "data_set_size": 2**n,  # Tamaño de la base de datos (2^n)
            "target": target,
            "occurrences": occurrence_count,  # Ocurrencias encontradas en las simulaciones de Grover
            "iterations": 1,  # Para Grover, no contamos las iteraciones explícitamente, ya que solo tenemos el conteo
            "time": elapsed_time
        })

    except Exception as e:
        app.logger.error(f"Error en /grover: {str(e)}")
        return jsonify({"error": f"Error en la solicitud: {str(e)}"}), 400

@app.route('/linear', methods=['POST'])
def linear_endpoint():
    start_time = time.time()
    try:
        request_data = request.get_json()
        app.logger.info(f"Datos recibidos en /linear: {request_data}")

        # Verifica que los datos sean válidos
        if 'n' not in request_data or 'target' not in request_data:
            return jsonify({"error": "Faltan parámetros: 'n' y/o 'target'"}), 400

        n = request_data['n']
        target = request_data['target']

        # Asegurarse de que 'n' es un número entero válido y que 'target' no está vacío
        if not isinstance(n, int) or n <= 0 or not target:
            return jsonify({"error": "'n' debe ser un número entero positivo y 'target' no puede estar vacío."}), 400

        # Generar el conjunto de datos
        data_set = random.sample(range(1, 2**n), 2**n - 1)  # Crear un conjunto de números del 1 a 2^n - 1
        data_set.append(target)  # Añadir el valor de target en una posición aleatoria

        # Realizar búsqueda lineal
        result_index, iterations = linear_search(data_set, target)
        elapsed_time = time.time() - start_time

        return jsonify({
            "algorithm": "Linear Search",
            "data_set_size": 2**n,  # Tamaño de la lista generada (2^n elementos)
            "target": target,
            "result_index": result_index,
            "iterations": iterations,
            "time": elapsed_time
        })

    except Exception as e:
        app.logger.error(f"Error en /linear: {str(e)}")
        return jsonify({"error": f"Error en la solicitud: {str(e)}"}), 400

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
