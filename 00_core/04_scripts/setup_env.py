"""Script para configurar o .env com as URLs do Supabase."""

import os
from typing import Dict, Optional


def load_env(env_path: str = ".env") -> Dict[str, str]:
    """Carrega as variáveis do arquivo .env."""
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip().strip('"')
    return env_vars


def save_env(env_vars: Dict[str, str], env_path: str = ".env") -> None:
    """Salva as variáveis no arquivo .env."""
    with open(env_path, "w", encoding="utf-8") as f:
        for key, value in sorted(env_vars.items()):
            f.write(f'{key}="{value}"\n')


def setup_supabase_urls(
    password: Optional[str] = None,
    project_ref: str = "uaxnbpzamzxradpmccse",
    region: str = "aws-0-sa-east-1",
) -> Dict[str, str]:
    """Configura as URLs do Supabase."""
    if not password:
        password = input("Digite sua senha do Supabase: ")

    # Conexão direta para a aplicação principal
    base_url = f"postgresql://postgres.{project_ref}:{password}@{region}"
    db_url = f"{base_url}.supabase.co:5432/postgres"

    return {
        "DATABASE_URL": db_url,  # Conexão direta para a aplicação
        "SUPABASE_DB_URL": db_url,  # Alias para scripts
    }


def main() -> None:
    """Função principal."""
    # Carrega variáveis existentes
    env_vars = load_env()

    # Configura URLs do Supabase
    supabase_urls = setup_supabase_urls()
    env_vars.update(supabase_urls)

    # Salva o arquivo
    save_env(env_vars)
    print("✅ Arquivo .env atualizado com sucesso!")
    print("🔑 As URLs do Supabase foram configuradas.")
    print("\nURLs configuradas:")
    print("- DATABASE_URL: Conexão direta para a aplicação")
    print("- SUPABASE_DB_URL: Alias para scripts de migração")


if __name__ == "__main__":
    main()
