# socket_server.py
import socket
import threading
from reception_agent import ReceptionAgent
import os

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "agents"
}

class SocketServer:
    def __init__(self, host='0.0.0.0', port=8000):
        self.host = host
        self.port = port
        self.reception_agent = ReceptionAgent(DB_CONFIG, os.getenv("OPENAI_API_KEY"))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def handle_client(self, conn, addr):
        print(f"🔌 Connexion établie avec {addr}")
        try:
            while True:
                data = conn.recv(1024).decode('utf-8').strip()
                if not data:
                    break
                
                # Traitement par l'agent
                response = self.reception_agent.handle_query(data)
                conn.sendall(f"Assistant: {response}\n".encode('utf-8'))
                
        finally:
            conn.close()

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"🚀 Serveur socket démarré sur {self.host}:{self.port}")
        while True:
            conn, addr = self.sock.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    server = SocketServer()
    server.start()