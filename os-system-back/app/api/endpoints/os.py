from fastapi import APIRouter, Depends, HTTPException
from app.schemas.os_schema import OSCreate
from app.services.os_service import OSService
from app.repositories.os_repository import OSRepository
from app.core.database import get_collection
from app.core.security import obter_usuario_logado

router = APIRouter()

async def get_os_service():
    collection = get_collection("ordens_servico")
    repository = OSRepository(collection)
    return OSService(repository)

@router.post("/", status_code=201)
async def criar_os(
    os_data: OSCreate,
    user_email: str = Depends(obter_usuario_logado),
    os_service: OSService = Depends(get_os_service)
):
    os_id = await os_service.registrar_manutencao(os_data, user_email)
    return {"message": "Ordem de serviço registrada", "id": os_id}

@router.get("/")
async def listar_os(
    user_email: str = Depends(obter_usuario_logado),
    os_service: OSService = Depends(get_os_service)
):
    return await os_service.listar_ordens(user_email)

@router.put("/{os_id}")
async def atualizar_os(
    os_id: str,
    os_data: OSCreate,
    user_email: str = Depends(obter_usuario_logado),
    os_service: OSService = Depends(get_os_service)
):
    sucesso = await os_service.atualizar_os(os_id, os_data.model_dump(), user_email)
    if not sucesso:
        raise HTTPException(404, "OS não encontrada ou acesso negado")
    return {"message": "Atualizada com sucesso"}

@router.delete("/{os_id}")
async def excluir_os(
    os_id: str,
    user_email: str = Depends(obter_usuario_logado),
    os_service: OSService = Depends(get_os_service)
):
    sucesso = await os_service.excluir_os(os_id, user_email)
    if not sucesso:
        raise HTTPException(404, "OS não encontrada ou acesso negado")
    return {"message": "Excluída com sucesso"}