SE PIDE QUE USE LA PRIMER FORMA PARA CORRER EL PROYECTO YA QUE CON 2 COMANDOS YA SE EJECUTA TODO CON EL UNICO REQUISITO DE TENER DOCKER ABIERTO.

FORMA 1
*Ejecutar fastapi y un contenedor MySql con docker compose
    1.- EJECUTA EL SIGUIENTE COMANDO PARA Compilar el docker compose "docker-compose up -d --build"
    2.- Si deseas levantar un docker compose que ya haya sido compilado y no has movido nada en el codigo solo usa "docker-compose up -d"
    3.- Para acceder al swagger hay que colocar la siguiente url "http://localhost:8000/docs"
    4.- EN LOS ARCHIVOS DE CONFIGURACION SE USA LO SIGUIENTE  usuario "user", contraseña "password" y puerto 3307  CON ESTOS DATOS SE DEBE HACER LA CONEXION AL WORKBRENCH.
    5.-(opcional) para versionar la imagen de la api usa "docker tag fastapi-api:latest fastapi-api:<version>" despues de compliar el docker compose y no olvides borrar en docker desktop la version latest.

*Detener docker compose fastapi
    1.-docker-compose stop

*Para eliminar todo (contenedores, network y volumen):
    1.-docker-compose down -v

*Como probar la api en postman
    1.-Get con paginacion, ejemplo "http://localhost:8000/Users?name=a", debe de responder 200 si existen el o los usuarios sino, 200 (lista vacia)
    
    2-Get por id ejemplo, "http://localhost:8000/Users/1", debe de responder 200 si existe el usuario sino, 404 (no existe el usuario)

    3.-Post ejemplo, "http://localhost:8000/Users/" con el siguiente body:
    {
    "name": "Ana",
    "lastname": "Ramírez",
    "address": "Calle Luna 123",
    "phone": 554,
    "email": "ana.ramirez@example.com"
    }
    debe de responder 204 si se creo el usuario sino, 409 (si existe un usuario con el email duplicado)

    4.-Delete ejemplo, "http://localhost:8000/Users/1" debe de responder 204 si se elimino el usuario sino, 404 (no existe el usuario)

    5.-Update ejemplo, "http://localhost:8000/Users/1" con el siguiente body 
    {
    "name": "Ana",
    "lastname": "Ramírez",
    "address": "Calle Juan 123",
    "phone": 4562124896,
    "email": "ana.ramirez@example.com"
    }
    debe de responder 204 si se actualizo el usuario sino, 409 (si se quiere actualizar un usuario con un email que ya existe en otro usuario)






FORMA 2
*Ejecutar fastapi en contendor
    1.- docker build -t fastapi-app:1 .
    2.- docker run --name fastapi-container -d --rm -p 8000:8000 fastapi-app:1
NOTA: La API está configurada para correr con un base de datos de mysql llamada "DistributedSystems", con un usuario "root", que está en un contenedor que se mapea al puerto "3307", con la contraseña "password", para cambiar eso, entra a app/db/session.py y modifica lo necesario en la variable SQLALCHEMY_DATABASE_URL. Si quieres ejecutarlo en un SMBD fuera de un contenedor tambien deberas de cambiar el host "host.docker.internal" a "localhost".






OTRAS OPCIONES PARA EJECUTAR EL PROYECTO 
*Iniciar el proyecto cuando no es un contenedor
    1.- Crear un entorno virtual "python3 -m venv venv"
    2.- Activar el entorno virtual "en PowerShell → venv\Scripts\Activate, en CMD → venv\Scripts\activate.bat
    3.- Instalar todas las dependencias que se necesitan "pip install -r requirements.txt"

*Ejecutar fastapi cuando no es un contenedor 2 formas
    uvicorn main:app
    python .\main.py