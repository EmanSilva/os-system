from fastapi import APIRouter
from app.api.endpoints import auth, os, config

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
api_router.include_router(os.router, prefix="/ordens-servico", tags=["Ordens de Serviço"])
api_router.include_router(config.router, prefix="/config", tags=["Configurações"])