import bcrypt
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings


ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def gerar_hash_senha(senha: str) -> str:
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hash_bytes.decode('utf-8')

def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            senha_pura.encode('utf-8'),
            senha_hash.encode('utf-8')
        )
    except Exception:
        return False

def criar_token_acesso(dados: dict):
    para_codificar = dados.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    para_codificar.update({"exp": expira})
    return jwt.encode(para_codificar, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def obter_usuario_logado(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Poderia não validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception