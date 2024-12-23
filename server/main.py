from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pathlib import Path

# Carregar variáveis de ambiente da raiz do projeto
env_path = Path(__file__).parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="KeepAI API")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "KeepAI API está rodando!"}


@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "supabase_url": os.getenv("SUPABASE_URL") is not None,
        "database_url": os.getenv("DATABASE_URL") is not None,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
