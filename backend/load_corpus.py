#----------
import jsonlines
import pandas as pd
from tqdm import tqdm
from preprocessing import preprocess

# Rutas de archivo
CORPUS_RAW_PATH = "backend\data\corpus_raw.csv"
CORPUS_CLEAN_PATH = "backend\data\corpus_limpio.csv"


def load_corpus():
    # 1. Cargar el corpus desde el archivo corpus.jsonl usando jsonlines
    print("[INFO] Cargando corpus desde corpus.jsonl...")
    corpus = []
    with jsonlines.open('backend\data\corpus.jsonl') as reader:
        for obj in reader:
            corpus.append(obj)

    # Convertir el corpus a un DataFrame de pandas
    corpus_df = pd.DataFrame(corpus)

    # Verificar las primeras filas del corpus para comprobar las claves
    print(corpus_df.head())  # Imprime las primeras filas del DataFrame para inspeccionar las claves

    # 2. Preprocesar el corpus
    processed_docs = []
    ids = []

    print("[INFO] Procesando documentos...")
    for i, doc in tqdm(corpus_df.iterrows(), total=corpus_df.shape[0], desc="Preprocesando documentos"):
        # Acceder a las claves correctas
        raw_text = doc["text"]  # Acceder a la clave 'text'
        doc_id = doc["_id"]  # Usar "_id" como el ID del documento

        # Preprocesamos el texto
        clean_text = preprocess(raw_text)

        # Almacenamos el documento procesado
        processed_docs.append(clean_text)
        ids.append(doc_id)

    # Crear DataFrame con los documentos procesados
    processed_df = pd.DataFrame({
        "id": ids,
        "text": processed_docs
    })

    # Guardar el corpus original y el corpus limpio
    print(f"[INFO] Guardando corpus original en {CORPUS_RAW_PATH}...")
    corpus_df.to_csv(CORPUS_RAW_PATH, index=False)

    print(f"[INFO] Guardando corpus limpio en {CORPUS_CLEAN_PATH}...")
    processed_df.to_csv(CORPUS_CLEAN_PATH, index=False)

    print("[INFO] Corpus procesado y guardado correctamente.")

# Ejecutar la carga y procesamiento
load_corpus()