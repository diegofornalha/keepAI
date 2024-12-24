# Notebooks do KeepAI

Este diretório contém notebooks Jupyter para desenvolvimento, testes e análises do projeto.

## Estrutura

Os notebooks estão organizados numericamente por ordem de prioridade e dependência:

### 01 - Testes de Banco de Dados

- `01_test_migrations.ipynb`: Testa as migrações do Supabase
  - Verifica schemas e tabelas
  - Testa inserções e relacionamentos
  - Valida constraints e índices

### 02 - Testes do Sistema

- `02_test_keepai.ipynb`: Testa funcionalidades principais
  - Criação e gestão de notas
  - Autenticação e usuários
  - Validação de dados

### 03 - Testes de IA (TODO)

- `03_ai_tests.ipynb`: Testes dos componentes de IA
  - Embeddings e similaridade
  - Geração de texto
  - Classificação de conteúdo

## Configuração

1. Instale as dependências:

```bash
pip install jupyter notebook pandas numpy matplotlib seaborn
```

2. Configure as variáveis de ambiente:

```bash
export SUPABASE_URL=sua_url
export SUPABASE_KEY=sua_chave
```

3. Inicie o Jupyter:

```bash
jupyter notebook
```

## Boas Práticas

1. **Organização**:

   - Use numeração para indicar ordem/dependência
   - Mantenha um notebook por funcionalidade
   - Documente claramente cada seção

2. **Código**:

   - Importe bibliotecas no início
   - Use células markdown para documentação
   - Limpe outputs antes de commitar

3. **Dados**:

   - Use dados de teste, nunca produção
   - Limpe após os testes
   - Valide resultados esperados

4. **Versionamento**:
   - Mantenha notebooks no git
   - Limpe outputs antes do commit
   - Documente mudanças significativas
