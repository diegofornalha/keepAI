import os
from supabase.client import create_client, AsyncClient
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "As variáveis de ambiente SUPABASE_URL e SUPABASE_KEY devem estar definidas"
    )

# Cliente assíncrono do Supabase
supabase_client: AsyncClient = create_client(SUPABASE_URL, SUPABASE_KEY)

__all__ = ["supabase_client"]
