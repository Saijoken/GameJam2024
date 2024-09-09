import json
import socket
import threading
from datetime import datetime
# Pour le chrono du jeu, côté serveur afin de synchroniser le timer de chaque client
from protocols import Protocols
from lobby import Lobby
import uuid
from database import Database


class Server:

    # Initialize server and port
    SERVER = socket.gethostname()
    PORT = 5555
    # Create socket and initialize connection type
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = socket.gethostbyname(SERVER)

    def __init__(self):
        self.waiting_for_pair = None
        self.lobby = Lobby()
        self.running = True
        self.database = Database()
        self.database.create()
        self.clients = { }
        self.lobbies = { }

    # Time function
    def time(self):
        return datetime.now().strftime("[%d/%m - %H:%M:%S]")

    # Timer function for the game

    def init_connection(self):
        try:
            # Bind port to server and handle binding error
            try:
                self.serverSocket.bind((self.server_ip, self.PORT))
            except socket.error as e:
                print(str(e))
            print(f"{self.time()} [SERVER ON]")
            # Listen port and accept connections from client
            # Maximum of 2 connections since it's a two-player game
            self.serverSocket.listen(2)
            while self.running:
                try:
                    client, addr = self.serverSocket.accept()
                    print("Connexion acceptée")
                    thread = threading.Thread(target=self.handle_client(client, addr), args=(client, addr))
                    print("Thread créé:", thread)
                    thread.start()
                except Exception as e:
                    print(str(e))
        except Exception as e:
            print(str(e))


    # Handle hosting or joining a room
    def handle_client(self, client, addr, game_id=None):
        while self.running:
            self.send_data(Protocols.Response.NICKNAME, None, client)
            message = json.loads(client.recv(1024).decode("ascii"))
            r_type = message.get("type")
            nickname = self.get_valid_nickname(client)
            # If nickname is valid, add the client to the list of clients for the server & lobby
            if r_type == Protocols.Request.NICKNAME:
                self.clients[client] = nickname
            else:
                continue
            # If game_id doesn't exist yet, the first player creates the lobby
            if not game_id and len(self.clients) == 1:
                self.create_lobby(client)
            # Else the client can join an existing lobby
            else:
                self.join_lobby(game_id, client)

    # Create a lobby
    def create_lobby(self, client):
        # Create a game_id and add it as the id of the lobby
        game_id = self.host()
        self.lobby.add_game(game_id, client)
        # The client who creates the lobby is waiting for another connection
        self.waiting_for_pair = client

        # Envoyer un message au client pour les informer qu'il a créé un lobby
        self.send_data(Protocols.Response.LOBBY_CREATED, {"game_id": game_id}, client)

        # Créer un nouveau thread pour gérer la partie
        #game_thread = threading.Thread(target=self.handle_game, args=(game_id, player1, player2))
        #game_thread.start()

    # Join a lobby
    def join_lobby(self, game_id, client):
        if game_id in self.lobby.games:
            if self.lobby.start_game(game_id):
                return "Erreur: le jeu a déjà commencé"
            else:
                if self.lobby.get_len(game_id) == 1:
                    self.lobby.add_client_to_game(game_id, client)
                    self.lobby.start_game(game_id)
                else:
                    return "Erreur: le lobby est complet"
        else:
            return "Erreur: ce lobby n'existe pas"

    # Get the data (for save/load, updates in the game)
    def get_data(self, client, bytes):
        data = client.recv(bytes)
        data = json.loads(data.decode("ascii"))
        return data

    # Send an info to one client/player
    def send_data(self, r_type, data, client):
        message = {"type": r_type, "data": data}
        message = json.dumps(message).encode("ascii")
        client.send(message)

    # Create unique ID for a new room
    def host(self):
        game_id = (str(uuid.uuid4())[:6])
        return game_id

    # Fonction pour handle le login
    # Fonction pour handle le logout/la déconnexion


    def receive_data(self):
        while True:
            client, address = self.serverSocket.accept()
            print(f"Connected with {str(address)}")
            thread = threading.Thread(target=self.handle_client, args=(client, address))
            thread.start()


    def get_valid_nickname(self, client):
        while self.running:
            try:
                # Demander le pseudo au client
                self.send_data(Protocols.Response.NICKNAME, None, client)
                message = json.loads(client.recv(1024).decode("ascii"))
                nickname = message.get("data")
                # Vérifier si le pseudo est déjà pris
                if nickname in self.clients.values():
                    self.send_data(Protocols.Response.NICKNAME_ERROR, "Nickname already taken", client)
                else:
                    return nickname
            except Exception as e:
                print(str(e))


if __name__ == "__main__":
    s = Server()
    t1 = threading.Thread(target=s.init_connection())
    t1.start()
