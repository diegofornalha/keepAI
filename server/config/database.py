import os
from supabase import create_client, Client
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

# Cliente do Supabase
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

__all__ = ["supabase_client"]
