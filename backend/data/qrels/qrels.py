import pandas as pd

def load_qrels(qrels_path):
    # Cargar archivo con columnas: query-id, doc-id, relevance (score binario)
    df = pd.read_csv(qrels_path, sep="\t", header=0, names=["query_id", "doc_id", "relevance"])
    
    # Asegurar que los IDs sean strings para evitar problemas de comparación
    df["query_id"] = df["query_id"].astype(str)
    df["doc_id"] = df["doc_id"].astype(str)
    df["relevance"] = df["relevance"].astype(int)  # En caso venga como float

    return df

def load_queries(queries_path):
    # Asume formato: query-id \t query-text
    return pd.read_csv(queries_path, sep="\t", names=["query_id", "query_text"])