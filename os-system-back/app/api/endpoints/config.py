from fastapi import APIRouter, Depends
from app.core.database import get_collection
from app.core.security import obter_usuario_logado

router = APIRouter()

@router.get("/checklist")
async def obter_checklist_padrao(usuario_email: str = Depends(obter_usuario_logado)):
    collection = get_collection("checklist_config")
    cursor = collection.find({}, {"_id": 0})
    itens = await cursor.to_list(length=100)

    if not itens:
        return [{"tarefa": "Verificação Geral", "concluido": False}]

    return itens