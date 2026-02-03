from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.router import api_router
from app.core.bootstrap import carregar_dados_iniciais

@asynccontextmanager
async def lifespan(app: FastAPI):
    await carregar_dados_iniciais()
    yield

app = FastAPI(title="OS System API", lifespan=lifespan)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/", tags=["Health"])
async def health():
    return {"status": "online"}