from supabase import create_client, Client
import os

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError(
        "SUPABASE_URL e SUPABASE_KEY devem ser definidos nas variáveis de ambiente"
    )

supabase: Client = create_client(supabase_url=supabase_url, supabase_key=supabase_key)
