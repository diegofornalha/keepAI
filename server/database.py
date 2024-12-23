import os
from supabase import create_client, Client

# Configuração do Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Inicializar Supabase
if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL e SUPABASE_KEY devem ser definidos no arquivo .env")

try:
    # Inicializar cliente Supabase
    supabase: Client = create_client(supabase_url, supabase_key)
    print("Conexão com Supabase estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar com Supabase: {str(e)}")
    raise
