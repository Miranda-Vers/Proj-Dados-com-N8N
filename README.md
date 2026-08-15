# Proj-Dados-com-N8N
# 📊 Pipeline de Dados Automatizado com n8n

Automação que lê um dataset CSV, processa com Python/pandas, grava os resultados
num banco SQL e versiona o relatório final no GitHub — tudo orquestrado pelo n8n.

## 🔧 Tecnologias utilizadas
- **n8n** — orquestração do fluxo (triggers, nodes, integração entre etapas)
- **Python + pandas** — limpeza e agregação dos dados
- **PostgreSQL** — armazenamento dos dados tratados
- **GitHub API** — versionamento automático do relatório final
- **Telegram/Slack** — notificação de conclusão

## 🔄 Como funciona o fluxo
1. Trigger inicia o workflow
2. n8n carrega o dataset (CSV)
3. Um script Python (pandas) limpa e agrega os dados
4. Os dados tratados são inseridos numa tabela PostgreSQL
5. Um relatório resumo é commitado automaticamente no GitHub
6. Uma notificação avisa que o pipeline rodou com sucesso

![Print do workflow](./workflow.png)
<!-- Troque pela captura de tela real do seu workflow no n8n -->

## ▶️ Como rodar
1. Clone este repositório
2. Rode `schema.sql` no seu banco Postgres (ou SQLite)
3. Configure as credenciais no n8n (Postgres, GitHub, Telegram)
4. Importe o `workflow.json` exportado do seu n8n
5. Ative o workflow

## 🧠 Aprendizados
Como orquestrar automações no n8n usando triggers, nodes e sub-workflows chamados como ferramentas por um agente de IA.
- Integração com APIs REST reais (Telegram e GitHub) dentro de um fluxo automatizado, incluindo autenticação por token.
- Limpeza e agregação de dados com Python e pandas, incluindo tratamento de encoding e valores inválidos num dataset real.
- Armazenamento de dados processados em banco SQL (SQLite) e versionamento automático de relatórios via API do GitHub.
- Diagnóstico de problemas reais de infraestrutura (rede, firewall, dependências) — a parte que mais ensina, porque não tem tutorial que cobre exatamente o seu erro.

## 📎 Próximos passos
- [ ] Adicionar tratamento de erros no workflow
- [ ] Agendar execução automática (Schedule Trigger)
- [ ] Criar um dashboard simples de visualização