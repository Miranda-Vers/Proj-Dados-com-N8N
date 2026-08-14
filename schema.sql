-- schema.sql
-- Tabela para armazenar os dados tratados pelo pipeline n8n.
-- Rode este script uma vez no seu banco antes de ativar o workflow.

-- ==== Versao PostgreSQL ====
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

-- Exemplo de insercao manual (o node Postgres do n8n fara isso automaticamente
-- a partir do dados_limpos.csv gerado pelo process_data.py)
-- INSERT INTO dados_processados (categoria, valor)
-- VALUES ('exemplo', 100.50);

-- Consulta rapida para conferir se os dados estao chegando certos
-- SELECT * FROM dados_processados ORDER BY data_processamento DESC LIMIT 10;