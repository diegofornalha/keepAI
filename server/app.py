from flask import Flask, request, jsonify, render_template, send_from_directory, session
import os
from main import main
from server.config.settings import get_supabase_client
from server.config.security import security_check, sanitize_input, generate_csrf_token, SecurityConfig
import secrets
from datetime import datetime

# Obtém o caminho absoluto do diretório atual
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(os.path.dirname(current_dir), 'server', 'templates')
static_dir = os.path.join(os.path.dirname(current_dir), 'server', 'static')

app = Flask(__name__, 
    template_folder=template_dir,
    static_folder=static_dir
)

# Configurações de segurança
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', secrets.token_hex(32))
app.config['MAX_CONTENT_LENGTH'] = SecurityConfig.MAX_CONTENT_LENGTH
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutos
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Inicializa o agente
agent = main()

@app.before_request
def before_request():
    # For��a HTTPS em produção
    if not request.is_secure and app.env == 'production':
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
    
    # Gera CSRF token se não existir
    if 'csrf_token' not in session:
        session['csrf_token'] = generate_csrf_token()

@app.after_request
def after_request(response):
    # Adiciona headers de segurança
    for header, value in SecurityConfig.SECURE_HEADERS.items():
        response.headers[header] = value
    return response

@app.route('/')
def home():
    return render_template('index.html', csrf_token=session.get('csrf_token'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/api/chat', methods=['POST'])
@security_check
def chat():
    # Verifica CSRF token
    token = request.headers.get('X-CSRF-Token')
    if not token or token != session.get('csrf_token'):
        return jsonify({'error': 'Token CSRF inválido'}), 403
    
    # Sanitiza input
    message = sanitize_input(request.json.get('message', ''))
    
    try:
        response = agent.run(message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes')
@security_check
def get_notes():
    try:
        # Obtém o cliente Supabase usando a função do settings
        supabase = get_supabase_client()
        
        # Busca todas as notas ordenadas por data
        result = supabase.table('notes').select('*').order('data', desc=True).execute()
        
        # Sanitiza os dados antes de retornar
        sanitized_data = []
        for note in result.data:
            sanitized_note = {
                'id': note['id'],
                'title': sanitize_input(note['title']),
                'content': sanitize_input(note['content']),
                'data': note['data']
            }
            sanitized_data.append(sanitized_note)
        
        return jsonify({
            'response': sanitized_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes', methods=['POST'])
@security_check
def create_note():
    try:
        # Verifica CSRF token
        token = request.headers.get('X-CSRF-Token')
        if not token or token != session.get('csrf_token'):
            return jsonify({'error': 'Token CSRF inválido'}), 403
        
        # Sanitiza input
        titulo = sanitize_input(request.json.get('titulo', ''))
        conteudo = sanitize_input(request.json.get('conteudo', ''))
        
        if not titulo or not conteudo:
            return jsonify({'error': 'Título e conteúdo são obrigatórios'}), 400
        
        # Obtém o cliente Supabase
        supabase = get_supabase_client()
        
        # Insere a nova nota
        result = supabase.table('notes').insert({
            'titulo': titulo,
            'conteudo': conteudo,
            'data': datetime.now().isoformat()
        }).execute()
        
        return jsonify({'response': result.data[0]}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
@security_check
def update_note(note_id):
    try:
        # Verifica CSRF token
        token = request.headers.get('X-CSRF-Token')
        if not token or token != session.get('csrf_token'):
            return jsonify({'error': 'Token CSRF inválido'}), 403
        
        # Sanitiza input
        titulo = sanitize_input(request.json.get('titulo', ''))
        conteudo = sanitize_input(request.json.get('conteudo', ''))
        
        if not titulo or not conteudo:
            return jsonify({'error': 'Título e conteúdo são obrigatórios'}), 400
        
        # Obtém o cliente Supabase
        supabase = get_supabase_client()
        
        # Atualiza a nota
        result = supabase.table('notes').update({
            'titulo': titulo,
            'conteudo': conteudo,
            'updated_at': datetime.now().isoformat()
        }).eq('id', note_id).execute()
        
        if not result.data:
            return jsonify({'error': 'Nota não encontrada'}), 404
        
        return jsonify({'response': result.data[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
@security_check
def delete_note(note_id):
    try:
        # Verifica CSRF token
        token = request.headers.get('X-CSRF-Token')
        if not token or token != session.get('csrf_token'):
            return jsonify({'error': 'Token CSRF inválido'}), 403
        
        # Obtém o cliente Supabase
        supabase = get_supabase_client()
        
        # Deleta a nota
        result = supabase.table('notes').delete().eq('id', note_id).execute()
        
        if not result.data:
            return jsonify({'error': 'Nota não encontrada'}), 404
        
        return jsonify({'response': 'Nota deletada com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Tratamento de erros
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Recurso não encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'Payload muito grande'}), 413

if __name__ == '__main__':
    # Obtém a porta do ambiente ou usa 3000 como padrão
    port = int(os.environ.get('PORT', 3000))
    # Executa o app Flask
    app.run(host='0.0.0.0', port=port, debug=True) 