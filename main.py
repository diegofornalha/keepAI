from server.config.settings import PROJECT_NAME, MODEL_CONFIG, get_supabase_client
from server.modules.notes_manager import NotesManager
from server.modules.agent import KeepAIAgent

def main():
    """Inicializa e retorna o agente KeepAI"""
    print(f"\nInicializando {PROJECT_NAME}...")
    
    # Inicializa o cliente Supabase
    supabase = get_supabase_client()
    
    # Inicializa o gerenciador de notas
    notes_manager = NotesManager(supabase)
    
    # Inicializa o agente
    agent = KeepAIAgent(notes_manager, MODEL_CONFIG)
    
    print(f"\n{PROJECT_NAME} está pronto para uso!")
    return agent

if __name__ == "__main__":
    main() 