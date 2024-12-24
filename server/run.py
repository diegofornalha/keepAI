"""Ponto de entrada da aplicação Flask."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import (
    APP_NAME,
    APP_VERSION,
    CORS_ORIGINS,
    CORS_METHODS,
    CORS_HEADERS,
)
from routes.api import api_router

# Cria a aplicação FastAPI
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="API do KeepAI - Seu assistente pessoal inteligente",
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
    allow_credentials=True,
)

# Inclui as rotas da API
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
