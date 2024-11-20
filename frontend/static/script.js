async function handleSubmit(event) {
    event.preventDefault();

    const n = document.getElementById("n").value;
    const target = document.getElementById("target").value;
    const algorithm = document.getElementById("algorithm").value;

    const requestData = {
        n: parseInt(n),
        target: target
    };

    const url = algorithm === "grover" ? "/grover" : "/linear";
    
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        const result = await response.json();
        document.getElementById("result").innerHTML = JSON.stringify(result, null, 2);
    } catch (error) {
        console.error('Error en la solicitud:', error);
        document.getElementById("result").innerHTML = 'Hubo un error al realizar la solicitud.';
    }
}

document.getElementById('searchForm').addEventListener('submit', handleSubmit);
