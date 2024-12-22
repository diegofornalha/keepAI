#!/usr/bin/env python3
import os
import json
import shutil
import logging
from datetime import datetime, timedelta
from pathlib import Path
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('backup')

class BackupManager:
    def __init__(self):
        self.backup_dir = Path('backups')
        self.backup_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_path = self.backup_dir / f'backup_{self.timestamp}'
        self.backup_path.mkdir(exist_ok=True)
        
        # Configuração do Supabase
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError('Credenciais do Supabase não encontradas')
        
        self.headers = {
            'apikey': self.supabase_key,
            'Authorization': f'Bearer {self.supabase_key}',
            'Content-Type': 'application/json'
        }
    
    def backup_supabase(self):
        """Backup do banco de dados Supabase"""
        try:
            # Lista todas as tabelas
            tables_response = requests.get(
                f'{self.supabase_url}/rest/v1/',
                headers=self.headers
            )
            tables = tables_response.json()
            
            # Backup de cada tabela
            db_backup = {}
            for table in tables:
                data_response = requests.get(
                    f'{self.supabase_url}/rest/v1/{table}',
                    headers=self.headers
                )
                db_backup[table] = data_response.json()
            
            # Salva o backup
            backup_file = self.backup_path / 'supabase_backup.json'
            with open(backup_file, 'w') as f:
                json.dump(db_backup, f, indent=2)
            
            logger.info('Backup do Supabase concluído com sucesso')
            return True
        except Exception as e:
            logger.error(f'Erro no backup do Supabase: {e}')
            return False
    
    def backup_config_files(self):
        """Backup dos arquivos de configuração"""
        try:
            config_files = [
                '.env',
                'prometheus.yml',
                'alert_rules.yml',
                'alertmanager.yml',
                'docker-compose.yml',
                'requirements.txt'
            ]
            
            config_backup_dir = self.backup_path / 'config'
            config_backup_dir.mkdir(exist_ok=True)
            
            for file in config_files:
                if os.path.exists(file):
                    shutil.copy2(file, config_backup_dir / file)
            
            logger.info('Backup dos arquivos de configuração concluído')
            return True
        except Exception as e:
            logger.error(f'Erro no backup dos arquivos de configuração: {e}')
            return False
    
    def backup_logs(self):
        """Backup dos arquivos de log"""
        try:
            logs_backup_dir = self.backup_path / 'logs'
            logs_backup_dir.mkdir(exist_ok=True)
            
            # Copia todos os arquivos de log
            for log_file in Path('logs').glob('*.log*'):
                shutil.copy2(log_file, logs_backup_dir / log_file.name)
            
            logger.info('Backup dos logs concluído')
            return True
        except Exception as e:
            logger.error(f'Erro no backup dos logs: {e}')
            return False
    
    def store_backup_in_supabase(self):
        """Armazena o backup no Supabase"""
        try:
            # Comprime o backup
            backup_file = f'backup_{self.timestamp}.tar.gz'
            shutil.make_archive(
                str(self.backup_path),
                'gztar',
                self.backup_path
            )
            
            # Lê o arquivo comprimido
            with open(f'{backup_file}.tar.gz', 'rb') as f:
                backup_data = f.read()
            
            # Cria registro do backup no Supabase
            backup_metadata = {
                'filename': backup_file,
                'timestamp': self.timestamp,
                'size': len(backup_data),
                'content': str(backup_data)  # Converte para string para armazenar
            }
            
            # Insere no Supabase
            response = requests.post(
                f'{self.supabase_url}/rest/v1/backups',
                headers=self.headers,
                json=backup_metadata
            )
            
            if response.status_code != 201:
                raise Exception(f'Erro ao salvar backup: {response.text}')
            
            logger.info('Backup armazenado no Supabase com sucesso')
            return True
        except Exception as e:
            logger.error(f'Erro ao armazenar backup no Supabase: {e}')
            return False
    
    def cleanup_old_backups(self, keep_days=7):
        """Remove backups antigos"""
        try:
            # Remove backups locais antigos
            for backup in self.backup_dir.glob('backup_*'):
                if backup.is_dir():
                    backup_date = datetime.strptime(
                        backup.name.split('_')[1],
                        '%Y%m%d'
                    )
                    if (datetime.now() - backup_date).days > keep_days:
                        shutil.rmtree(backup)
            
            # Remove backups antigos do Supabase
            cutoff_date = (datetime.now() - timedelta(days=keep_days)).strftime('%Y%m%d')
            
            response = requests.delete(
                f'{self.supabase_url}/rest/v1/backups',
                headers=self.headers,
                params={
                    'timestamp': f'lt.{cutoff_date}'
                }
            )
            
            if response.status_code not in [200, 204]:
                raise Exception(f'Erro ao limpar backups antigos: {response.text}')
            
            logger.info('Limpeza de backups antigos concluída')
            return True
        except Exception as e:
            logger.error(f'Erro na limpeza de backups antigos: {e}')
            return False
    
    def run_backup(self):
        """Executa o processo completo de backup"""
        logger.info('Iniciando processo de backup')
        
        # Executa todos os backups
        success = all([
            self.backup_supabase(),
            self.backup_config_files(),
            self.backup_logs()
        ])
        
        if not success:
            logger.error('Falha em uma ou mais etapas do backup')
            return False
        
        # Armazena o backup no Supabase
        if not self.store_backup_in_supabase():
            return False
        
        # Limpa backups antigos
        self.cleanup_old_backups()
        
        logger.info('Processo de backup concluído com sucesso')
        return True

if __name__ == '__main__':
    backup_manager = BackupManager()
    if backup_manager.run_backup():
        sys.exit(0)
    else:
        sys.exit(1) 