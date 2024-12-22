from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.tools import Tool

class KeepAIAgent:
    def __init__(self, notes_manager, model_config):
        self.notes_manager = notes_manager
        self.model_config = model_config
        self.agent = self._setup_agent()
    
    def _get_system_message(self):
        return SystemMessage(
            content="""Você é um assistente pessoal focado em ajudar a organizar compromissos e tarefas.
            
            AÇÕES IMEDIATAS OBRIGATÓRIAS:
            1. Se o usuário mencionar "ir na igreja" -> EXECUTE criar_nota IMEDIATAMENTE com todo o contexto disponível
            2. Se o usuário mencionar horário em qualquer mensagem -> USE esse horário na próxima ação
            3. Se o usuário escrever "criar nota" -> EXECUTE criar_nota IMEDIATAMENTE com todo o contexto
            4. Se o usuário mencionar "mudar titulo" -> EXECUTE atualizar_nota IMEDIATAMENTE
            
            CONTEXTO:
            - SEMPRE mantenha o contexto da conversa (horários, locais, detalhes mencionados)
            - USE o contexto ao criar ou atualizar notas
            - NUNCA ignore informações já fornecidas pelo usuário
            
            PROIBIDO:
            - Pedir esclarecimentos antes de criar uma nota
            - Dizer "não sei", "sinto muito" ou falar sobre limitações
            - Perguntar sobre contexto antes de executar um comando
            - Adicionar mensagens de erro ao conteúdo das notas
            - Ignorar horários ou detalhes já mencionados
            
            COMPORTAMENTO CORRETO:
            1. Primeiro EXECUTE a ação solicitada usando todo o contexto disponível
            2. Depois sugira próximos passos
            3. Mantenha o foco no usuário
            
            EXEMPLOS DE RESPOSTAS CORRETAS:
            Usuário: "ir na igreja"
            [Contexto anterior menciona 9h]
            Assistente: [usar criar_nota com horário] "✅ Criei uma nota sobre seu compromisso na igreja às 9h! Quer adicionar mais algum detalhe?"
            
            LEMBRE-SE:
            - SEMPRE use o contexto da conversa
            - Mantenha as notas organizadas com quebras de linha
            - Use linguagem positiva e proativa
            - Foque em ajudar o usuário a organizar seus compromissos
            """
        )
    
    def _get_tools(self):
        return [
            Tool(
                name="criar_nota",
                func=self.notes_manager.criar_nota,
                description="Cria uma nova nota. Use a primeira linha como título (opcional) e o resto como conteúdo."
            ),
            Tool(
                name="ler_nota",
                func=self.notes_manager.ler_nota,
                description="Lê uma nota específica. Argumento: ID da nota (número)."
            ),
            Tool(
                name="atualizar_nota",
                func=self.notes_manager.atualizar_nota,
                description="Atualiza uma nota existente. Primeira linha: ID da nota, depois título (opcional) e conteúdo."
            ),
            Tool(
                name="deletar_nota",
                func=self.notes_manager.deletar_nota,
                description="Deleta uma nota. Argumento: ID da nota (número)."
            ),
            Tool(
                name="listar_notas",
                func=self.notes_manager.listar_notas,
                description="Lista todas as notas salvas."
            )
        ]
    
    def _setup_agent(self):
        # Configurar LLM
        llm = ChatGoogleGenerativeAI(**self.model_config)
        
        # Configurar memória
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            human_prefix="Humano",
            ai_prefix="Assistente"
        )
        
        # Configurar o agente
        agent = initialize_agent(
            self._get_tools(),
            llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=memory,
            system_message=self._get_system_message(),
            handle_parsing_errors=True
        )
        
        # Força uma primeira interação em português
        agent.run("Por favor, responda em português do Brasil: Olá!")
        
        return agent
    
    def run(self, message: str):
        """Executa uma mensagem no agente"""
        return self.agent.run(message) 