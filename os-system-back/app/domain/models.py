from datetime import datetime
from typing import List, Optional

class ChecklistItem:
    def __init__(self, tarefa: str, concluido: bool = False):
        self.tarefa = tarefa
        self.concluido = concluido

class OrdemServico:
    def __init__(self, descricao: str, checklist: List[ChecklistItem],
                 usuario_email: str, foto_url: Optional[str] = None):
        self.descricao = descricao
        self.checklist = checklist
        self.usuario_email = usuario_email
        self.foto_url = foto_url
        self.data_criacao = datetime.now()