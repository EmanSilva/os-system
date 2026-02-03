from datetime import datetime


class OSService:
    def __init__(self, repository):
        self.repository = repository

    async def registrar_manutencao(self, os_data, user_email: str):
        os_dict = os_data.model_dump()
        os_dict["usuario_email"] = user_email
        os_dict["data_criacao"] = datetime.utcnow()

        return await self.repository.create(os_dict)

    async def listar_ordens(self, email: str):
        ordens = await self.repository.list_by_user(email)
        for o in ordens:
            o["id"] = str(o["_id"])
            del o["_id"]
        return ordens

    async def atualizar_os(self, os_id: str, os_data: dict, user_email: str):
        os_existente = await self.repository.get_by_id(os_id)
        if not os_existente or os_existente["usuario_email"] != user_email:
            return False

        if "_id" in os_data: del os_data["_id"]

        os_data["usuario_email"] = os_existente["usuario_email"]
        os_data["data_criacao"] = os_existente["data_criacao"]
        os_data["data_atualizacao"] = datetime.now()

        await self.repository.update(os_id, os_data)
        return True

    async def excluir_os(self, os_id: str, user_email: str):
        os_existente = await self.repository.get_by_id(os_id)
        if not os_existente or os_existente["usuario_email"] != user_email:
            return False
        await self.repository.delete(os_id)
        return True