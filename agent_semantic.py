# agent_semantic.py
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain.tools import Tool


class SemanticAgent:
    def __init__(self, database, api_key, threshold=0.82):
        """
        database: liste de tuples (input, output) provenant de MySQL.
        """
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=api_key
        )
        self.threshold = threshold
        self.questions = [q for q, _ in database]
        self.responses = [r for _, r in database]
        # Pré-calcul des embeddings pour toutes les questions en base
        self.question_embeddings = self.embeddings.embed_documents(self.questions)

    def _cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def search(self, query: str) -> str:
        """Recherche la question la plus similaire et retourne la réponse associée."""
        query_embedding = self.embeddings.embed_query(query)
        similarities = [self._cosine_similarity(query_embedding, emb) for emb in self.question_embeddings]
        max_idx = int(np.argmax(similarities))
        if similarities[max_idx] > self.threshold:
            return self.responses[max_idx]
        return "Aucune réponse trouvée"
    
    def get_tool(self):
        """Retourne un outil LangChain basé sur cet agent."""
        return Tool(
            name="Recherche Sémantique",
            func=self.search,
            description="Recherche la question la plus proche dans une base de données et retourne la réponse associée."
        )
