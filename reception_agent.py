# reception_agent.py
import mysql.connector
from agent_semantic import SemanticAgent
from agent_llm import generate_answer
from agent_database import DatabaseAgent

class ReceptionAgent:
    """Agent d'accueil qui gère la logique de recherche et de fallback."""
    def __init__(self, db_config, api_key):
        self.db_config = db_config
        self.api_key = api_key
        # history = load_history()
        
        self.database_agent = DatabaseAgent()
        history = self.database_agent.load_historical_data()  
        self.semantic_agent = SemanticAgent(history, api_key).get_tool()
        # self.database_agent = DatabaseAgent()
        self.conversation_context = []  # <-- Ajout mémoire session
        
    # Ajouter cette méthode à la classe ReceptionAgent
    def process_message(self, message: str) -> str:
        return self.handle_query(message)

    def handle_query(self, query: str) -> str:
        # D'abord, recherche sémantique dans la base
        response = self.semantic_agent.func(query)
        if response == "Aucune réponse trouvée":
            # Si rien n'est trouvé, utiliser le LLM (fallback)
            # Ajout du contexte à la requête
            full_query = "\n".join(self.conversation_context + [f"Dernière question: {query}"])
            response = generate_answer(full_query)
        # Enregistrer l'interaction dans la base
        self.database_agent.store_interaction(query, response)
        return response

    def start(self):
        print("🔍 Service Client Intelligent - Tapez 'exit' pour quitter\n")
        while True:
            try:
                user_input = input("Client : ").strip()
                if user_input.lower() in ['exit', 'quit']:
                    print("👋 Fin de la session.")
                    self.conversation_context = []  # Reset mémoire
                    break
                
                   # Construction du contexte complet
                self.conversation_context.append(f"Client: {user_input}")
                result = self.handle_query(user_input)
                self.conversation_context.append(f"Assistant: {result}")
                   
                # result = self.handle_query(user_input)
                print(f"\nAssistant : {result}\n")
            except KeyboardInterrupt:
                print("\n👋 Session interrompue.")
                break
