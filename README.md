# SRI2025 - Information Retrieval System

This project implements an Information Retrieval (IR) system using **TF-IDF** and **BM25** ranking models. It allows search queries over a document corpus, and evaluates results using standard IR metrics like **Precision**, **Recall**, and **MAP (Mean Average Precision)**.

---

## Project Structure
## Installation

### 1. Clone the repository

git clone https://github.com/WiloG2/SRI_Gr06.git
cd SRI_Gr06

### 2.Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

### 3.Create and activate a virtual environment
pip install -r requirements.txt

## Observations

If you can't download corpus.jsonl and queries.jsonl, this project used gaming corpus from Ir_datasets, you can download dataset from:

https://ir-datasets.com/beir.html#beir/climate-fever

## How to Run

On backend:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

On frontend:
npm install
npm run dev
Access at: http://localhost:5173/


