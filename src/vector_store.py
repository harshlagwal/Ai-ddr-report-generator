import chromadb
from langchain_community.vectorstores import Chroma
import os

class VectorStore:
    def __init__(self, embedding_model, persist_directory="data/chroma_db"):
        self.embedding_model = embedding_model
        self.persist_directory = persist_directory

    def create_store(self, documents):
        """
        Creates a ChromaDB vector store from local documents.
        """
        # Ensure directory exists
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)

        vector_db = Chroma.from_documents(
            documents=documents,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory
        )
        return vector_db

    def load_store(self):
        """
        Loads an existing ChromaDB vector store.
        """
        if os.path.exists(self.persist_directory):
            return Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embedding_model
            )
        return None

if __name__ == "__main__":
    from embeddings import EmbeddingModel
    emb = EmbeddingModel().get_embeddings()
    vs = VectorStore(emb)
    print("Vector storage initialized.")
