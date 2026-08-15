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
------------------------------------------------------------
"""

import sys
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
    # encoding="ISO-8859-1" porque esse dataset (Superstore) tem alguns
    # caracteres que nao sao UTF-8 valido (ex: nomes de produto com acento estranho)
    return pd.read_csv(caminho, encoding="ISO-8859-1")


def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas vazias, duplicadas e valores invalidos na coluna numerica."""
    antes = len(df)

    df = df.dropna(how="all")
    df = df.drop_duplicates()

    df[COL_VALOR] = pd.to_numeric(df[COL_VALOR], errors="coerce")
    df = df.dropna(subset=[COL_VALOR])

    depois = len(df)
    print(f"Linhas antes da limpeza: {antes} | depois: {depois}")
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
    df = carregar_dados(INPUT_CSV)
    df_limpo = limpar_dados(df)
    df_limpo.to_csv(OUTPUT_CSV, index=False)

    resumo = gerar_resumo(df_limpo)
    salvar_resumo_markdown(resumo, OUTPUT_SUMMARY)

    print(f"Arquivos gerados: {OUTPUT_CSV}, {OUTPUT_SUMMARY}")


if __name__ == "__main__":
    main()