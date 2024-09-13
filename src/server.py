import socket
import pickle
import threading

class Server:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.clients = []
        self.game_state = {}

    def start(self):
        self.server.listen()
        print(f"Serveur démarré sur {self.host}:{self.port}")
        while True:
            conn, addr = self.server.accept()
            print(f"Nouvelle connexion de {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(conn,))
            client_thread.start()

    def handle_client(self, conn):
        self.clients.append(conn)
        player_id = len(self.clients)
        conn.send(pickle.dumps(player_id))
        
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                if not data:
                    break
                if data == "get":
                    conn.send(pickle.dumps(self.game_state))
                elif isinstance(data, dict) and "action" in data:
                    self.handle_action(data)
                    conn.send(pickle.dumps({"status": "ok"}))  # Envoyer une réponse simple
            except Exception as e:
                print(f"Erreur lors du traitement des données du client : {e}")
                break
        
        self.clients.remove(conn)
        conn.close()

    def handle_action(self, action):
        if action["action"] == "prop_interaction":
            prop_id = action["prop_id"]
            specific_action = action["specific_action"]
            self.game_state[prop_id] = specific_action
            
            if specific_action == "valve_activated":
                print(f"Valve {prop_id} a été activée!")
                # Ici, vous pouvez ajouter toute logique supplémentaire nécessaire
                # pour gérer l'activation de la valve au niveau du serveur
            
            # Diffuser l'état mis à jour à tous les clients
            self.broadcast(action)  # On envoie l'action complète au lieu de game_state

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(pickle.dumps(message))
            except Exception as e:
                print(f"Erreur lors de l'envoi au client : {e}")
                self.clients.remove(client)

if __name__ == "__main__":
    server = Server()
    server.start()