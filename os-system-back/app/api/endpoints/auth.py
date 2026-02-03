from fastapi import APIRouter, Depends, HTTPException
from app.schemas.auth_schema import LoginRequest, UserCreate
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.core.database import get_collection

router = APIRouter()

async def get_auth_service():
    collection = get_collection("usuarios")
    repository = UserRepository(collection)
    return AuthService(repository)

@router.post("/register", status_code=201)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    user_id = await auth_service.registrar_usuario(user_data)
    return {"message": "Usuário criado com sucesso", "id": user_id}

@router.post("/login")
async def login(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.autenticar_usuario(login_data.email, login_data.senha)