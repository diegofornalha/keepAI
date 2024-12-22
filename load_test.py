import argparse
import asyncio
import aiohttp
import time
import json
from datetime import datetime
import statistics
import sys
import logging
import psutil
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoadTest:
    def __init__(self, base_url, num_users, duration, scenario='default'):
        self.base_url = base_url
        self.num_users = num_users
        self.duration = duration
        self.scenario = scenario
        self.results = []
        self.errors = []
        self.start_time = None
        self.end_time = None
        self.system_stats = []

    async def collect_system_stats(self):
        """Coleta estatísticas do sistema durante o teste"""
        while True:
            try:
                stats = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu_percent': psutil.cpu_percent(),
                    'memory_percent': psutil.virtual_memory().percent,
                    'memory_used': psutil.virtual_memory().used / (1024 * 1024),  # MB
                }
                self.system_stats.append(stats)
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Erro ao coletar estatísticas do sistema: {str(e)}")

    async def make_request(self, session, endpoint, user_id, method='GET', data=None):
        """Faz uma requisição e registra o tempo"""
        start_time = time.time()
        try:
            if method == 'GET':
                async with session.get(f"{self.base_url}{endpoint}") as response:
                    content = await response.text()
                    end_time = time.time()
                    elapsed = end_time - start_time
            else:  # POST
                async with session.post(f"{self.base_url}{endpoint}", json=data) as response:
                    content = await response.text()
                    end_time = time.time()
                    elapsed = end_time - start_time
                
            self.results.append({
                'user_id': user_id,
                'endpoint': endpoint,
                'method': method,
                'status': response.status,
                'time': elapsed,
                'timestamp': datetime.now().isoformat(),
                'content_length': len(content)
            })
            
            if response.status != 200:
                logger.warning(f"Resposta não-200 para {endpoint}: {response.status}")
                    
        except Exception as e:
            logger.error(f"Erro ao acessar {endpoint}: {str(e)}")
            self.errors.append({
                'user_id': user_id,
                'endpoint': endpoint,
                'method': method,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })

    async def simulate_user(self, user_id):
        """Simula um usuário fazendo requisições"""
        logger.info(f"Iniciando usuário {user_id}")
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            requests_made = 0
            
            while time.time() - start_time < self.duration:
                if self.scenario == 'default':
                    # Cenário padrão
                    await self.make_request(session, '/', user_id)
                    await self.make_request(session, '/api/notes', user_id)
                    await self.make_request(session, '/api/cache/stats', user_id)
                    requests_made += 3
                elif self.scenario == 'heavy_read':
                    # Cenário de leitura intensiva
                    for _ in range(5):
                        await self.make_request(session, '/api/notes', user_id)
                    requests_made += 5
                elif self.scenario == 'mixed':
                    # Cenário misto com leitura e escrita
                    await self.make_request(session, '/api/notes', user_id)
                    await self.make_request(session, '/api/chat', user_id, 'POST', 
                                         {'message': 'Teste de carga'})
                    requests_made += 2
                
                # Pausa dinâmica baseada na carga
                await asyncio.sleep(1)
            
            logger.info(f"Usuário {user_id} completou {requests_made} requisições")

    async def run(self):
        """Executa o teste de carga"""
        self.start_time = datetime.now()
        logger.info(f"Iniciando teste de carga com {self.num_users} usuários por {self.duration} segundos...")
        logger.info(f"Cenário: {self.scenario}")
        
        try:
            # Inicia coleta de estatísticas do sistema
            stats_task = asyncio.create_task(self.collect_system_stats())
            
            # Inicia simulação de usuários
            user_tasks = [self.simulate_user(i) for i in range(self.num_users)]
            await asyncio.gather(*user_tasks)
            
            # Cancela coleta de estatísticas
            stats_task.cancel()
            try:
                await stats_task
            except asyncio.CancelledError:
                pass
            
        except Exception as e:
            logger.error(f"Erro durante o teste: {str(e)}")
        finally:
            self.end_time = datetime.now()

    def print_results(self):
        """Imprime os resultados do teste"""
        if not self.results:
            logger.error("Nenhum resultado para mostrar.")
            return

        print("\n=== Resultados do Teste de Carga ===")
        print(f"Cenário: {self.scenario}")
        print(f"Duração do teste: {(self.end_time - self.start_time).total_seconds():.2f} segundos")
        print(f"Número de usuários: {self.num_users}")
        
        # Agrupa resultados por endpoint e método
        by_endpoint = {}
        for r in self.results:
            key = f"{r['method']} {r['endpoint']}"
            if key not in by_endpoint:
                by_endpoint[key] = []
            by_endpoint[key].append(r['time'])

        # Análise por endpoint
        print("\nEstatísticas por Endpoint:")
        for endpoint, times in by_endpoint.items():
            success_rate = len([r for r in self.results 
                              if f"{r['method']} {r['endpoint']}" == endpoint 
                              and r['status'] == 200]) / len(times) * 100
            
            print(f"\n{endpoint}:")
            print(f"  Requisições: {len(times)}")
            print(f"  Taxa de sucesso: {success_rate:.1f}%")
            print(f"  Tempo médio: {statistics.mean(times):.3f}s")
            print(f"  Tempo mínimo: {min(times):.3f}s")
            print(f"  Tempo máximo: {max(times):.3f}s")
            print(f"  Desvio padrão: {statistics.stdev(times):.3f}s")
            print(f"  Percentil 90: {sorted(times)[int(len(times)*0.9)]:.3f}s")
            print(f"  Percentil 95: {sorted(times)[int(len(times)*0.95)]:.3f}s")

        # Estatísticas do sistema
        if self.system_stats:
            print("\nEstatísticas do Sistema:")
            cpu_usage = [s['cpu_percent'] for s in self.system_stats]
            mem_usage = [s['memory_percent'] for s in self.system_stats]
            print(f"  CPU - Média: {statistics.mean(cpu_usage):.1f}%")
            print(f"  CPU - Máximo: {max(cpu_usage):.1f}%")
            print(f"  Memória - Média: {statistics.mean(mem_usage):.1f}%")
            print(f"  Memória - Máximo: {max(mem_usage):.1f}%")

        # Estatísticas gerais
        all_times = [r['time'] for r in self.results]
        total_bytes = sum(r['content_length'] for r in self.results)
        
        print("\nEstatísticas Gerais:")
        print(f"Total de requisições: {len(self.results)}")
        print(f"Tempo médio geral: {statistics.mean(all_times):.3f}s")
        print(f"Requisições por segundo: {len(self.results)/self.duration:.2f}")
        print(f"Taxa de erro: {(len(self.errors)/len(self.results)*100):.2f}%")
        print(f"Dados transferidos: {total_bytes/1024/1024:.2f}MB")
        print(f"Throughput: {(total_bytes/1024/1024)/self.duration:.2f}MB/s")

        # Erros
        if self.errors:
            print("\nErros encontrados:")
            error_counts = {}
            for error in self.errors:
                error_type = error['error']
                error_counts[error_type] = error_counts.get(error_type, 0) + 1
            
            for error_type, count in error_counts.items():
                print(f"  {error_type}: {count} ocorrências")

def main():
    parser = argparse.ArgumentParser(description='Teste de carga para o KeepAI')
    parser.add_argument('--users', type=int, default=10, help='Número de usuários simultâneos')
    parser.add_argument('--duration', type=int, default=60, help='Duração do teste em segundos')
    parser.add_argument('--url', type=str, default='http://localhost:5000', help='URL base da aplicação')
    parser.add_argument('--scenario', type=str, default='default', 
                       choices=['default', 'heavy_read', 'mixed'],
                       help='Cenário de teste')
    args = parser.parse_args()

    try:
        # Executa o teste
        test = LoadTest(args.url, args.users, args.duration, args.scenario)
        asyncio.run(test.run())
        test.print_results()
    except KeyboardInterrupt:
        logger.info("Teste interrompido pelo usuário")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro fatal durante o teste: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 