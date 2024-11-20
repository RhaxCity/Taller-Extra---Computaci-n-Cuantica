# Proyecto de Búsqueda Cuántica y Lineal
---
Desarrollado por: Juan José Gómez Arenas
---
Este proyecto implementa dos algoritmos de búsqueda: **Búsqueda Lineal** y **Búsqueda Cuántica de Grover**, ambos accesibles a través de una API REST. El objetivo es comparar el rendimiento de estos algoritmos en un conjunto de datos.

## Descripción

1. **Búsqueda Lineal**: Recorrido secuencial de una lista de elementos hasta encontrar el objetivo. Complejidad O(N), donde N es el tamaño de la lista.
2. **Búsqueda Cuántica de Grover**: Utiliza principios de la computación cuántica para buscar un objetivo en un conjunto de datos no ordenado de manera más eficiente, con una complejidad O(√N).

## Tecnologías

- **Flask**: Para crear la API REST.
- **Qiskit**: Para implementar y simular el algoritmo de Grover.
- **Docker**: Para crear y ejecutar el contenedor de la aplicación.

## Requisitos

- Docker y Docker Compose instalados.

## Instalación y Ejecución

1. **Construir la imagen Docker**:

   En el directorio raíz del proyecto, ejecuta el siguiente comando para construir la imagen Docker:

   ```bash
   docker-compose build
   docker-compose up
   ```
   
   Esto iniciará el servidor en http://localhost:5000.
