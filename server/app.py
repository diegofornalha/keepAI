from flask import Flask, render_template, jsonify, request
from .routes.notes import notes_bp
from .config.integrations import IntegrationsConfig
from .langchain_components.chat import ChatManager
import logging
import traceback

def create_app():
    app = Flask(__name__)
    
    # Configuração de logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Inicializa o gerenciador de chat
    try:
        chat_manager = ChatManager()
        logger.info("ChatManager inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar ChatManager: {str(e)}")
        logger.error(traceback.format_exc())
        chat_manager = None
    
    # Registra blueprints
    app.register_blueprint(notes_bp)
    
    @app.route('/')
    def index():
        return render_template('index.html')
        
    @app.route('/notes')
    def notes():
        return render_template('notes.html')
        
    @app.route('/calendar')
    def calendar():
        return render_template('calendar.html')
        
    @app.route('/tasks')
    def tasks():
        return render_template('tasks.html')
        
    @app.route('/api/chat', methods=['POST'])
    async def chat():
        try:
            if chat_manager is None:
                logger.error("ChatManager não está disponível")
                return jsonify({
                    'error': 'O serviço de chat está temporariamente indisponível. Por favor, tente novamente em alguns minutos.'
                }), 503
            
            data = request.get_json()
            if not data:
                logger.warning("Requisição sem dados")
                return jsonify({
                    'error': 'Por favor, forneça uma mensagem para o chat.'
                }), 400
            
            message = data.get('message', '').strip()
            if not message:
                logger.warning("Mensagem vazia recebida")
                return jsonify({
                    'error': 'A mensagem não pode estar vazia.'
                }), 400
            
            logger.info(f"Processando mensagem: {message[:50]}...")
            
            # Processa a mensagem usando o ChatManager
            response = await chat_manager.process_message(message)
            
            if not response:
                logger.error("Resposta vazia do ChatManager")
                return jsonify({
                    'error': 'Não foi possível gerar uma resposta. Por favor, tente novamente.'
                }), 500
            
            logger.info(f"Resposta gerada com sucesso: {response[:50]}...")
            return jsonify({
                'response': response
            })
            
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'error': 'Ops! Tivemos um problema ao processar sua mensagem. Por favor, tente novamente.'
            }), 500
    
    return app 