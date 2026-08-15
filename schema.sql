-- schema.sql
-- Tabela para armazenar os dados tratados pelo pipeline n8n.
-- Rode este script uma vez no seu banco antes de ativar o workflow.

-- ==== Versao utilizando o PostgreSQL ====
CREATE TABLE IF NOT EXISTS dados_processados (
    id SERIAL PRIMARY KEY,
    categoria VARCHAR(100) NOT NULL,
    valor NUMERIC(12, 2) NOT NULL,
    data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==== Versao SQLite (use esta se nao quiser instalar Postgres) ====
-- CREATE TABLE IF NOT EXISTS dados_processados (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     categoria TEXT NOT NULL,
--     valor REAL NOT NULL,
--     data_processamento TEXT DEFAULT CURRENT_TIMESTAMP
-- );