CLONAR Y EJECUTAR EL PROYECTO 

*Ejecutar fastapi y un contenedor MySql con docker compose
    1.- Como primer paso se debe clonar el repositorio del proyecto con "git clone https://github.com/Leonardo-Negrete/FastApiProject.git" que es de la rama master.(Se debe tener git instalado)

    2.- DENTRO DEL PROYECTO EJECUTA EL SIGUIENTE COMANDO PARA Compilar el docker compose "docker-compose up -d --build", este comando se debe ejecutar 2 veces para evitar un problema que da hydra.(Hay que tener docker abierto)

    3.- Si deseas levantar un docker compose que ya haya sido compilado y no has movido nada en el codigo solo usa "docker-compose up -d"

    4.- Para acceder al swagger hay que colocar la siguiente url "http://localhost:8000/docs" en el buscador.

    4.- EN LOS ARCHIVOS DE CONFIGURACION SE USA LO SIGUIENTE  usuario "user", contraseña "password" y puerto 3307  CON ESTOS DATOS SE DEBE HACER LA CONEXION AL WORKBRENCH para poder visualiar a la bd de usuarios y asi probar que realmente funcionan las rutas.

*Detener docker compose fastapi
    1.-docker-compose stop

*Para eliminar todo (contenedores, network y volumen):
    1.-docker-compose down -v

-------------------------------------------------------------------------------------------------------------------------------------------------------------
OAUTH2.0
Antes de probar los enpoints se debe crear un token para que se permita el acceso ya que de lo contrario va a marcar un error de autorizacion.

1.- Primer paso es en postman crear un POST con la siguiente URL --> http://localhost:4445/clients 
en ese post en body se debe pasar el siguiente json --> 
PARA ESCRIBIR SOLAMENTE!!
{
    "client_id":"josue_3",
    "client_secret":"1234-secret",
    "grant_types":["client_credentials"],
    "response_types":["token"],
    "scope":"write",
    "token_endpoint_auth_method":"client_secret_basic",
    "access_token_strategy":"jwt"
} 

PARA LEER SOLAMENTE!!
{
    "client_id":"josue_2",
    "client_secret":"1234-secret",
    "grant_types":["client_credentials"],
    "response_types":["token"],
    "scope":"read",
    "token_endpoint_auth_method":"client_secret_basic",
    "access_token_strategy":"jwt"
} 

PARA LEER Y ESCRIBIR ,ESTE VA A PODER HACERLO TODO.
{
    "client_id":"josue_1",
    "client_secret":"1234-secret",
    "grant_types":["client_credentials"],
    "response_types":["token"],
    "scope":"write read",
    "token_endpoint_auth_method":"client_secret_basic",
    "access_token_strategy":"jwt"
} 


2.- Ese primer paso fue para crear usuarios a los cuales se les pueden generar token dependiendo sus atributos , ahora vamos a crear tokens se debe abrir un request de postman y en el apartado de auth se debe selecionar oauth2.0 en auth type , se va a abrir una ventana alado y nos vamos a bajar a Configure New Token ahi vamos a poner lo siguiente 

Token name -->Pr_hydra_1
Grant type -->Client Credentials
Access token Url -->http://localhost:4444/oauth2/token
Client Id -->josue_3
Client Secret-->1234-secret
Scope -->write
Client Authentication -->Send as Basic Auth header

Nota:Esto es para generar un token de solo escritura por lo que se debe crear uno para cada client id que creamos y eso se hace cambiando solo el client id, token name y scope por lo que pusimos al momento de crearlos.

--------------------------------------------------------------------------------------------------------------------------------------------------------------
Probar La Api

Ya que tenemos nuestros 3 tokens se pueden probar ya sea en postman o en swagger , en postman solamente antes de ejecutar los url con sus verbos en la parte de auth se selecciona el token para ese tipo de verbo(read o write) ,si se desea probar en swagger en postman se copea el token que aparece abajo de su nombre al seleccionarlo y ese lo vas a pegar en el el candado que sale en swagger alado de los enpoints y listo se da click en logout.


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
    debe de responder 201 si se creo el usuario sino, 409 (si existe un usuario con el email duplicado)

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


*Como probar en swagger 
Es mas facil probarlo ya que solamente se selecciona el recuadro del enpoint y se da click en try it out y se rellena el campo que se pide y se da click en execute y deben salir los mismos codigos que se mencionan en la parte de probarlo con postman.