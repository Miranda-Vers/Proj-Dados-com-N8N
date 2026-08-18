"""
process_data.py
------------------------------------------------------------
Script de limpeza e agregacao de dados para o pipeline n8n.
Este script e chamado pelo node "Execute Command" do n8n.

COMO ADAPTAR:
1. Troque INPUT_CSV pelo caminho real do seu arquivo de entrada.
2. Ajuste COL_CATEGORIA e COL_VALOR para os nomes reais das
   colunas do seu dataset.
3. O script gera dois arquivos de saida:
   - dados_limpos.csv  -> pronto para o node Postgres inserir no banco
   - resumo.md         -> pronto para o node do GitHub commitar
4. Ao final, imprime uma unica linha de JSON no stdout com o
   resultado da execucao (success, contagens, execution_id).
   E essa linha que o n8n deve parsear no Code node.
------------------------------------------------------------
"""
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# ---------- CONFIGURACAO (ajuste aqui para o seu dataset) ----------
INPUT_CSV = "dados_brutos.csv"
OUTPUT_CSV = "dados_limpos.csv"
OUTPUT_SUMMARY = "resumo.md"

COL_CATEGORIA = "Category"    # coluna usada para agrupar os dados
COL_VALOR = "Sales"           # coluna numerica que sera somada/media
# ---------------------------------------------------------------------


def carregar_dados(caminho: str) -> pd.DataFrame:
    """Le o CSV bruto e para a execucao com uma mensagem clara se o arquivo nao existir."""
    if not Path(caminho).exists():
        sys.exit(f"Erro: arquivo '{caminho}' nao encontrado. Ajuste INPUT_CSV no topo do script.")
    return pd.read_csv(caminho, encoding="ISO-8859-1")


def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas vazias, duplicadas e valores invalidos na coluna numerica."""
    antes = len(df)

    df = df.dropna(how="all")
    df = df.drop_duplicates()

    df[COL_VALOR] = pd.to_numeric(df[COL_VALOR], errors="coerce")
    df = df.dropna(subset=[COL_VALOR])

    depois = len(df)
    # debug para quem roda manualmente no terminal - nao interfere no JSON final,
    # que sempre sai por ultimo, na ultima linha do stdout
    print(f"[debug] Linhas antes da limpeza: {antes} | depois: {depois}", file=sys.stderr)
    return df


def gerar_resumo(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa por categoria e calcula total, media e contagem de registros."""
    resumo = (
        df.groupby(COL_CATEGORIA)[COL_VALOR]
        .agg(total="sum", media="mean", registros="count")
        .reset_index()
        .sort_values("total", ascending=False)
    )
    return resumo


def salvar_resumo_markdown(resumo: pd.DataFrame, caminho: str) -> None:
    """Salva o resumo como uma tabela markdown, pronta para virar README/commit."""
    conteudo = "# Resumo do processamento\n\n" + resumo.to_markdown(index=False)
    Path(caminho).write_text(conteudo, encoding="utf-8")


def main() -> None:
    execution_id = str(uuid.uuid4())
    started_at = datetime.now(timezone.utc).isoformat()

    try:
        df = carregar_dados(INPUT_CSV)
        antes = len(df)

        df_limpo = limpar_dados(df)
        depois = len(df_limpo)

        df_limpo.to_csv(OUTPUT_CSV, index=False)

        resumo = gerar_resumo(df_limpo)
        salvar_resumo_markdown(resumo, OUTPUT_SUMMARY)

        top = resumo.iloc[0]

        resultado = {
            "success": True,
            "execution_id": execution_id,
            "started_at": started_at,
            "rows_input": antes,
            "rows_output": depois,
            "rows_rejected": antes - depois,
            "top_category": str(top[COL_CATEGORIA]),
            "top_category_total": float(top["total"]),
        }
    except Exception as e:
        resultado = {
            "success": False,
            "execution_id": execution_id,
            "started_at": started_at,
            "error_type": type(e).__name__,
            "message": str(e),
        }

    # linha unica de JSON no stdout - e isso que o n8n vai capturar
    print(json.dumps(resultado, ensure_ascii=False))


if __name__ == "__main__":
    main()