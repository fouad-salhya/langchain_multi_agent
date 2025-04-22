# database.py
import mysql.connector
from langchain.tools import StructuredTool
from typing import Tuple

def insert_history(user_input: str, agent_output: str) -> Tuple[bool, str]:
    """Enregistre l'interaction (question et réponse) dans MySQL."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="agents"
        )
        cursor = conn.cursor()
        query = "INSERT INTO history (input, output) VALUES (%s, %s)"
        cursor.execute(query, (user_input, agent_output))
        conn.commit()
        return (True, "✅ Enregistré avec succès")
    except mysql.connector.Error as e:
        return (False, f"❌ Erreur MySQL: {e.msg}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

store_chat_tool = StructuredTool.from_function(
    name="Stockage_DB",
    description="Enregistre les interactions en base de données MySQL",
    func=insert_history
)

def load_history(dummy_arg: str = "") -> Tuple[bool, list[Tuple[str, str]]]:
    """Charge l'historique depuis la table 'history'."""
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="agents"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT input, output FROM history")
        return (True, cursor.fetchall())
    except mysql.connector.Error as e:
        return (False, [])
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
# NOUVEAU TOOL AJOUTÉ
load_history_tool = StructuredTool.from_function(
    name="Chargement_DB",
    description="Charge l'historique des interactions depuis MySQL",
    func=load_history
)