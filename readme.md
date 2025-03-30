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

*Ejecutar fastapi y un contenedor con docker compose
    1.- Iniciar el docker compose "docker-compose up -d --build"
    2.- Crear una nueva conexion en tu SMBD con usuario "user", contraseña "password" (si te lo solicita) y puerto 3307 (hecho asi, para evitar colisiones con otra base de datos ya hecha anteriormente).
    3.- Si deseas levantar un docker compose que ya haya sido compilado y no has movido nada en el codigo solo usa "docker-compose up -d"

*Detener docker compose fastapi
    1.-docker-compose stop

*Para eliminar todo (contenedores, network y volumen):
    1.-docker-compose down -v