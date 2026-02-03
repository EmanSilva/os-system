import asyncio
from app.core.database import get_collection
from app.core.security import gerar_hash_senha


async def carregar_dados_iniciais():
    print("🚀 Verificando dados iniciais do sistema...")

    checklist_coll = get_collection("checklist_config")
    total_checklist = await checklist_coll.count_documents({})

    if total_checklist == 0:
        print("📝 Populando checklist padrão...")
        itens_padrao = [
            {"tarefa": "Verificar cabos de rede", "concluido": False},
            {"tarefa": "Limpar poeira dos coolers", "concluido": False},
            {"tarefa": "Testar fontes de energia", "concluido": False},
            {"tarefa": "Verificar temperatura", "concluido": False}
        ]
        await checklist_coll.insert_many(itens_padrao)

    user_coll = get_collection("usuarios")
    admin_existente = await user_coll.find_one({"email": "admin@teste.com"})

    if not admin_existente:
        print("👤 Criando usuário admin padrão...")
        admin_user = {
            "email": "admin@teste.com",
            "senha_hash": gerar_hash_senha("123"),
            "nome": "Administrador",
            "ativo": True
        }
        await user_coll.insert_one(admin_user)

    print("✅ Sistema pronto para uso.")