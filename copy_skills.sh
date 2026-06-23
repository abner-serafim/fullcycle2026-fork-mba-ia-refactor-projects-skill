#!/bin/bash

# Script de cópia e sincronização total da pasta de Custom Skills
# Autor: Abner Serafim Arede

echo "====== Iniciando a sincronização COMPLETA das pastas .agent e .claude ======"

# 1. Sincronização na raiz do repositório
if [ -d ".agent" ]; then
    mkdir -p .claude
    # Copia recursivamente todo o conteúdo mantendo a estrutura de subpastas
    cp -r .agent/* .claude/
    echo "✓ Todo o conteúdo da pasta .agent da raiz foi copiado para a pasta .claude da raiz."
else
    echo "Erro: A pasta .agent original não foi encontrada na raiz do repositório."
    echo "Certifique-se de rodar este script no diretório principal onde a pasta .agent está localizada."
    exit 1
fi

# 2. Replicação para dentro de cada um dos subprojetos
PROJECTS=("code-smells-project" "ecommerce-api-legacy" "task-manager-api")

for PROJ in "${PROJECTS[@]}"; do
    if [ -d "$PROJ" ]; then
        echo "Sincronizando estruturas completas para o projeto: $PROJ..."
        
        # Define os caminhos das pastas de destino de cada projeto
        DEST_AGENT="$PROJ/.agent"
        DEST_CLAUDE="$PROJ/.claude"
        
        # Garante a criação das pastas de destino
        mkdir -p "$DEST_AGENT"
        mkdir -p "$DEST_CLAUDE"
        
        # Executa a cópia de absolutamente todos os arquivos e subpastas (sem filtrar arquivos específicos)
        cp -r .agent/* "$DEST_AGENT/"
        cp -r .agent/* "$DEST_CLAUDE/"
        
        echo "  ✓ Conteúdo totalmente integrado em $PROJ/.agent/"
        echo "  ✓ Conteúdo totalmente integrado em $PROJ/.claude/"
    else
        echo "Aviso: O diretório do projeto $PROJ não foi encontrado. Pulando..."
    fi
done

echo "====== Sincronização global concluída com sucesso! ======"