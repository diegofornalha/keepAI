# KeepAI

KeepAI é um assistente pessoal inteligente para gerenciamento de notas e compromissos. Desenvolvido com Python e Flask, ele oferece uma interface web simples e intuitiva para:

- Criar notas e lembretes
- Gerenciar compromissos
- Organizar tarefas
- Manter um histórico de conversas

## Principais Funcionalidades

- 📝 Criação e edição de notas
- 💬 Chat interativo com IA
- ⏰ Gerenciamento de compromissos
- 🔄 Sincronização em tempo real

## Em Desenvolvimento

Funcionalidades que estão sendo implementadas:

- 📝 Atualização completa do conteúdo das notas (atualmente só título)
- 🔍 Sistema de filtros e busca de notas
- ⚡️ Ordenação personalizada das notas
- 🌐 Testes de integração na versão web
- 🚀 Deploy e testes no ambiente Vercel

## Tecnologias

- Python/Flask
- Supabase (Banco de dados)
- Google Gemini (IA)
- HTML/CSS/JavaScript
- Vercel (Deploy)

### Explicação Detalhada do Projeto KeepAI e Recomendações

### **1. Estrutura e Organização**

A estrutura modular do KeepAI está bem definida. Organizar os diretórios conforme o padrão sugerido melhora a manutenibilidade e escalabilidade. Aqui está o significado de cada diretório:

- **`server/`:** Contém o código principal do servidor.
  - **`modules/`:** Módulos específicos, como gerenciamento de notas ou usuários.
  - **`config/`:** Arquivos de configuração, como conexões com banco de dados.
  - **`static/`:** Arquivos estáticos, como CSS, JS ou imagens.
  - **`templates/`:** Modelos de página HTML.
  - **`utils/`:** Funções utilitárias reutilizáveis.
- **`tests/`:** Armazena testes unitários e funcionais, garantindo qualidade no desenvolvimento.
- **`docs/`:** Contém documentação do projeto.
- **`scripts/`:** Scripts para automação ou inicialização.

---

### **3. Testes Automatizados**

Testes garantem que o código funcione conforme esperado. Use `pytest` para criar testes:

**Exemplo:**

```python
python
Copiar código
import pytest
from server.modules.notes_manager import NotesManager

def test_criar_nota():
    notes_manager = NotesManager(mock_supabase_client())
    resultado = notes_manager.criar_nota("Teste de nota")
    assert "✅" in resultado
    assert "nota" in resultado.lower()

```

Testes validam funções críticas como criação e leitura de notas.

---

### **4. Melhorias de Segurança**

**Rate Limiting:** Limita o número de requisições por IP para prevenir abusos.

**Exemplo:**

```python
python
Copiar código
from functools import wraps
from flask import request, jsonify
import time

def rate_limit(limit=60, window=60):  # 60 requisições por minuto
    def decorator(f):
        requests = {}

        @wraps(f)
        def wrapped(*args, **kwargs):
            now = time.time()
            ip = request.remote_addr

            # Limpa requisições antigas
            requests[ip] = [req for req in requests.get(ip, [])
                          if req > now - window]

            if len(requests.get(ip, [])) >= limit:
                return jsonify({'error': 'Taxa limite excedida'}), 429

            requests.setdefault(ip, []).append(now)
            return f(*args, **kwargs)

        return wrapped
    return decorator

```

Isso impede que um usuário sobrecarregue o sistema com requisições excessivas.

---

### **5. Documentação**

Uma boa documentação ajuda desenvolvedores e usuários a entenderem o funcionamento da API.

**Exemplo de Documentação:**

````markdown
markdown
Copiar código

# API Documentation

## Endpoints

### POST /api/chat

Processa mensagens do usuário e retorna respostas do assistente.

**Request:**

```json
{
  "message": "criar nota sobre reunião amanhã às 10h"
}
```
````

**Response:**

```json
json
Copiar código
{
    "response": "✅ Criei uma nota sobre sua reunião! Quer adicionar mais algum detalhe?"
}

```

### GET /api/notes

Lista todas as notas do usuário.

````yaml
yaml
Copiar código
---

#### **6. Configuração no macOS**
Configurar o ambiente virtual no macOS garante que as dependências sejam gerenciadas corretamente.

**Passos:**
1. Criar e ativar o ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

````

1. Instalar dependências:

   ```bash
   bash
   Copiar código
   pip install -r requirements.txt

   ```

2. Configurar variáveis de ambiente:

   ```
   env
   Copiar código
   FLASK_APP=server/app.py
   FLASK_ENV=development
   FLASK_DEBUG=1

   ```

---

### **7. Próximos Passos**

Sugestões para futuras implementações:

- **Backup automático:** Evitar perda de dados.
- **Markdown:** Suporte para formatação nas notas.
- **Tags:** Agrupamento e categorização.
- **Notificações:** Lembretes automáticos para compromissos.
- **Interface responsiva:** Melhor experiência em dispositivos móveis.

Com essas melhorias, o KeepAI será mais robusto, seguro e fácil de usar.

## Sistema de Logging e Cache

### Configuração

1. **Logs**

   - Localização: `/logs/`
   - Arquivos:
     - `keepai.log`: Logs principais da aplicação
     - `grpc.log`: Logs específicos do gRPC
   - Rotação: 10MB por arquivo, mantém 5 arquivos de backup

2. **Cache**
   - TTL padrão: 1 minuto para notas
   - Limpeza automática: A cada 5 minutos
   - Estatísticas disponíveis em: `/api/cache/stats`

### Como Usar

#### Monitoramento de Logs

1. **Visualizar logs em tempo real**:

```bash
tail -f logs/keepai.log
```

2. **Formato dos logs**:

```
[DATA HORA] NÍVEL [MÓDULO:LINHA] MENSAGEM
```

Exemplo:

```
[2024-12-22 07:32:39] INFO [keepai:44] Inicializando KeepAI...
```

3. **Níveis de Log**:

- DEBUG: Informações detalhadas para debugging
- INFO: Informações gerais sobre operações
- WARNING: Avisos que não impedem a operação
- ERROR: Erros que afetam funcionalidades

4. **Informações Extras**:

- IP do cliente
- User Agent
- Tamanho das mensagens
- Contagem de itens
- Stack traces em erros

#### Monitoramento de Cache

1. **Estatísticas**:

```bash
curl http://localhost:3000/api/cache/stats
```

Resposta:

```json
{
  "hits": 10,
  "misses": 2,
  "sets": 12,
  "total_items": 5,
  "hit_rate": "83.33%"
}
```

2. **Métricas Disponíveis**:

- `hits`: Número de acertos no cache
- `misses`: Número de falhas no cache
- `sets`: Número de itens armazenados
- `total_items`: Itens atualmente no cache
- `hit_rate`: Taxa de acerto (hits/total de requisições)

### Testes de Carga

1. **Executar testes unitários**:

```bash
python test.py
```

2. **Simular múltiplos usuários**:

```bash
python load_test.py --users 10 --duration 60
```

### Troubleshooting

1. **Porta em Uso**:

- O servidor tentará automaticamente a próxima porta disponível
- Exemplo: se 3000 estiver em uso, tentará 3001, 3002, etc.

2. **Logs Muito Grandes**:

- Rotação automática ao atingir 10MB
- Mantém 5 arquivos de backup (keepai.log.1, keepai.log.2, etc.)

3. **Problemas Comuns**:

- Erro de conexão: Verifique logs/keepai.log
- Erros gRPC: Verifique logs/grpc.log
- Cache não funcionando: Verifique /api/cache/stats

### Boas Práticas

1. **Monitoramento**:

- Verifique os logs regularmente
- Monitore a taxa de acerto do cache
- Configure alertas para erros frequentes

2. **Manutenção**:

- Limpe logs antigos periodicamente
- Ajuste TTL do cache conforme necessidade
- Monitore uso de memória do cache

3. **Segurança**:

- Não exponha /api/cache/stats em produção
- Proteja o diretório de logs
- Limite o tamanho máximo de mensagens

### Desenvolvimento

1. **Adicionar Novos Logs**:

```python
logger.info('Mensagem', extra={
    'chave': 'valor',
    'outra_info': 123
})
```

2. **Usar Cache**:

```python
@cached(ttl_minutes=5)
def minha_funcao():
    # código aqui
    pass
```

### Próximos Passos

1. **Melhorias Planejadas**:

- Adicionar métricas de performance
- Implementar logs estruturados (JSON)
- Integrar com sistemas de monitoramento

2. **Monitoramento Contínuo**:

- Analisar padrões de uso
- Identificar gargalos
- Otimizar configurações

## Gerenciamento de Logs

O sistema utiliza um mecanismo automatizado de rotação e compressão de logs com as seguintes características:

- Rotação diária de logs
- Compressão automática de logs antigos
- Retenção de logs por 30 dias
- Logs são comprimidos usando gzip para economia de espaço

### Configuração do Sistema de Logs

1. O arquivo de configuração está em `logs/logrotate.conf`
2. O script de rotação está em `logs/rotate_logs.sh`
3. A automação é feita via launchd (macOS) com o arquivo `com.keepai.logrotate.plist`

Para instalar a automação de logs:

```bash
# Copie o arquivo plist para o diretório de LaunchAgents
cp com.keepai.logrotate.plist ~/Library/LaunchAgents/

# Carregue o serviço
launchctl load ~/Library/LaunchAgents/com.keepai.logrotate.plist
```

Para executar a rotação de logs manualmente:

```bash
./logs/rotate_logs.sh
```

## Sistema de Backup Automático

O sistema realiza backups autom��ticos diários dos seguintes componentes:

- Banco de dados Supabase
- Arquivos de configuração
- Logs do sistema

### Configuração do Backup

1. Configure as variáveis de ambiente no arquivo `.env`:

   ```bash
   # Supabase (obrigatório)
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

2. Instale o serviço de backup:

   ```bash
   # Copie o arquivo plist para o diretório de LaunchAgents
   cp com.keepai.backup.plist ~/Library/LaunchAgents/

   # Carregue o serviço
   launchctl load ~/Library/LaunchAgents/com.keepai.backup.plist
   ```

### Características do Backup

- **Frequência**: Diário (1:00 AM)
- **Retenção**: 7 dias
- **Compressão**: Arquivos são comprimidos em formato tar.gz
- **Armazenamento**: Supabase (tabela `backups`)
- **Logs**: Disponíveis em `logs/backup_output.log` e `logs/backup_error.log`

### Executar Backup Manualmente

```bash
python scripts/backup.py
```

### Restauração de Backup

Os backups são armazenados na tabela `backups` do Supabase com os seguintes campos:

- `filename`: Nome do arquivo de backup
- `timestamp`: Data e hora do backup
- `size`: Tamanho do backup em bytes
- `content`: Conteúdo do backup comprimido

Para restaurar um backup:

1. Acesse o Supabase e baixe o backup desejado
2. Descompacte o arquivo tar.gz
3. Restaure os dados do Supabase usando o arquivo JSON
4. Copie os arquivos de configuração conforme necessário
