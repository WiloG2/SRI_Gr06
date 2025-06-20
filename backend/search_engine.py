import pandas as pd
from rank_bm25 import BM25Okapi
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing import preprocess  # Usamos la función de preprocesado que ya tienes
from pathlib import Path


# Ruta del corpus limpio
BASE_DIR = Path(__file__).resolve().parent
CORPUS_PATH = BASE_DIR / "data" / "corpus_limpio.csv"
RAW_CORPUS_PATH = BASE_DIR / "data" / "corpus_raw.csv"

corpus_raw_df = pd.read_csv(RAW_CORPUS_PATH)
corpus_raw_df = corpus_raw_df.rename(columns={"_id": "id"})  # Para uniformidad, si es necesario
id_to_raw_text = dict(zip(corpus_raw_df["id"].astype(str), corpus_raw_df["text"]))


# Cargar el corpus limpio una vez y almacenarlo en memoria
def load_corpus():
    print("[INFO] Cargando corpus limpio...")
    corpus_df = pd.read_csv(CORPUS_PATH)  # Cargamos el corpus desde el CSV

    # Verificar si hay valores NaN en la columna 'text'
    if corpus_df['text'].isnull().any():
        print("[WARNING] El corpus contiene valores NaN en la columna 'text'. Los reemplazaremos por cadenas vacías.")
        corpus_df['text'] = corpus_df['text'].fillna('')  # Reemplazar NaN por cadena vacía
    
    return corpus_df

# Cargar el corpus en memoria al inicio
corpus_df = load_corpus()
corpus_clean = corpus_df['text'].tolist()  # Solo tomamos la columna 'text' para búsqueda

id_to_title = dict(zip(corpus_raw_df["id"].astype(str), corpus_raw_df["title"]))

# Crear el vectorizador TF-IDF y el índice BM25 una sola vez
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus_clean)  # Índice invertido de TF-IDF
print(tfidf_matrix)

# Tokenizamos el corpus para BM25
corpus_tokens = [doc.split() for doc in corpus_clean]  # Tokenización simple para BM25
bm25 = BM25Okapi(corpus_tokens)  # Índice de BM25

# Función de búsqueda con TF-IDF
def search_with_tfidf(query, top_n=5):
    
    # Preprocesar la consulta
    query_clean = preprocess(query)
    query_vector = vectorizer.transform([query_clean])

    # Calcular similitudes
    similarities = (tfidf_matrix * query_vector.T).toarray()

    # Obtener los índices de los documentos más similares
    ranked_indexes = similarities.flatten().argsort()[-top_n:][::-1]

    results = []
    for idx in ranked_indexes:
        doc_id = str(corpus_df.iloc[idx]["id"])
        title = id_to_title.get(doc_id, "[Título no encontrado]")
        raw_text = id_to_raw_text.get(doc_id, "[Texto original no encontrado]")
        results.append({"id": doc_id, "title": title, "text": raw_text})
    return results

# Función de búsqueda con BM25
def search_with_bm25(query, top_n=5):
    # Tokenizar la consulta
    query_tokens = query.split()

    # Obtener las puntuaciones BM25 para la consulta
    scores = bm25.get_scores(query_tokens)

    # Obtener los índices de los documentos más relevantes
    ranked_indexes = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]

    # Obtener los documentos más relevantes
    results = []
    for idx in ranked_indexes:
        doc_id = str(corpus_df.iloc[idx]["id"])
        title = id_to_title.get(doc_id, "[Título no encontrado]")
        raw_text = id_to_raw_text.get(doc_id, "[Texto original no encontrado]")
        results.append({"id": doc_id, "title": title, "text": raw_text})
    return results