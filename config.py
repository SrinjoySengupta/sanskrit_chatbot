# app/config.py

import os

# Path to dataset CSV
DATA_PATH = os.path.join("data", "gita.csv")

# Path to FAISS index
INDEX_PATH = os.path.join("indexes", "gita.index")

# Embedding model to use
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Path to SQLite database
DB_PATH = os.path.join("indexes", "chatbot.db")

# Admin password for exporting KYC & chat logs
ADMIN_PASSWORD = "admin123"  # change this in production

# Number of top results to retrieve from FAISS
TOP_K = 3
