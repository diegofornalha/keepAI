import asyncio
import aiohttp
import time
import statistics
import matplotlib.pyplot as plt  # type: ignore
from datetime import datetime
import json
from typing import Dict, Any, List, Optional, Tuple


class ExtendedLoadTester:
    def __init__(self) -> None:
        self.results: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []
        self.start_time: Optional[float] = None

    async def run_scenario(
        self, scenario_name: str, endpoint: str, payload: Dict[str, Any]
    ) -> Tuple[Optional[float], Optional[int]]:
        try:
            async with aiohttp.ClientSession() as session:
                start = time.time()
                async with session.post(endpoint, json=payload) as response:
                    duration = time.time() - start
                    status = response.status

                    self.results.append(
                        {
                            "scenario": scenario_name,
                            "duration": duration,
                            "status": status,
                            "timestamp": datetime.now().isoformat(),
                        }
                    )

                    return duration, status

        except Exception as e:
            self.errors.append(
                {
                    "scenario": scenario_name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            )
            return None, None

    def generate_report(self) -> Dict[str, Any]:
        if not self.results:
            return {"message": "Sem resultados para reportar"}

        # Análise estatística
        durations = [r["duration"] for r in self.results]

        report = {
            "total_requests": len(self.results),
            "total_errors": len(self.errors),
            "avg_response_time": statistics.mean(durations),
            "median_response_time": statistics.median(durations),
            "min_response_time": min(durations),
            "max_response_time": max(durations),
            "std_dev": statistics.stdev(durations),
            "percentiles": {
                "95th": statistics.quantiles(durations, n=20)[-1],
                "99th": statistics.quantiles(durations, n=100)[-1],
            },
        }

        # Gera gráficos
        plt.figure(figsize=(10, 6))
        plt.hist(durations, bins=50)
        plt.title("Distribuição dos Tempos de Resposta")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Frequência")
        plt.savefig("load_test_results.png")

        return report


async def main() -> None:
    tester = ExtendedLoadTester()

    # Cenários de teste
    scenarios: List[Dict[str, Any]] = [
        {
            "name": "Processamento de Nota",
            "endpoint": "http://localhost:3000/api/process-note",
            "payload": {"content": "Nota de teste para análise"},
        },
        {
            "name": "Busca Semântica",
            "endpoint": "http://localhost:3000/api/search",
            "payload": {"query": "exemplo de busca"},
        },
    ]

    # Executa testes
    tasks = []
    for scenario in scenarios:
        for _ in range(100):  # 100 requisições por cenário
            tasks.append(
                tester.run_scenario(
                    scenario["name"], scenario["endpoint"], scenario["payload"]
                )
            )

    await asyncio.gather(*tasks)

    # Gera relatório
    report = tester.generate_report()

    # Salva resultados
    with open("load_test_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("Teste de carga concluído! Resultados salvos em load_test_report.json")


if __name__ == "__main__":
    asyncio.run(main())
