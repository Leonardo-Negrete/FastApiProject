# Usamos una imagen base de Python (3.10 o 3.11, la que prefieras)
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
# (Primero copiamos requirements para hacer cache de dependencias)
COPY requirements.txt ./

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu código al contenedor
COPY . .

# Expone el puerto que utilizará la aplicación
EXPOSE 8000

# Comando para ejecutar la app con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
