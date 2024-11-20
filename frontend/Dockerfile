# Imagen base con Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el código del frontend al contenedor
COPY . /app

# Instalar Flask para servir archivos estáticos
RUN pip install --no-cache-dir flask

# Exponer el puerto en el que Flask ejecutará la aplicación
EXPOSE 5000

# Comando para ejecutar el servidor Flask
CMD ["python", "app.py"]
