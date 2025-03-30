*Ejecutar fastapi cuando no es un contenedor 2 formas
    1.- uvicorn main:app
    2.- python .\main.py

*Ejecutar fastapi en contendor
    1.- docker build -t fastapi-app:1 .
    2.- docker run --name fastapi-container -d --rm -p 8000:8000 fastapi-app:1
NOTA: esta configurado para correr con un base de datos que está en un contender en el puerto 3307, para cambiar eso, entra a app/db/session.py y modifica el puerto que esta en la variable SQLALCHEMY_DATABASE_URL. Si quieres ejecutarlo en un SMBD fuera de un contenedor tambien deberas de cambiar el host "host.docker.internal" a "localhost".