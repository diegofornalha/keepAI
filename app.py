from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import socket
import signal
import sys
import psutil
import time
from datetime import datetime
from main import main
from server.config.settings import get_supabase_client
from server.utils.logger import setup_logger
from server.utils.cache import cached, cache
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Configuração do logger
logger = setup_logger()

# Métricas da aplicação
app_metrics = {
    'start_time': datetime.now().isoformat(),
    'requests': 0,
    'errors': 0,
    'response_times': [],
    'memory_samples': []
}

# Métricas do Prometheus
http_requests_total = Counter('http_requests_total', 'Total de requisições HTTP', ['method', 'endpoint', 'status'])
http_request_duration_seconds = Histogram('http_request_duration_seconds', 'Duração das requisições HTTP')
cpu_usage = Gauge('cpu_usage', 'Uso de CPU em porcentagem')
memory_usage = Gauge('memory_usage', 'Uso de memória em porcentagem')
cache_hits_total = Counter('cache_hits_total', 'Total de acertos no cache')
cache_misses_total = Counter('cache_misses_total', 'Total de erros no cache')

def collect_metrics():
    """Coleta métricas do sistema"""
    try:
        process = psutil.Process()
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': process.cpu_percent(),
            'memory_percent': process.memory_percent(),
            'memory_rss': process.memory_info().rss / 1024 / 1024,  # MB
            'memory_vms': process.memory_info().vms / 1024 / 1024,  # MB
            'threads': process.num_threads(),
            'open_files': len(process.open_files()),
            'connections': len(process.connections())
        }
        
        app_metrics['memory_samples'].append(metrics)
        # Mantém apenas as últimas 100 amostras
        if len(app_metrics['memory_samples']) > 100:
            app_metrics['memory_samples'].pop(0)
            
        return metrics
    except Exception as e:
        logger.error(f'Erro ao coletar métricas: {str(e)}')
        return None

def is_port_in_use(port):
    """Verifica se uma porta está em uso"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return False
        except socket.error:
            return True

def find_available_port(start_port, max_attempts=10):
    """Encontra uma porta disponível"""
    for port in range(start_port, start_port + max_attempts):
        if not is_port_in_use(port):
            return port
    raise RuntimeError(f'Não foi possível encontrar uma porta disponível entre {start_port} e {start_port + max_attempts - 1}')

def signal_handler(sig, frame):
    """Manipula o sinal de interrupção"""
    logger.info('Encerrando servidor...')
    # Coleta métricas finais
    final_metrics = collect_metrics()
    if final_metrics:
        logger.info('Métricas finais:', extra=final_metrics)
    # Limpa o cache antes de encerrar
    cache.clear()
    logger.info('Cache limpo')
    sys.exit(0)

app = Flask(__name__, 
    template_folder='server/templates',
    static_folder='server/static'
)

# Inicializa o agente
logger.info('Inicializando KeepAI...')
agent = main()
logger.info('Agente inicializado com sucesso')

@app.before_request
def before_request():
    """Executa antes de cada requisição"""
    request.start_time = time.time()
    app_metrics['requests'] += 1

@app.after_request
def after_request(response):
    """Executa após cada requisição"""
    # Calcula tempo de resposta
    if hasattr(request, 'start_time'):
        elapsed = time.time() - request.start_time
        app_metrics['response_times'].append(elapsed)
        # Mantém apenas os últimos 1000 tempos
        if len(app_metrics['response_times']) > 1000:
            app_metrics['response_times'].pop(0)
    
    # Atualiza contagem de erros
    if response.status_code >= 400:
        app_metrics['errors'] += 1
    
    # Registra a duração da requisição
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        http_request_duration_seconds.observe(duration)

    # Registra a requisição
    http_requests_total.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        status=response.status_code
    ).inc()
    
    return response

@app.route('/')
@cached(ttl_minutes=5)  # Cache da página inicial por 5 minutos
def home():
    logger.info('Página inicial acessada', extra={
        'ip': request.remote_addr,
        'user_agent': request.user_agent.string
    })
    return render_template('index.html')

@app.route('/favicon.svg')
def favicon():
    logger.debug('Favicon solicitado')
    return send_from_directory(app.static_folder, 'favicon.svg', mimetype='image/svg+xml')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    logger.info('Nova mensagem recebida', extra={
        'user_input': user_message,
        'ip': request.remote_addr,
        'user_agent': request.user_agent.string
    })
    try:
        response = agent.run(user_message)
        logger.info('Resposta gerada com sucesso', extra={'message_length': len(response)})
        return jsonify({'response': response})
    except Exception as e:
        logger.error('Erro ao processar mensagem', exc_info=True, extra={
            'error': str(e),
            'user_input': user_message
        })
        return jsonify({'error': str(e)}), 500

@app.route('/api/notes')
@cached(ttl_minutes=10)  # Aumentando TTL para 10 minutos
def get_notes():
    try:
        # Obtém o cliente Supabase usando a função do settings
        supabase = get_supabase_client()
        
        # Busca todas as notas ordenadas por data
        logger.info('Buscando notas no Supabase')
        result = supabase.table('notes').select('*').order('data', desc=True).execute()
        
        # Retorna os dados diretamente
        logger.info('Notas recuperadas com sucesso', extra={'count': len(result.data)})
        return jsonify({
            'response': result.data
        })
    except Exception as e:
        logger.error('Erro ao buscar notas', exc_info=True, extra={'error': str(e)})
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/stats')
def cache_stats():
    """Rota para visualizar estatísticas do cache"""
    try:
        stats = cache.get_stats()
        logger.info('Estatísticas do cache recuperadas', extra=stats)
        return jsonify(stats)
    except Exception as e:
        logger.error('Erro ao recuperar estatísticas do cache', exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/metrics')
def app_metrics_endpoint():
    """Rota para visualizar métricas da aplicação"""
    try:
        current_metrics = collect_metrics()
        
        # Calcula estatísticas dos tempos de resposta
        response_times = app_metrics['response_times']
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
        else:
            avg_response_time = 0
            max_response_time = 0
        
        metrics_data = {
            **app_metrics,
            'current': current_metrics,
            'uptime_seconds': (datetime.now() - datetime.fromisoformat(app_metrics['start_time'])).total_seconds(),
            'avg_response_time': avg_response_time,
            'max_response_time': max_response_time,
            'error_rate': (app_metrics['errors'] / app_metrics['requests'] * 100) if app_metrics['requests'] > 0 else 0
        }
        
        return jsonify(metrics_data)
    except Exception as e:
        logger.error('Erro ao recuperar métricas', exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/metrics')
def metrics():
    # Atualiza métricas do sistema
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().percent)
    
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    # Registra o handler para SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Obtém a porta do ambiente ou usa 3000 como padrão
        start_port = int(os.environ.get('PORT', 3000))
        
        # Tenta encontrar uma porta disponível
        port = find_available_port(start_port)
        
        # Coleta métricas iniciais
        initial_metrics = collect_metrics()
        if initial_metrics:
            logger.info('Métricas iniciais:', extra=initial_metrics)
        
        # Executa o app Flask
        logger.info(f'Iniciando servidor na porta {port}')
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        logger.error('Erro ao iniciar servidor', exc_info=True, extra={'error': str(e)})
        sys.exit(1)
