# Imagen base con Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el código del backend al contenedor
COPY . /app

# Instalar las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que Flask ejecutará la aplicación
EXPOSE 5001

# Comando para ejecutar el servidor Flask
CMD ["python", "app.py"]
