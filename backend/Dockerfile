# 1. Imagen base de Python ligera
FROM python:3.12-slim

# 2. Evitar que Python genere archivos .pyc y que el output sea lento
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalamos dependencias del sistema necesarias para Postgres
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# 5. Instalamos las librerías de Python
# Nota: Ahora crearemos el archivo requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos el código de nuestra carpeta backend a /app
COPY . .

# 7. Comando para arrancar la API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]