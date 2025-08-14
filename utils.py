# app/utils.py
"""
Utility functions for embeddings, FAISS index, and searching.
"""

import os
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Dict

from app.config import (
    DATA_PATH,
    INDEX_PATH,
    EMBEDDING_MODEL,
    TOP_K,
)

# ---------------------------
# Load embedding model once
# ---------------------------
_model = SentenceTransformer(EMBEDDING_MODEL)


def load_dataset() -> pd.DataFrame:
    """
    Load the Bhagavad Gita dataset.
    Expected columns: 'sanskrit', 'english'
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    # Basic cleanup
    df.columns = [c.strip().lower() for c in df.columns]
    if "sanskrit" not in df.columns or "english" not in df.columns:
        raise ValueError("Dataset must have 'sanskrit' and 'english' columns.")
    df = df.dropna(subset=["sanskrit", "english"]).reset_index(drop=True)
    return df


def embed_sentences(sentences: List[str]) -> np.ndarray:
    """
    Embed a list of sentences into a numpy array (float32).
    """
    embeddings = _model.encode(sentences, convert_to_numpy=True, show_progress_bar=False)
    return embeddings.astype("float32")


def build_faiss_index(sentences: List[str]) -> faiss.IndexFlatL2:
    """
    Build a FAISS L2 index from given sentences.
    """
    embeddings = embed_sentences(sentences)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


def save_index(index: faiss.IndexFlatL2, path: str):
    faiss.write_index(index, path)


def load_index(path: str) -> faiss.IndexFlatL2:
    if not os.path.exists(path):
        raise FileNotFoundError(f"FAISS index not found at {path}")
    return faiss.read_index(path)


def semantic_search(query: str, df: pd.DataFrame, index: faiss.IndexFlatL2, top_k: int = TOP_K) -> List[Tuple[str, str, float]]:
    """
    Search for the top_k most similar Sanskrit or English lines given a query.
    Returns a list of tuples: (sanskrit, english, score)
    """
    q_emb = embed_sentences([query])
    D, I = index.search(q_emb, top_k)
    results = []
    for idx, dist in zip(I[0], D[0]):
        if 0 <= idx < len(df):
            sanskrit_line = df.iloc[idx]["sanskrit"]
            english_line = df.iloc[idx]["english"]
            score = float(dist)
            results.append((sanskrit_line, english_line, score))
    return results


def format_results(results: List[Tuple[str, str, float]]) -> str:
    """
    Format results into a readable string for display in the chatbot.
    """
    lines = []
    for i, (sanskrit, english, score) in enumerate(results, 1):
        lines.append(f"**{i}. Sanskrit:** {sanskrit}\n**   English:** {english}")
    return "\n\n".join(lines)
