from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import requests

# Endpoint de JWKS de Hydra
JWKS_URL = "http://hydra-public:4444/.well-known/jwks.json"

# Obtener JWKS de Hydra
jwks = requests.get(JWKS_URL).json()

#  Clase personalizada para devolver 401 en lugar de 403 cuando no se envía el token
class HTTPBearer401(HTTPBearer):
    def __init__(self, **kwargs):
        # auto_error=False evita que super().__call__ lance 403 de inmediato
        super().__init__(auto_error=False, **kwargs)
    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)
        if not credentials or credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return credentials

# Usamos nuestra clase personalizada en lugar de la original
security = HTTPBearer401()

#  Extraer clave pública desde el JWKS usando el 'kid'
def get_public_key(kid: str):
    for key in jwks["keys"]:
        if key["kid"] == kid:
            return key
    return None

#  Verificar el token JWT
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # Leer encabezado del token para obtener el 'kid'
        headers = jwt.get_unverified_header(token)
        kid = headers.get("kid")
        if not kid:
            raise HTTPException(status_code=401, detail="Token missing 'kid' in header")

        # Buscar la clave pública en el JWKS
        key = get_public_key(kid)
        if not key:
            raise HTTPException(status_code=401, detail="Public key not found for given 'kid'")

        # Validar el token
        payload = jwt.decode(
            token,
            key=key,
            algorithms=[headers["alg"]],
            options={"verify_aud": False}  # Cambiar a True si usas 'aud' en el token
        )

        # Verificar si el scope está presente
        scopes = payload.get("scp", [])  # Cambié "scope" por "scp" aquí
        if isinstance(scopes, str):
            scopes = scopes.split()  # Convierte a lista si es una cadena

        return payload  # Devuelve el payload

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


#  Manejamos el Scope dentro del Token
def require_scope(required_scope: str):
    def scope_dependency(token_data: dict = Depends(verify_token)):
        # Obtener los scopes del token
        scopes = token_data.get("scp", [])  # Usamos "scp" en lugar de "scope" según el payload que compartiste

        # Asegurar que sea lista (si es string, convertirlo a lista)
        if isinstance(scopes, str):
            scopes = scopes.split()  # Convertimos de string a lista
        elif not isinstance(scopes, list):
            scopes = []

        # Verificamos si el scope requerido está presente
        if required_scope not in scopes:
            raise HTTPException(
                status_code=403,  # 403 cuando el scope no está presente
                detail=f"Access denied: missing required scope '{required_scope}'"
            )

        return token_data  # Devolvemos los claims si se necesita

    return scope_dependency