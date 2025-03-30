*Iniciar el proyecto cuando no es un contenedor
    1.- Crear un entorno virtual "python3 -m venv venv"
    2.- Activar el entorno virtual "en PowerShell → venv\Scripts\Activate, en CMD → venv\Scripts\activate.bat
    3.- Instalar todas las dependencias que se necesitan "pip install -r requirements.txt"

*Ejecutar fastapi cuando no es un contenedor 2 formas
    uvicorn main:app
    python .\main.py

*Ejecutar fastapi en contendor
    1.- docker build -t fastapi-app:1 .
    2.- docker run --name fastapi-container -d --rm -p 8000:8000 fastapi-app:1
NOTA: La API está configurada para correr con un base de datos de mysql llamada "DistributedSystems", con un usuario "root", que está en un contenedor que se mapea al puerto "3307", con la contraseña "password", para cambiar eso, entra a app/db/session.py y modifica lo necesario en la variable SQLALCHEMY_DATABASE_URL. Si quieres ejecutarlo en un SMBD fuera de un contenedor tambien deberas de cambiar el host "host.docker.internal" a "localhost".