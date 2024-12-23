from server.config.settings import settings


def main() -> None:
    """Função principal"""
    print(f"Projeto: {settings.PROJECT_NAME}")
    print(f"Versão: {settings.VERSION}")


if __name__ == "__main__":
    main()
