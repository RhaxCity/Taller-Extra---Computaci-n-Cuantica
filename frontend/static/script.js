async function runGrover(event) {
    event.preventDefault(); // Evitar que el formulario se envíe y la página se recargue
    
    // Obtener los valores del formulario
    const n = document.getElementById('n').value;
    const target = document.getElementById('target').value;
    
    // Hacer la solicitud POST al servidor Flask
    const response = await fetch('http://localhost:5001/grover', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ n: parseInt(n), target: parseInt(target) })
    });
    
    // Obtener los datos de la respuesta
    const data = await response.json();
    
    // Mostrar los resultados
    const summary = `
        <p><strong>Algoritmo:</strong> Grover</p>
        <p><strong>Valor objetivo:</strong> ${data.target}</p>
        <p><strong>Encontrado:</strong> ${data.occurrences} veces en ${data.attempts} intentos.</p>
        <p><strong>Tiempo:</strong> ${data.time.toFixed(4)} segundos.</p>
    `;
    document.getElementById('summary').innerHTML = summary;
    
    // Mostrar la imagen del circuito cuántico
    const circuitImageHTML = `
        <h3>Circuito Cuántico:</h3>
        <img src="data:image/png;base64,${data.circuit_image}" alt="Circuito Cuántico de Grover">
    `;
    document.getElementById('circuitImage').innerHTML = circuitImageHTML;
    
    // Mostrar el archivo de resultados en formato JSON
    const resultFileHTML = `
        <h3>Archivo de Resultados:</h3>
        <pre>${JSON.stringify(data, null, 4)}</pre>
    `;
    document.getElementById('resultFile').innerHTML = resultFileHTML;
}

async function runLinear(event) {
    event.preventDefault(); // Evitar que el formulario se envíe y la página se recargue
    
    // Obtener los valores del formulario
    const n = document.getElementById('n').value;
    const target = document.getElementById('target').value;
    
    // Hacer la solicitud POST al servidor Flask
    const response = await fetch('http://localhost:5001/linear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ n: parseInt(n), target: parseInt(target) })
    });
    
    // Obtener los datos de la respuesta
    const data = await response.json();
    
    // Mostrar los resultados de la búsqueda lineal
    const summary = `
        <p><strong>Algoritmo:</strong> Búsqueda Lineal</p>
        <p><strong>Índice encontrado:</strong> ${data.index}</p>
        <p><strong>Iteraciones:</strong> ${data.iterations}</p>
        <p><strong>Tiempo:</strong> ${data.time.toFixed(4)} segundos.</p>
    `;
    document.getElementById('summary').innerHTML = summary;
    
    // Mostrar el archivo de resultados en formato JSON
    const resultFileHTML = `
        <h3>Archivo de Resultados:</h3>
        <pre>${JSON.stringify(data, null, 4)}</pre>
    `;
    document.getElementById('resultFile').innerHTML = resultFileHTML;
}

// Añadir un evento de escucha al formulario para evitar el envío por defecto
document.getElementById("searchForm").addEventListener("submit", function(event) {
    const algorithm = document.getElementById("algorithm").value;
    if (algorithm === "grover") {
        runGrover(event);
    } else if (algorithm === "linear") {
        runLinear(event);
    }
});
