from pydantic import BaseModel, field_validator
from typing import List
from datetime import datetime


class ChecklistItemSchema(BaseModel):
    tarefa: str
    concluido: bool = False


class OSCreate(BaseModel):
    descricao: str
    checklist: List[ChecklistItemSchema]
    foto_base64: str

    @field_validator('checklist')
    @classmethod
    def at_least_one_checked(cls, v: List[ChecklistItemSchema]) -> List[ChecklistItemSchema]:
        if not any(item.concluido for item in v):
            raise ValueError('Pelo menos um item do checklist deve estar concluído')
        return v

    @field_validator('foto_base64')
    @classmethod
    def foto_not_empty(cls, v: str) -> str:
        if not v or len(v) < 100:
            raise ValueError('A foto de comprovação é obrigatória')
        return v

class OSResponse(OSCreate):
    id: str
    usuario_email: str
    data_criacao: datetime