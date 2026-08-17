# 📊 Pipeline de Dados Automatizado com n8n

Automação end-to-end que combina **n8n**, **Python/pandas**, **SQL** e um **agente de IA no Telegram** para transformar um dataset bruto em dados tratados, armazenados e resumidos — tudo disparável por linguagem natural.

![Status](https://img.shields.io/badge/status-funcional-brightgreen) ![n8n](https://img.shields.io/badge/n8n-self--hosted-orange) ![Python](https://img.shields.io/badge/python-pandas-blue)

---

## 🧭 Visão geral

Imagine uma empresa que recebe diariamente um CSV de vendas. Alguém precisa tratar os dados, validar, armazenar e gerar um relatório — e, idealmente, qualquer pessoa do time deveria conseguir disparar esse processo sem abrir o n8n ou saber Python.

Este projeto resolve isso com dois workflows que **conversam entre si**:

- Um agente de IA no Telegram interpreta o pedido do usuário em linguagem natural.
- Quando o pedido envolve processar dados, o agente aciona — como uma ferramenta — um segundo workflow responsável pela limpeza e agregação real dos dados com Python/pandas.
- O resultado volta para o agente, que responde ao usuário de forma natural, com os números reais do processamento.

O operador consulta e dispara o processamento por linguagem natural, enquanto o pipeline mantém o processamento determinístico — a IA decide *quando* agir, o Python decide *como* transformar os dados.

---

## 🏗️ Arquitetura

Diferente de versões anteriores deste projeto, os dois workflows **não rodam mais isolados**: o agente aciona o pipeline diretamente, via **Call n8n Workflow Tool**.

```
                  ┌───────────────┐
                  │ Telegram Trigger │
                  └────────┬────────┘
                           ▼
                     ┌───────────┐
                     │ AI Agent  │  (Google Gemini)
                     └─────┬─────┘
             ┌─────────────┼──────────────┬───────────────┐
             ▼             ▼              ▼               ▼
        Simple Memory  Calculator     Date & Time   Call 'Pipeline de Dados'
                                                            │
                                                            ▼
                                          ┌──────────────────────────────┐
                                          │      Pipeline de Dados        │
                                          │ (When Executed by Another WF) │
                                          └───────────────┬────────────────┘
                                                          ▼
                                                  Execute Command
                                                  (roda process_data.py)
                                                          │
                                                          ▼
                                                         If
                                              (verifica sucesso/erro)
                                                 ┌────────┴────────┐
                                                 ▼                 ▼
                                             sucesso              erro
                                                 │                 │
                                                 └────────┬────────┘
                                                          ▼
                                              retorna resultado ao Agent
                                                          │
                                                          ▼
                                                Send a text message
                                                (resposta no Telegram)
```
##Telegram e IA
<img width="1456" height="814" alt="image" src="https://github.com/user-attachments/assets/8d764d31-d52a-4589-a064-910d938d2a8f" />

## Execute Command
<img width="1456" height="812" alt="image" src="https://github.com/user-attachments/assets/f6e6f299-654c-4205-a182-5c69b948487a" />

**Fluxo real de uso:**

```
Usuário: Roda o pipeline de dados
   ↓
Agente decide chamar a tool "executar_pipeline"
   ↓
Sub-workflow processa dados_brutos.csv com Python/pandas
   ↓
Agent recebe o resultado e responde:
"O pipeline de dados foi executado com sucesso! 9.994 registros
foram processados e atualizados no banco de dados."
```

---

## 🔧 Tecnologias utilizadas

| Camada                   | Ferramenta                                        |
| ------------------------ | -------------------------------------------------- |
| Orquestração             | n8n (self-hosted, via npm)                          |
| Processamento de dados   | Python 3 + pandas                                   |
| Banco de dados           | SQLite (`dados.db`)                                 |
| Interface conversacional | Telegram Bot API                                    |
| Modelo de IA             | Google Gemini (via node AI Agent do n8n)            |
| Exposição pública        | ngrok (túnel HTTPS para o webhook do Telegram)      |
| Visualização             | Matplotlib (gráfico de resultados)                  |

---

## 📁 Estrutura do repositório

```
.
├── process_data.py          # Script de limpeza e agregação (Python + pandas)
├── schema.sql                # Schema SQL
├── dados_brutos.csv          # Dataset de entrada (Superstore, Kaggle)
├── dados_limpos.csv          # Saída: dados tratados
├── resumo.md                  # Saída: relatório resumo gerado automaticamente
├── resumo_grafico.png        # Visualização dos resultados
├── Banco de dados Mercado/   # Estrutura do banco
└── README.md
```

---

## 📈 Resultados reais

Rodado sobre o dataset [Superstore (Kaggle)](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) — **9.994 registros** processados sem nenhuma linha perdida na limpeza:

| Categoria       | Total em vendas | Média  | Registros |
| --------------- | --------------- | ------ | --------- |
| Technology      | 836.154         | 452,71 | 1.847     |
| Furniture       | 742.000         | 349,84 | 2.121     |
| Office Supplies | 719.047         | 119,32 | 6.026     |

---

## ▶️ Como rodar localmente

**1. Clone o repositório**

```bash
git clone https://github.com/Miranda-Vers/Proj-Dados-com-N8N.git
cd Proj-Dados-com-N8N
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

**4. Suba o n8n localmente**

O node `Execute Command` vem **desabilitado por padrão** a partir do n8n 2.0. Antes de iniciar, libere-o:

```bash
# Windows (CMD)
set NODES_EXCLUDE=[]
n8n start
```

**5. Exponha o n8n publicamente (necessário para o Telegram)**

O Telegram entrega mensagens via **webhook**, o que exige uma URL HTTPS pública alcançável pela internet — `localhost` sozinho não é suficiente, mesmo com a saída de rede liberada. A forma mais rápida para desenvolvimento é um túnel com [ngrok](https://ngrok.com):

```bash
ngrok http 5678
```

Copie a URL gerada em `Forwarding` e reinicie o n8n informando ela:

```bash
set WEBHOOK_URL=https://SUA-URL-AQUI.ngrok-free.dev/
set NODES_EXCLUDE=[]
n8n start
```

Depois, desative e reative os workflows no editor para que o n8n re-registre o webhook com a URL atual.

> ⚠️ No plano gratuito do ngrok a sessão expira periodicamente e a URL muda a cada reinício — é necessário repetir a atualização do `WEBHOOK_URL` e reativar os workflows quando isso acontecer.

---

## 🧠 Aprendizados

- Como orquestrar automações no n8n usando triggers, sub-workflows e a tool **Call n8n Workflow Tool**, que permite que um agente de IA dispare outro workflow como se fosse uma função.
- Diferença prática entre um agente de IA "conversando" e um agente de IA **executando ações reais** através de ferramentas conectadas a lógica determinística (Python).
- Limpeza e agregação de dados com Python e pandas, incluindo tratamento de encoding e valores inválidos num dataset real.
- Como o node `Telegram Trigger` depende de um webhook público, e como isso difere de chamadas de saída (outbound) — a rede pode estar liberada para *sair* e mesmo assim nada funcionar se nada souber alcançar sua máquina de *fora*.
- Diagnóstico de infraestrutura real: isolar se um erro de rede é de entrada (inbound) ou saída (outbound), testar a API do Telegram diretamente via `curl` e via `node -e`, e usar `getWebhookInfo` para confirmar exatamente para onde o Telegram está tentando entregar mensagens.

## 🐛 Desafios enfrentados (e como foram resolvidos)

- **Node `Execute Command` desaparecendo:** a partir do n8n 2.0, esse node vem bloqueado por padrão por segurança. Resolvido liberando via variável de ambiente `NODES_EXCLUDE=[]`.
- **Telegram Trigger não recebendo mensagens:** o n8n rodando apenas em `localhost` não é alcançável pelo Telegram, já que o `Telegram Trigger` depende de um webhook HTTPS público. Resolvido expondo a instância local via túnel **ngrok** e configurando a variável `WEBHOOK_URL` com a URL pública antes de iniciar o n8n.
- **Webhook desatualizado após reiniciar o túnel:** ao reiniciar o ngrok, a URL pública muda — se o n8n não for reiniciado com a nova URL e o workflow reativado, o Telegram continua tentando entregar mensagens para uma URL que não existe mais (`getWebhookInfo` retornando `url` vazio ou desatualizado). Resolvido criando uma rotina fixa de reinício: subir o túnel → atualizar `WEBHOOK_URL` → reiniciar o n8n → reativar os workflows.
- **Diagnóstico de rede (inbound vs outbound):** testes com `curl` confirmaram que chamadas de saída para GitHub e Telegram funcionavam normalmente, isolando o problema real como sendo apenas a ausência de uma URL pública para receber mensagens — não um bloqueio de firewall, como se suspeitava inicialmente.

---

## 📎 Próximos passos

- [ ] Fazer `process_data.py` retornar um resultado estruturado (JSON com `execution_id`, contagem de registros processados/rejeitados) em vez de apenas texto solto no stdout, tornando a verificação de sucesso/erro mais robusta que a checagem atual de `stderr` vazio.
- [ ] Adicionar validação de qualidade de dados (colunas obrigatórias, valores negativos, categorias vazias) antes da agregação.
- [ ] Persistir cada execução no banco com um `execution_id`, permitindo rastrear o histórico de processamentos.
- [ ] Adicionar tratamento de erros mais granular, com notificação automática no Telegram em caso de falha no pipeline.
- [ ] Agendar execução automática (Schedule Trigger), além do disparo via chat.
- [ ] Adicionar testes automatizados (pytest) para as funções de limpeza e agregação.

---

## 📄 Licença

Este projeto é livre para fins de estudo e portfólio.
