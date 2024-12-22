from server.config.settings import get_supabase_client

def test_connection():
    print("Testando conexão com Supabase...")
    try:
        # Obtém o cliente Supabase
        supabase = get_supabase_client()
        
        # Tenta listar as notas
        result = supabase.table('notes').select('*').order('data', desc=True).execute()
        
        print("\nNotas encontradas:")
        for nota in result.data:
            print(f"\nID: {nota['id']}")
            print(f"Título: {nota['titulo']}")
            print(f"Conteúdo: {nota['conteudo']}")
            print(f"Data: {nota['data']}")
            print("-" * 50)
            
        print(f"\nTotal de notas: {len(result.data)}")
        
    except Exception as e:
        print(f"Erro ao conectar: {str(e)}")

if __name__ == "__main__":
    test_connection() 