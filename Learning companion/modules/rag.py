import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import Config
from modules.utils import clean_text


class RAGEngine:
    def __init__(self, kb_path="data/knowledge_base"):
        """
        Retrieval-Augmented Generation (RAG) engine.
        Loads knowledge base, builds embeddings, and enables semantic search.
        """
        self.kb_path = kb_path
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.index = None
        self.chunks = []
        self._build_index()

    def _build_index(self):
        """Load knowledge base JSON files and build FAISS index."""
        all_chunks = []

        if not os.path.exists(self.kb_path):
            raise FileNotFoundError(f"Knowledge base path not found: {self.kb_path}")

        for file in os.listdir(self.kb_path):
            if file.endswith(".json"):
                file_path = os.path.join(self.kb_path, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        raw_data = json.load(f)

                        if not isinstance(raw_data, list):
                            raise ValueError(f"File {file} must contain a JSON array of strings.")

                        for entry in raw_data:
                            if isinstance(entry, str):
                                all_chunks.append(clean_text(entry))
                            else:
                                print(f"⚠️ Skipping non-string entry in {file}: {entry}")

                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing error in {file_path}: {e}")
                except Exception as e:
                    print(f"❌ Error reading {file_path}: {e}")

        if not all_chunks:
            raise ValueError("No valid knowledge chunks found in knowledge base.")

        self.chunks = all_chunks

        # Build embeddings
        embeddings = self.model.encode(all_chunks, convert_to_numpy=True, show_progress_bar=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def retrieve(self, query, top_k=Config.TOP_K):
        """
        Retrieve top_k most relevant knowledge chunks for a given query.
        """
        if not self.index:
            raise RuntimeError("FAISS index has not been built.")

        q_emb = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(q_emb, top_k)

        results = []
        for i in indices[0]:
            if 0 <= i < len(self.chunks):
                results.append(self.chunks[i])

        return results
