from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from search_engine import search_with_tfidf, search_with_bm25

app = FastAPI()

# Habilitar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O especifica tu frontend (ej: ["http://localhost:5173"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para recibir la consulta y el modelo de búsqueda (tfidf o bm25)
class QueryRequest(BaseModel):
    query: str
    model: str  # "tfidf" o "bm25"

@app.post("/search")
async def search_endpoint(request: QueryRequest):
    query = request.query
    model = request.model

    # Llamada a las funciones de búsqueda basadas en el modelo
    if model == "tfidf":
        results = search_with_tfidf(query)  # Función optimizada para TF-IDF
    elif model == "bm25":
        results = search_with_bm25(query)  # Función optimizada para BM25
    else:
        raise HTTPException(status_code=400, detail="Modelo no soportado. Usa 'tfidf' o 'bm25'.")

    # Retornar solo los primeros 5 resultados (si hay más de 5)
    return {"results": results[:5]}  # Limitar a los primeros 5 resultados
