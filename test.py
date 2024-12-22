import unittest
import sys
import os

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Importa os testes
from server.utils.tests import TestCache, TestLogger

if __name__ == '__main__':
    # Cria uma suíte de testes
    suite = unittest.TestSuite()
    
    # Adiciona as classes de teste
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCache))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLogger))
    
    # Executa os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Sai com código de erro se algum teste falhou
    sys.exit(not result.wasSuccessful()) 