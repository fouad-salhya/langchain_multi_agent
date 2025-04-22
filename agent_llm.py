# agent_llm.py
import os
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool
from langchain.agents import AgentType, initialize_agent
from langchain_community.agent_toolkits.load_tools import load_tools
import warnings
from langchain_core._api.deprecation import LangChainDeprecationWarning  
from langchain.memory import ConversationBufferMemory 
from langchain.prompts import MessagesPlaceholder


# Ignorer l'avertissement de dépréciation
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

# Initialisation du modèle GPT-3.5 avec OpenAI
model = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Initialisation de SerpAPIWrapper (moteur de recherche web)
search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))

# Définition d'un Tool pour la recherche web
search_tool = Tool(
    name="Recherche_Web",
    description="Questions sur actualités, événements, ou connaissances générales",
    func=search.run,
)

# Chargement d'outils complémentaires
gpt3_tools = load_tools(["llm-math"], llm=model)
gpt3_tools.append(search_tool)


# Mémoire de conversation (Ajout)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

system_message = """Répondez toujours en français et en texte simple. 
                   Format interdit : JSON/XML/HTML."""
                   
# Initialisation de l'agent avec tous ces outils
gpt3agent = initialize_agent(
    tools=gpt3_tools,
    llm=model,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    system_message=system_message,
    handle_parsing_errors=True,
    return_intermediate_steps=False,
    memory=memory
)


def generate_answer(question: str) -> str:
    """Génère une réponse via l'agent LLM (fallback)"""
    try:
        # Exécute l'action et récupère le résultat final
        response = gpt3agent.run(input= question)
        return response
    except Exception as e:
        return f"Erreur : {str(e)}"
