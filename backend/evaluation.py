import jsonlines
import pandas as pd
from search_engine import search_with_tfidf, search_with_bm25
from data.qrels.qrels import load_qrels

# Cargar queries
queries = []
with jsonlines.open("backend/data/qrels/queries.jsonl") as reader:
    for obj in reader:
        queries.append(obj)

# Cargar qrels
qrels = load_qrels("backend/data/qrels/test.tsv")
qrels["query_id"] = qrels["query_id"].astype(str)

#Funcion para obtener los documentos de qrels (test)
def get_relevant_docs(qrels_df, query_id):
    return set(
        qrels_df[
            (qrels_df["query_id"] == query_id) & (qrels_df["relevance"] > 0)
        ]["doc_id"]
    )

#Funcion para calcular MAP (Mean Average Precision)
def average_precision(retrieved_docs, relevant_docs):
    """Calcula la Average Precision (AP) para una sola query."""
    if not relevant_docs:
        return 0.0

    precisions = []
    hit_count = 0

    for rank, doc_id in enumerate(retrieved_docs, start=1):
        if doc_id in relevant_docs:
            hit_count += 1
            precisions.append(hit_count / rank)

    if not precisions:
        return 0.0

    return sum(precisions) / len(relevant_docs)


#Funcion para evaluar la búsqueda
def evaluate_search(search_fn, top_n=5, label="TF-IDF"):
    precisions = []
    recalls = []
    average_precisions = []
    rows = []

    for q in queries:
        query_id = str(q["_id"])
        query_text = q["text"]
        relevant_docs = get_relevant_docs(qrels, query_id)
        if not relevant_docs:
            continue

        results = search_fn(query_text, top_n=top_n)
        retrieved_docs = [r["id"] for r in results]

        retrieved_set = set(retrieved_docs)
        true_positives = len(retrieved_set & relevant_docs)

        precision = true_positives / len(retrieved_docs) if retrieved_docs else 0
        recall = true_positives / len(relevant_docs) if relevant_docs else 0
        ap = average_precision(retrieved_docs, relevant_docs)

        precisions.append(precision)
        recalls.append(recall)
        average_precisions.append(ap)

        rows.append({
            "query_id": query_id,
            "query_text": query_text,
            "precision": precision,
            "recall": recall,
            "average_precision": ap
        })


    # Métricas globales
    mean_precision = sum(precisions) / len(precisions) if precisions else 0
    mean_recall = sum(recalls) / len(recalls) if recalls else 0
    mean_ap = sum(average_precisions) / len(average_precisions) if average_precisions else 0

    print(f"\n[{label}] Mean Precision: {mean_precision:.3f}")
    print(f"[{label}] Mean Recall: {mean_recall:.3f}")
    print(f"[{label}] Mean Average Precision (MAP): {mean_ap:.3f}")

    results_df = pd.DataFrame(rows)
    results_df.to_csv(f"backend/results/eval_{label.lower()}.csv", index=False)

    return results_df


if __name__ == "__main__":
    #TF-IDF y BM25
    print("Evaluando TF-IDF...")
    evaluate_search(search_with_tfidf, label="TF-IDF")

    print("\nEvaluando BM25...")
    evaluate_search(search_with_bm25, label="BM25")
