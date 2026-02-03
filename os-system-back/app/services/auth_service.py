from app.core.security import verificar_senha, criar_token_acesso, gerar_hash_senha
from fastapi import HTTPException, status


class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    async def registrar_usuario(self, user_data):
        existente = await self.user_repository.find_by_email(user_data.email)
        if existente:
            raise HTTPException(status_code=400, detail="E-mail já cadastrado")

        novo_usuario = {
            "email": user_data.email,
            "senha_hash": gerar_hash_senha(user_data.password),
            "nome": user_data.name,
            "ativo": True
        }

        return await self.user_repository.create(novo_usuario)

    async def autenticar_usuario(self, email, senha):
        user = await self.user_repository.find_by_email(email)

        if not user or not verificar_senha(senha, user["senha_hash"]):
            raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

        token = criar_token_acesso(dados={"sub": user["email"]})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_email": user["email"],
            "user_name": user.get("nome", "Usuário")  # <-- Adicionamos o nome aqui
        }