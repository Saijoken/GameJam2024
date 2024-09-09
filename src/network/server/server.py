import json
import socket
import threading
from datetime import datetime
import hashlib
from protocols import Protocols
from lobby import Lobby
import uuid
from database import Database

class Server:

    def __init__(self):
        self.SERVER = socket.gethostname()
        self.PORT = 5555
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Make the serverSocket non blocking
        self.serverSocket.setblocking(False)
        # Dynamic listening
        self.server_ip = ''
        self.waiting_for_pair = None
        self.lobby = Lobby()
        self.running = True
        self.database = Database()
        self.database.create()
        self.clients = {}
        self.lobbies = {}

    # Time function
    def time(self):
        return datetime.now().strftime("[%d/%m - %H:%M:%S]")

    # Timer function for the game


    ##########################################################################################
    # First connection client-server and client handling
    ##########################################################################################

    def init_connection(self):
        try:
            print("server_ip:", self.server_ip)
            self.serverSocket.bind((self.server_ip, self.PORT))
            self.serverSocket.listen(2)
            print(f"{self.time()} [SERVER ON]")
            
            while self.running:
                try:
                    client, addr = self.serverSocket.accept()
                    print(f"Connexion acceptée de {addr}")
                    thread = threading.Thread(target=self.handle_client, args=(client, addr))
                    thread.start()
                except Exception as e:
                    print(f"Erreur lors de l'acceptation de la connexion: {str(e)}")
        except Exception as e:
            print(str(e))
        finally:
            self.serverSocket.close()

    # Handle choice between play, credits, quit
    # If play then handle login/register
    # If login/register successful then handle joining or creating a lobby
    def handle_client(self, client, addr, game_id=None):
        try:
            while self.running:
                # Menu : choose play or credits or quit
                self.send_menu_options(client)
                choice = self.receive_menu_choice(client)
                # Switch/case to handle the choice
                if choice == "Credits":
                    self.send_data(Protocols.Response.CREDITS, "Credits", client)
                elif choice == "Quit":
                    self.send_data(Protocols.Response.QUIT, "Quit", client)
                    # Make sure to close everything
                    self.serverSocket.close()
                elif choice == "Play":
                    # First register or login
                    self.handle_auth(client)
                    # Then choose register or login
                    if self.handle_auth(client):
                        if not game_id and len(self.clients) == 1:
                            self.create_lobby(client)
                        else:
                            self.join_lobby(game_id, client)
        except Exception as e:
            print(str(e))
        finally:
            if client in self.clients:
                del self.clients[client]
            client.close()

    # Get a valid nickname
    def get_valid_nickname(self, client):
        while self.running:
            try:
                # Ask client for the nickname
                self.send_data(Protocols.Response.NICKNAME, None, client)
                message = json.loads(client.recv(1024).decode("ascii"))
                nickname = message.get("data")
                # Check if nickname already exists
                #TODO reload an existing game if the nickname already exists
                if nickname in self.clients.values():
                    self.send_data(Protocols.Response.NICKNAME_ERROR, "Nickname already taken", client)
                else:
                    return nickname
            except Exception as e:
                print(str(e))


    # Create a lobby
    def create_lobby(self, client):
        # Create a game_id and add it as the id of the lobby
        game_id = self.generate_game_id()
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
        # Ask the client for the game_id
        self.send_data(Protocols.Response.REQUEST_GAME_ID, None, client)
        message = json.loads(client.recv(1024).decode("ascii"))
        game_id = message.get("data")
        if game_id in self.lobby.games:
            if self.lobby.start_game(game_id):
                self.send_data(Protocols.Response.LOBBY_FULL, "Le jeu a déjà commencé", client)
            else:
                if self.lobby.get_len(game_id) == 1:
                    self.lobby.add_client_to_game(game_id, client)
                    self.send_data(Protocols.Response.JOINED_LOBBY, {"game_id": game_id}, client)
                    self.lobby.start_game(game_id)
                    # Start the game thread
                else:
                    self.send_data(Protocols.Response.LOBBY_FULL, "Impossible de rejoindre le lobby", client)
        else:
            self.send_data(Protocols.Response.LOBBY_NOT_FOUND, "Lobby introuvable", client)


    ##########################################################################################
    # Connection types handling (login, register...)
    ##########################################################################################

    # Handle authentification choice
    def handle_auth(self, client):
        self.send_data(Protocols.Response.AUTH, ["Login", "Register", "Quit"], client)
        choice = self.get_data(client)
        # Switch/case on the choice
        if choice == "Login":
            return self.handle_login(client)
        elif choice == "Register":
            return self.handle_register(client)
        else:
            self.send_data(Protocols.Response.QUIT, None, client)

    # Login a client
    def handle_login(self, client):
        # Ask the client for the login and password
        self.send_data(Protocols.Response.LOGIN_REQUEST, "Entrez votre nom d'utilisateur et mot de passe", client)
        message = json.loads(client.recv(1024).decode("ascii"))
        if message.get("type") == Protocols.Request.LOGIN:
            nickname = message.get("data").get("nickname")
            password = message.get("data").get("password")
            
            # Check if it matches with the database (à remplacer par une vérification dans la base de données)
            if self.database.check_credentials(nickname, password):
                self.send_data(Protocols.Response.LOGIN_SUCCESS, "Connexion réussie", client)
                self.clients[client] = nickname
                return True
            else:
                self.send_data(Protocols.Response.LOGIN_FAILED, "Identifiants incorrects", client)
                return False
        else:
            self.send_data(Protocols.Response.LOGIN_FAILED, "Requête invalide", client)
            return False

    # Logout a client
    def handle_logout(self, client):
        if client in self.clients:
            nickname = self.clients[client]
            del self.clients[client]
            self.send_data(Protocols.Response.LOGOUT_SUCCESS, "Déconnexion réussie", client)
            print(f"{self.time()} User {nickname} logged out")
            return True
        else:
            self.send_data(Protocols.Response.LOGOUT_FAILED, "Utilisateur non connecté", client)
            return False
    
    # Disconnect a client from the game
    def handle_disconnect(self, client, game_id):
        if game_id in self.lobby.games:
            if self.lobby.games[game_id][client]:
                self.lobby.remove_client_from_game(game_id, client)
                self.send_data(Protocols.Response.DISCONNECTED_SUCCESS, None, self.lobby.get_other_client(game_id, client))
                del self.clients[client]
                #print(f"{self.time()} User {nickname} disconnected from game {game_id}")
            else:
                self.send_data(Protocols.Response.DISCONNECTED_FAILED, "Utilisateur introuvable", client)
        else:
            self.send_data(Protocols.Response.LOBBY_NOT_FOUND, "Lobby introuvable", client)


    # Register a client
    def handle_register(self, client):
        self.send_data(Protocols.Response.REGISTER_REQUEST, "Entrez un nickname et un mot de passe", client)
        message = json.loads(client.recv(1024).decode("ascii"))
        
        if message.get("type") == Protocols.Request.REGISTER:
            nickname = message.get("data").get("nickname")
            password = message.get("data").get("password")
            
            if self.database.user_exists(nickname):
                self.send_data(Protocols.Response.REGISTER_FAILED, "Nickname déjà utilisé", client)
                return False
            
            # Hachage du mot de passe avant stockage
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            if self.database.add_user(nickname, hashed_password):
                self.send_data(Protocols.Response.REGISTER_SUCCESS, "Inscription réussie", client)
                print(f"{self.time()} New user registered: {nickname}")
                return True
            else:
                self.send_data(Protocols.Response.REGISTER_FAILED, "Erreur lors de l'inscription", client)
                return False
        else:
            self.send_data(Protocols.Response.REGISTER_FAILED, "Requête invalide", client)
            return False


    ##########################################################################################
    # Data handling (send, receive...)
    ##########################################################################################

    # Get the data (for save/load, updates in the game)
    def get_data(self, client):
        data = client.recv(1024).decode("ascii")
        data = json.loads(data).get("data")
        return data

    # Send an info to one client/player
    def send_data(self, r_type, data, client):
        message = {"type": r_type, "data": data}
        message = json.dumps(message).encode("ascii")
        client.send(message)

    # Create unique ID for a new room
    def generate_game_id(self):
        game_id = (str(uuid.uuid4())[:6])
        return game_id


if __name__ == "__main__":
    s = Server()
    s.init_connection()
