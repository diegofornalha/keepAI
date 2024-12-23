import asyncio
import aiohttp
import time
import os
from datetime import datetime
import statistics

class LoadTester:
    def __init__(self):
        self.users = int(os.getenv('LOAD_TEST_USERS', 100))
        self.duration = int(os.getenv('LOAD_TEST_DURATION', 300))
        self.rate = int(os.getenv('LOAD_TEST_RATE', 10))
        self.results = []
        
    async def make_request(self, session, user_id):
        start_time = time.time()
        try:
            async with session.post('http://localhost:3000/api/chat', json={
                'message': 'Teste de carga',
                'user_id': f'test_user_{user_id}'
            }) as response:
                await response.text()
                duration = time.time() - start_time
                self.results.append(duration)
                return duration
        except Exception as e:
            print(f"Erro na requisição: {str(e)}")
            return None
            
    async def run_test(self):
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            tasks = []
            
            while time.time() - start_time < self.duration:
                for _ in range(self.rate):
                    task = asyncio.create_task(
                        self.make_request(session, len(tasks))
                    )
                    tasks.append(task)
                await asyncio.sleep(1)
            
            await asyncio.gather(*tasks)
            
    def print_results(self):
        if not self.results:
            return
            
        print("\nResultados do Teste de Carga:")
        print(f"Total de requisições: {len(self.results)}")
        print(f"Tempo médio: {statistics.mean(self.results):.2f}s")
        print(f"Tempo máximo: {max(self.results):.2f}s")
        print(f"Tempo mínimo: {min(self.results):.2f}s")
        print(f"Desvio padrão: {statistics.stdev(self.results):.2f}s")

if __name__ == '__main__':
    tester = LoadTester()
    asyncio.run(tester.run_test())
    tester.print_results() 