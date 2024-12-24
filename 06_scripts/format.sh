#!/bin/bash

# Formata todos os arquivos Python usando Black
black .

# Verifica se há erros de formatação
black --check . 