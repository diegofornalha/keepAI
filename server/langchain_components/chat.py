from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
import os
import logging
import asyncio

class ChatManager:
    def __init__(self):
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")
            
        self.llm = ChatGoogleGenerativeAI(
            temperature=0.7,
            model="gemini-pro",
            google_api_key=google_api_key,
            convert_system_message_to_human=True,
            max_output_tokens=2048,
            top_p=0.95,
            top_k=40,
            safety_settings={
                "HARASSMENT": "block_none",
                "HATE_SPEECH": "block_none",
                "SEXUALLY_EXPLICIT": "block_none",
                "DANGEROUS_CONTENT": "block_none"
            }
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True,
            output_key="output"
        )
        
        self.prompt = PromptTemplate(
            input_variables=["history", "input"],
            template="""Você é um assistente amigável e prestativo chamado KeepAI. 
Você SEMPRE responde em português do Brasil de forma natural e conversacional.
Você é direto e objetivo em suas respostas, mas mantém um tom amigável.

Algumas regras importantes:
1. Mantenha suas respostas curtas e diretas
2. Use linguagem informal mas profissional
3. Seja empático e amigável
4. Evite respostas muito longas ou técnicas demais
5. Se não souber algo, diga honestamente
6. Mantenha o contexto da conversa
7. Sempre sugira criar notas quando identificar tarefas ou compromissos

Histórico da conversa:
{history}

Humano: {input}
Assistente: """
        )
        
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True
        )
    
    async def process_message(self, message: str) -> str:
        """Processa uma mensagem do usuário e retorna a resposta"""
        try:
            # Garante que estamos usando o loop de eventos correto
            loop = asyncio.get_event_loop()
            
            # Adiciona tratamento de erros mais robusto
            try:
                response = await loop.run_in_executor(
                    None, 
                    lambda: self.conversation.predict(input=message)
                )
            except Exception as e:
                logging.error(f"Erro na chamada ao Gemini: {str(e)}")
                return "Desculpe, tive um problema ao processar sua mensagem. Pode tentar novamente?"
            
            # Validações adicionais da resposta
            if not response or response.isspace():
                return "Opa! Não consegui processar sua mensagem. Pode tentar dizer de outra forma?"
                
            # Limpeza e formatação da resposta
            response = response.replace("Assistente:", "").strip()
            response = response.replace("Deixe-me ajudar você com isso.", "").strip()
            
            return response
            
        except Exception as e:
            logging.error(f"Erro ao processar mensagem: {str(e)}")
            return "Desculpe, tive um problema técnico aqui. Pode tentar novamente?" 