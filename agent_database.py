# agent_database.py
from database import store_chat_tool, load_history_tool
from typing import Dict, Any

class DatabaseAgent:
    """Agent dédié à l'enregistrement des interactions dans la base de données."""
    def store_interaction(self, user_input: str, agent_output: str) -> Dict[str, Any]:
        try:
            result = store_chat_tool.run({
                "user_input": user_input,
                "agent_output": agent_output
            })
            return {"status": "success", "message": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    def load_historical_data(self) -> list[tuple[str, str]]:
        """Charge l'historique via le tool LangChain."""
        result = load_history_tool.run("")  # Étape 1 : Récupérer le tuple
        success, data = result              # Étape 2 : Déstructurer
        return data if success else []
