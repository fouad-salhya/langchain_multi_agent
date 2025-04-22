# main.py
from reception_agent import ReceptionAgent
import os

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "agents"
}
    
def main():
    api_key = os.getenv("OPENAI_API_KEY")  
    reception_agent = ReceptionAgent(DB_CONFIG, api_key)
    reception_agent.start()

if __name__ == "__main__":
    main()
