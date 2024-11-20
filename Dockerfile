# Usar una imagen base con Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el backend al contenedor
COPY ./backend /app/backend

# Copiar el frontend al contenedor
COPY ./frontend /app/frontend

# Instalar dependencias
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Exponer el puerto para Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "/app/backend/app.py"]
