# app/build_index.py
"""
One-time script to build FAISS index from Bhagavad Gita dataset.
Run: python app/build_index.py
"""

import os
from app.utils import load_dataset, build_faiss_index, save_index
from app.config import DATA_PATH, INDEX_PATH

def main():
    print(f"Loading dataset from {DATA_PATH}...")
    df = load_dataset()
    print(f"Loaded {len(df)} rows.")

    print("Building FAISS index...")
    index = build_faiss_index(df["sanskrit"].tolist())

    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)

    print(f"Saving index to {INDEX_PATH}...")
    save_index(index, INDEX_PATH)

    print("✅ FAISS index built and saved successfully.")

if __name__ == "__main__":
    main()
