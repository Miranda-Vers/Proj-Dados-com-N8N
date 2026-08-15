# 📊 Pipeline de Dados Automatizado com n8n

Automação end-to-end que combina **n8n**, **Python/pandas**, **SQL** e **Git/GitHub**
para transformar um dataset bruto em dados tratados, armazenados e versionados
automaticamente — com um agente de IA no Telegram como camada de interação.

![Status](https://img.shields.io/badge/status-funcional-brightgreen)
![n8n](https://img.shields.io/badge/n8n-self--hosted-orange)
![Python](https://img.shields.io/badge/python-pandas-blue)

---

## 🧭 Visão geral

Este projeto nasceu como um exercício prático para aplicar, num único fluxo real,
os conceitos de:

- Orquestração de automações (n8n)
- APIs REST e webhooks
- Lógica condicional em workflows
- Processamento de dados com Python e pandas
- Persistência em banco de dados SQL
- Versionamento automático via API do GitHub
- Um agente de IA conversacional como interface (Telegram + Groq)

O resultado é um pipeline que lê um dataset, limpa e agrega os dados, grava tudo
num banco SQL, gera um relatório e (opcionalmente) versiona esse relatório no
GitHub — tudo orquestrado visualmente no n8n.

---

## 🏗️ Arquitetura

O projeto é dividido em dois workflows n8n:

### 1. `Pipeline de Dados` (sub-workflow)

```
When Executed by Another Workflow
        │
        ▼
  Execute Command  ──►  roda process_data.py (Python + pandas)
        │
        ▼
        If  ──► verifica se o processamento rodou sem erro (stderr vazio)
       / \
  true/    \false
     ▼        ▼
 "sucesso"  "erro"   ──► Edit Fields com status + mensagem de retorno
```
<img width="1647" height="923" alt="image" src="https://github.com/user-attachments/assets/286f2f4e-53b2-4232-b6a0-3efa8f2b5cdb" />


### 2. `Telegram + Agente de IA`

```
Telegram Trigger (mensagem recebida)
        │
        ▼
    AI Agent (Groq)
    ├─ Simple Memory       (mantém contexto da conversa)
    ├─ Calculator          (tool)
    ├─ Date & Time         (tool) (Da para colocar outras tools(ferramentas, em um geral ajuda a concentrar certas tarefas a ferramentas especificas)
    └─ [futuro] Pipeline de Dados (tool, via Call n8n Workflow Tool)
        │
        ▼
  Send a text message  ──► responde no Telegram ( a Ia responde automaticamente, usei Groq pela a facilidade de conseguir o link da API após treina-la, mas da para usar qualquer outra)
```

<img width="1674" height="864" alt="image" src="https://github.com/user-attachments/assets/650dc8fa-91ed-4385-aae1-8c1a1557927f" />

> Os dois workflows já funcionam de forma independente. A conexão entre eles
> (o agente disparando o pipeline por comando de chat) está mapeada nos
> Próximos Passos.

---

## 🔧 Tecnologias utilizadas

| Camada | Ferramenta |
|---|---|
| Orquestração | n8n (self-hosted, via npm) |
| Processamento de dados | Python 3 + pandas |
| Banco de dados | SQLite (`dados.db`) |
| Versionamento | Git / GitHub |
| Interface conversacional | Telegram Bot API |
| Modelo de IA | Groq (via node AI Agent do n8n treinada para responder as perguntas dos usuários ) |
| Visualização | Matplotlib (gráfico de resultados) |

---

## 📁 Estrutura do repositório

```
.
├── process_data.py          # Script de limpeza e agregação (Python + pandas)
├── schema.sql                # Schema SQL (versões Postgres e SQLite)
├── dados_brutos.csv          # Dataset de entrada (Superstore, Kaggle)
├── dados_limpos.csv          # Saída: dados tratados
├── resumo.md                  # Saída: relatório resumo gerado automaticamente
├── resumo_grafico.png        # Visualização dos resultados
├── workflow_pipeline_dados.png   # Print do workflow "Pipeline de Dados"
├── workflow_telegram_agente.png  # Print do workflow do Telegram + Agente
└── README.md
```

---

## 📈 Resultados reais

Rodado sobre o dataset [Superstore (Kaggle)](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
— **9.994 registros** processados sem nenhuma linha perdida na limpeza:

| Categoria | Total em vendas | Média | Registros |
|---|---|---|---|
| Technology | 836.154 | 452,71 | 1.847 |
| Furniture | 742.000 | 349,84 | 2.121 |
| Office Supplies | 719.047 | 119,32 | 6.026 |

![Gráfico de vendas por categoria](./resumo_grafico.png)

---

## ▶️ Como rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
cd SEU-REPOSITORIO
```

**2. Instale as dependências Python**
```bash
python -m pip install pandas tabulate
```

**3. Rode o script isoladamente (sem n8n)**
```bash
python process_data.py
```
Isso gera `dados_limpos.csv`, `resumo.md` e `dados.db` na pasta.

**4. (Opcional) Suba o n8n localmente**

O node `Execute Command`, usado para rodar o script Python dentro do n8n, vem
**desabilitado por padrão** a partir do n8n 2.0. Antes de iniciar, libere-o:

```bash
# Windows (CMD)
set NODES_EXCLUDE=[]
n8n start

# PowerShell
$env:NODES_EXCLUDE="[]"
n8n start
```

Acesse `http://localhost:5678`, importe os workflows (`.json`, se incluídos)
ou recrie os nodes conforme o diagrama de arquitetura acima.

---

## 🧠 Aprendizados

- Como orquestrar automações no n8n usando triggers, nodes e sub-workflows chamados como ferramentas por um agente de IA.
- Integração com APIs REST reais (Telegram e GitHub) dentro de um fluxo automatizado, incluindo autenticação por token.
- Limpeza e agregação de dados com Python e pandas, incluindo tratamento de encoding e valores inválidos num dataset real.
- Armazenamento de dados processados em banco SQL (SQLite) e versionamento automático de relatórios via API do GitHub.
- Diagnóstico de problemas reais de infraestrutura (rede, firewall, dependências) — a parte que mais ensina, porque não tem tutorial que cobre exatamente o seu erro.

## 🐛 Desafios enfrentados (e como foram resolvidos)

- **Node `Execute Command` desaparecendo:** a partir do n8n 2.0, esse node vem
  bloqueado por padrão por segurança. Resolvido liberando via variável de
  ambiente `NODES_EXCLUDE=[]`.
- **Bloqueio de rede local:** chamadas às APIs do GitHub e do Telegram
  retornavam timeout a partir do n8n rodando localmente, mesmo com internet
  funcionando normalmente para outros serviços — sintoma de firewall/rede
  restritiva no ambiente de desenvolvimento. Contornado versionando os
  arquivos manualmente via Git/VSCode enquanto essa camada não é destravada.
- **Comparação de tipos no node `If`:** o campo `exitCode` do `Execute Command`
  chegava como número, mas a condição não validava de forma consistente entre
  execuções. Resolvido trocando a lógica de verificação para `stderr is empty`,
  uma checagem mais direta e sem ambiguidade de tipo.

---

## 📎 Próximos passos

- [ ] Conectar o `Pipeline de Dados` como ferramenta do agente de IA via
      **Call n8n Workflow Tool**, permitindo disparar o pipeline por comando
      de chat no Telegram.
- [ ] Reativar a integração automática com a API do GitHub assim que o
      ambiente de rede permitir.
- [ ] Adicionar tratamento de erros mais granular no workflow.
- [ ] Agendar execução automática (Schedule Trigger).
- [ ] Migrar de SQLite para um banco relacional hospedado (Postgres), se o
      projeto crescer.

---

## 📄 Licença

Este projeto é livre para fins de estudo e portfólio.
