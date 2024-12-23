#!/usr/bin/env python3
import os
import sys
import time
import logging
import boto3
from datetime import datetime
from pathlib import Path
import subprocess
import gzip
import shutil

class BackupManager:
    def __init__(self):
        self.backup_dir = os.getenv('BACKUP_DIR')
        self.retention_days = int(os.getenv('BACKUP_RETENTION_DAYS', 30))
        self.s3_bucket = os.getenv('BACKUP_S3_BUCKET')
        
    def create_backup(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{self.backup_dir}/backup_{timestamp}.sql"
        
        # Backup do Postgres
        try:
            subprocess.run([
                'pg_dump',
                '-h', 'localhost',
                '-U', os.getenv('DB_USER'),
                '-d', os.getenv('DB_NAME'),
                '-f', backup_file
            ], check=True)
            
            # Compressão
            if os.getenv('BACKUP_COMPRESSION') == 'true':
                with open(backup_file, 'rb') as f_in:
                    with gzip.open(f"{backup_file}.gz", 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                backup_file = f"{backup_file}.gz"
            
            # Upload para S3
            if self.s3_bucket:
                s3 = boto3.client('s3')
                s3.upload_file(
                    backup_file,
                    self.s3_bucket,
                    f"backups/{Path(backup_file).name}"
                )
                
            return True
            
        except Exception as e:
            logging.error(f"Erro no backup: {str(e)}")
            return False
            
    def cleanup_old_backups(self):
        # Remove backups antigos
        current_time = time.time()
        for backup_file in Path(self.backup_dir).glob('backup_*.sql*'):
            if (current_time - backup_file.stat().st_mtime) > (self.retention_days * 86400):
                backup_file.unlink()

if __name__ == '__main__':
    backup_mgr = BackupManager()
    if backup_mgr.create_backup():
        backup_mgr.cleanup_old_backups()
        print("Backup concluído com sucesso!")
    else:
        sys.exit(1) 