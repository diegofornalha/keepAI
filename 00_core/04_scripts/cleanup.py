#!/usr/bin/env python3
"""Script para limpar arquivos temporários do projeto."""

import shutil
from pathlib import Path
from typing import List, Optional, Set


class ProjectCleaner:
    """Classe responsável por limpar arquivos temporários do projeto."""

    def __init__(self, project_root: Optional[Path] = None):
        """Inicializa o limpador com o diretório raiz do projeto."""
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.cleaned_paths: Set[str] = set()

    def get_patterns_to_clean(self) -> List[str]:
        """Retorna lista de padrões de arquivos/diretórios para limpar."""
        return [
            # Python
            "__pycache__",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            "*.so",
            "*.egg",
            "*.egg-info",
            "build",
            "dist",
            ".eggs",
            # Ambiente virtual
            ".venv",
            "venv",
            "ENV",
            # Cache e logs
            ".pytest_cache",
            ".coverage",
            ".mypy_cache",
            ".ruff_cache",
            "htmlcov",
            "*.log",
            # IDEs e editores
            ".idea",
            ".vscode",
            "*.swp",
            "*.swo",
            # Jupyter
            ".ipynb_checkpoints",
            # Mac
            ".DS_Store",
            # Outros
            "*.bak",
            "*.tmp",
            "*.temp",
        ]

    def should_clean_path(self, path: Path) -> bool:
        """Verifica se o caminho deve ser limpo."""
        # Evita limpar diretórios importantes
        protected_dirs = {
            ".git",
            "node_modules",
            "static",
            "media",
            "uploads",
        }

        return (
            path.name not in protected_dirs
            and path.name not in self.cleaned_paths
            and not any(parent.name in protected_dirs for parent in path.parents)
        )

    def clean_pattern(self, pattern: str) -> None:
        """Limpa arquivos/diretórios que correspondem ao padrão."""
        # Para arquivos com wildcard (*.pyc, *.log, etc)
        if "*" in pattern:
            for path in self.project_root.rglob(pattern):
                if self.should_clean_path(path):
                    self._remove_path(path)
        # Para diretórios específicos
        else:
            for path in self.project_root.rglob(pattern):
                if path.exists() and self.should_clean_path(path):
                    self._remove_path(path)

    def _remove_path(self, path: Path) -> None:
        """Remove um arquivo ou diretório de forma segura."""
        try:
            if path.is_file():
                path.unlink()
                print(f"Arquivo removido: {path}")
            elif path.is_dir():
                shutil.rmtree(path)
                print(f"Diretório removido: {path}")
            self.cleaned_paths.add(str(path))
        except Exception as e:
            print(f"Erro ao remover {path}: {e}")

    def clean_all(self) -> None:
        """Limpa todos os arquivos temporários do projeto."""
        print("Iniciando limpeza de arquivos temporários...")

        for pattern in self.get_patterns_to_clean():
            self.clean_pattern(pattern)

        print("\nLimpeza concluída!")
        print(f"Total de itens removidos: {len(self.cleaned_paths)}")


def main() -> None:
    """Função principal."""
    cleaner = ProjectCleaner()
    cleaner.clean_all()


if __name__ == "__main__":
    main()
