# KeepAI

KeepAI é um assistente pessoal inteligente para gerenciamento de notas, que utiliza IA para ajudar na organização e criação de conteúdo.

## Funcionalidades

- Criação de notas com título e conteúdo
- Edição de notas existentes
- Exclusão de notas
- Interface de chat com IA para interação natural
- Formatação automática de datas no padrão brasileiro
- Armazenamento persistente usando Supabase

## Tecnologias Utilizadas

- Python 3.9+
- Flask
- Supabase
- LangChain
- Google Generative AI
- HTML/CSS/JavaScript

## Configuração do Ambiente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/keepai.git
cd keepai
```

2. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
   Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
SUPABASE_URL=sua_url_do_supabase
SUPABASE_ANON_KEY=sua_chave_anonima_do_supabase
GOOGLE_API_KEY=sua_chave_api_do_google
```

4. Execute o servidor:

```bash
python -m server.app
```

## Deploy

O projeto está configurado para deploy no Vercel. Para fazer o deploy:

1. Faça fork do repositório no GitHub
2. Conecte o repositório ao Vercel
3. Configure as variáveis de ambiente no Vercel
4. Deploy!
