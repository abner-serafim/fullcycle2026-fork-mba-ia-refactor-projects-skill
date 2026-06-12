# Diretrizes de Heurísticas para Análise de Stack e Domínio

Este guia fornece as regras estritas que a Skill deve adotar para reconhecer a tecnologia e mapear o escopo do ecossistema alvo durante a **Fase 1 (Análise)**.

## 1. Detecção de Linguagem e Framework
A Skill deve mapear os arquivos manifestos na raiz do projeto para classificar o ecossistema:
- **Python / Flask:** - Presença de arquivos com extensão `.py`.
  - Arquivo `requirements.txt` contendo termos como `Flask`, `Flask-CORS` ou `Flask-SQLAlchemy`.
  - Declarações no código-fonte como `from flask import Flask`.
- **Node.js / Express:** - Presença de arquivos com extensão `.js`.
  - Arquivo `package.json` contendo nas dependências chaves como `"express"` ou `"sqlite3"`.
  - Chamadas de importação no código como `require('express')`.

## 2. Identificação da Camada de Persistência (Banco de Dados)
Para determinar qual banco de dados e conector estão sendo empregados:
- **SQLite3 Cru (Nativo):** Procurar por `import sqlite3` (Python) ou `require('sqlite3')` (JavaScript), mapeando o arquivo físico de destino (ex: `loja.db`, `:memory:`).
- **SQLAlchemy (ORM):** Identificar a inicialização de classes herdadas de ORM, como `db.Model` ou `SQLAlchemy()`.

## 3. Mapeamento de Tabelas e Esquemas
A Skill deve varrer os scripts de inicialização (`CREATE TABLE IF NOT EXISTS`) ou os arquivos dentro da pasta `models/` contendo propriedades decoradas (`__tablename__`) para extrair e listar o nome exato das tabelas de dados gerenciadas.

## 4. Dedução do Domínio de Negócio
Para preencher o campo "Domain" do relatório final, a inteligência deve analisar os nomes das rotas e das entidades manipuladas:
- Rotas contendo `/produtos`, `/checkout`, `/pedidos`: Classificar como **E-commerce / Sistema de Vendas**.
- Rotas contendo `/tasks`, `/categories`: Classificar como **Gerenciador de Tarefas / Produtividade**.
- Rotas contendo `/courses`, `/enrollments`: Classificar como **LMS / Plataforma de Ensino**.