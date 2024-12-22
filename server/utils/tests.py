import unittest
import time
import os
import logging
from logging.handlers import RotatingFileHandler
from .cache import Cache, cached
from .logger import setup_logger

class TestCache(unittest.TestCase):
    def setUp(self):
        self.cache = Cache()

    def test_cache_set_get(self):
        """Testa operações básicas de set/get do cache"""
        self.cache.set('test_key', 'test_value', ttl_minutes=1)
        self.assertEqual(self.cache.get('test_key'), 'test_value')

    def test_cache_expiration(self):
        """Testa se o cache expira corretamente"""
        self.cache.set('test_key', 'test_value', ttl_minutes=0.016)  # 1 segundo
        self.assertEqual(self.cache.get('test_key'), 'test_value')
        time.sleep(1.1)  # Espera o TTL expirar
        self.assertIsNone(self.cache.get('test_key'))

    def test_cache_stats(self):
        """Testa se as estatísticas do cache são atualizadas corretamente"""
        self.cache.set('test_key', 'test_value')
        self.cache.get('test_key')  # Hit
        self.cache.get('nonexistent_key')  # Miss
        
        stats = self.cache.get_stats()
        self.assertEqual(stats['hits'], 1)
        self.assertEqual(stats['misses'], 1)
        self.assertEqual(stats['sets'], 1)

    def test_cache_decorator(self):
        """Testa o decorator de cache"""
        call_count = 0
        
        @cached(ttl_minutes=1)
        def test_function():
            nonlocal call_count
            call_count += 1
            return 'test_result'
        
        # Primeira chamada - deve executar a função
        result1 = test_function()
        self.assertEqual(result1, 'test_result')
        self.assertEqual(call_count, 1)
        
        # Segunda chamada - deve usar o cache
        result2 = test_function()
        self.assertEqual(result2, 'test_result')
        self.assertEqual(call_count, 1)  # Não deve ter incrementado

class TestLogger(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuração inicial para todos os testes do logger"""
        cls.log_dir = 'logs'
        cls.log_file = os.path.join(cls.log_dir, 'test_keepai.log')
        
        # Cria o diretório de logs se não existir
        if not os.path.exists(cls.log_dir):
            os.makedirs(cls.log_dir)
            
        # Remove arquivos de log antigos
        for f in os.listdir(cls.log_dir):
            if f.startswith('test_keepai.log'):
                os.remove(os.path.join(cls.log_dir, f))

    def setUp(self):
        """Configuração para cada teste"""
        # Configura o logger de teste
        self.logger = logging.getLogger('test_keepai')
        self.logger.setLevel(logging.DEBUG)
        
        # Limpa handlers existentes
        self.logger.handlers = []
        
        # Adiciona handler de arquivo com rotação
        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=1024,  # 1KB para testes
            backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            '%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(file_handler)

    def test_log_levels(self):
        """Testa diferentes níveis de log"""
        test_message = 'Test log message'
        
        self.logger.debug(test_message)
        self.logger.info(test_message)
        self.logger.warning(test_message)
        self.logger.error(test_message)
        
        with open(self.log_file, 'r') as f:
            log_content = f.read()
            
        # Verifica se as mensagens foram registradas
        self.assertIn('INFO', log_content)
        self.assertIn('WARNING', log_content)
        self.assertIn('ERROR', log_content)
        self.assertIn(test_message, log_content)

    def test_log_rotation(self):
        """Testa a rotação de arquivos de log"""
        # Gera um arquivo de log grande (maior que 1KB)
        large_message = 'x' * 200  # 200 bytes por mensagem
        for _ in range(10):  # 2KB total
            self.logger.info(large_message)
            
        # Verifica se foram criados arquivos de backup
        backup_exists = any(
            os.path.exists(f'{self.log_file}.{i}')
            for i in range(1, 6)
        )
        self.assertTrue(backup_exists)

    def test_log_formatting(self):
        """Testa o formato das mensagens de log"""
        test_message = 'Test format message'
        self.logger.info(test_message)
        
        with open(self.log_file, 'r') as f:
            log_line = f.readline()
            
        # Verifica o formato da mensagem
        self.assertRegex(log_line, r'\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]')  # Data/hora
        self.assertIn('INFO', log_line)  # Nível
        self.assertIn('test_keepai', log_line)  # Nome do logger
        self.assertIn(test_message, log_line)  # Mensagem

if __name__ == '__main__':
    unittest.main() 