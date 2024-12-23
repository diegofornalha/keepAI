# KeepAI

Uma aplicação moderna para gerenciamento de notas, tarefas e calendário com integração de IA.

## Estrutura do Projeto

- [Estrutura de Infra](estrutura_modular/infra.md)
- [Estrutura de Server](estrutura_modular/server.md)
- [Estrutura de Database](estrutura_modular/database.md)
- [Estrutura de Clusters](estrutura_modular/clusters.md)

## Tecnologias Utilizadas

- **Aplicação Principal**:

  - Python/Flask
  - Jinja2 Templates
  - Bootstrap 5
  - Pydantic

- **Banco de Dados**:

  - Supabase

- **Serviços**:

  - Google Gemini (IA)
  - Flask-SocketIO (Realtime)
  - Clerk (Autenticação)

- **Infraestrutura**:
  - Docker
  - Docker Compose
  - Nginx

## Configuração do Ambiente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/keepai.git
cd keepai
```

2. Configure as variáveis de ambiente:

```bash
cp .env.example .env.local
```

3. Inicie os containers:

```bash
docker-compose up --build
```

4. Acesse a aplicação:

- http://localhost (ou http://localhost:5001 direto)

### Comandos Úteis

```bash
# Iniciar em modo desenvolvimento
docker-compose up

# Executar testes
pytest

# Formatar código
black server/
```

## Contribuição

1. Crie uma branch para sua feature: `git checkout -b feature/nome-da-feature`
2. Commit suas mudanças: `git commit -m 'feat: Adicionando nova feature'`
3. Push para a branch: `git push origin feature/nome-da-feature`
4. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Portas e Serviços

O projeto utiliza diferentes portas para cada serviço:

| Porta | Serviço            | Descrição                                                             |
| ----- | ------------------ | --------------------------------------------------------------------- |
| 5001  | Servidor Principal | Gerencia autenticação, notas, tarefas, chat e calendário              |
| 5002  | Serviço AI         | Processa requisições de inteligência artificial e geração de conteúdo |
| 5003  | Serviço Realtime   | Gerencia conexões WebSocket e eventos em tempo real                   |
| 80    | Nginx HTTP         | Proxy reverso para requisições HTTP                                   |
| 443   | Nginx HTTPS        | Proxy reverso para requisições HTTPS seguras                          |

### Endpoints Principais

- `/api/auth` - Autenticação e gerenciamento de usuários
- `/api/notes` - CRUD de notas e organização
- `/api/tasks` - Gerenciamento de tarefas e lembretes
- `/api/chat` - Comunicação em tempo real e chat
- `/api/calendar` - Eventos e calendário
- `/api/ai` - Processamento de IA e geração de conteúdo
- `/health` - Verificação de status dos serviços
