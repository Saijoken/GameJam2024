import json
import socket
import asyncudp
import asyncio
from protocols import Protocols
from lobby import Lobby
#from game import Game
from datetime import datetime
import hashlib
import uuid


class Server:

    def __init__(self):
        self.SERVER = socket.gethostname()
        self.PORT = 5555
        self.server_ip = socket.gethostbyname(self.SERVER)
        self.udp_socket = None
        self.waiting_for_pair = None
        self.lobby = Lobby()
        self.running = True
        #self.game = Game()
        # Struct of self.clients dict : { clientSocket1: nickname1, clientSocket2: nickname2 ...}
        self.clients = {}
        # Struct of self.lobbies dict : { 'game_id1': [clientSocket1, clientSocket2], 'game_id2': [clientSocket1] ... }
        self.lobbies = {}
        # TODO implémenter la classe Rooms (ou juste une classe enum)
        # Struct of self.rooms : { 'room1': [riddle1, riddle2], 'room2': [riddle3]...}
        # Avec riddle classe directement implémentée dans le dico
        self.rooms = {}

    # Time function
    def time(self):
        return datetime.now().strftime("[%d/%m - %H:%M:%S]")

    # Timer function for the game


    ##########################################################################################
    # First connection client-server and client handling
    ##########################################################################################

    async def init_task(self):
        try:
            print("server_ip:", self.server_ip)
            #self.serverSocket.bind((self.server_ip, self.PORT))
            #self.serverSocket.listen(2)
            
            # Create UDP socket with asyncudp module
            self.udp_socket = await asyncudp.create_socket(local_addr=(self.SERVER, self.PORT))
            print(f"{self.time()} [SERVER ON]")
            
            while self.running:
                try:
                    #client, addr = self.serverSocket.accept()
                    #thread = threading.Thread(target=self.handle_client, args=(client, addr))
                    #thread.start()

                    # UDP doesn't use connections
                    data, addr = await self.udp_socket.recvfrom()
                    print("data, address:", data, addr)
                    # Create the first task (the debut of the game, handle_client)
                    # Now handle_client doesn't use connections anymore just data
                    asyncio.create_task(self.handle_client(data, addr))
                except Exception as e:
                    print(f"Erreur lors de la création de la tâche: {str(e)}")
        except Exception as e:
            print(f"Erreur dans init_connection: {str(e)}")
        finally:
            self.udp_socket.close()

    # Handle choice between play, credits, quit
    # If play then handle login/register
    # If login/register successful then handle joining or creating a lobby
    async def handle_client(self, data, addr, game_id=None):
        try:
                msg = json.loads(data.decode())
                # Menu : choose play, credits, settings or quit
                options = ["Play", "Credits", "Settings", "Quit"]
                await self.send_data(Protocols.Response.MENU, options, addr)
                choice = msg.get('data')
                # Switch/case to handle the choice
                if choice == "Credits":
                    self.send_data(Protocols.Response.CREDITS, "Credits", addr)
                elif choice == "Quit":
                    self.send_data(Protocols.Response.QUIT, "Quit", addr)
                    del self.clients[addr]
                elif choice == "Settings":
                    self.send_data(Protocols.Response.SETTINGS, "Settings", addr)
                elif choice == "Play":
                    # First register or login
                    auth_success = self.handle_auth(addr)
                    # Then choose register or login
                    if auth_success:
                        options = ["Create a lobby", "Join a lobby"]
                        await self.send_data(Protocols.Response.CREATE_JOIN, options, addr)
                        choice = await msg.get('data')
                        # Switch/case to handle the choice
                        if choice == "Create a lobby":
                            game_id = await self.create_lobby(addr)
                            if game_id and self.lobby.get_len(game_id) == 2:
                                await self.choose_role(addr)
                        else:
                            success = await self.join_lobby(addr)
                            if success and self.lobby.get_len(game_id) == 2:
                                await self.choose_role(addr)
        except Exception as e:
            print(str(e))


    # Choose between past and future before playing
    async def choose_role(self, addr):
        options = ["Past", "Future"]
        await self.send_data(Protocols.Response.CHOOSE_ROLE, options, addr)
        choice = await self.get_data(addr)
        return choice
        # Add in JSON game_id, addr clients, which choose past/future

    # Get a valid nickname
    async def get_valid_nickname(self, addr):
        while self.running:
            try:
                # Ask client for the nickname
                await self.send_data(Protocols.Response.NICKNAME, None, addr)
                msg = await self.get_data(addr)
                nickname = msg.get("data")
                # Check if nickname already exists
                if nickname in self.clients.values():
                    await self.send_data(Protocols.Response.NICKNAME_ERROR, "Nickname already taken", addr)
                else:
                    return nickname
            except Exception as e:
                print(str(e))


    # Create a lobby
    async def create_lobby(self, addr):
        # Create a game_id and add it as the id of the lobby
        game_id = self.generate_game_id()
        self.lobby.add_game(game_id, addr)
        # The client who creates the lobby is waiting for another connection
        self.waiting_for_pair = addr

        # Send game_id to the client
        await self.send_data(Protocols.Response.LOBBY_CREATED, {"game_id": game_id}, addr)
        # Wait for another player to join
        while self.lobby.get_len(game_id) < 2:
            await asyncio.sleep(1)
    
        return game_id
        # Créer un nouveau thread pour gérer la partie
        #game_thread = threading.Thread(target=self.handle_game, args=(game_id, player1, player2))
        #game_thread.start()


    # Join a lobby
    async def join_lobby(self, game_id, addr):
        # Ask the client for the game_id
        await self.send_data(Protocols.Response.REQUEST_GAME_ID, None, addr)
        msg = await self.get_data(addr)
        game_id = msg.get("data")
        if game_id in self.lobby.games:
            if self.lobby.get_len(game_id) == 1:
                await self.lobby.add_client_to_game(game_id, addr)
                await self.send_data(Protocols.Response.JOINED_LOBBY, {"game_id": game_id}, addr)
                return True
            else:
                await self.send_data(Protocols.Response.LOBBY_FULL, "Impossible de rejoindre le lobby", addr)
        else:
                await self.send_data(Protocols.Response.LOBBY_NOT_FOUND, "Lobby introuvable", addr)

    ##########################################################################################
    # Connection types handling (login, register...)
    ##########################################################################################

    # Handle authentification choice
    async def handle_auth(self, addr):
        print("Started handling authentification")
        options = ["Login", "Register", "Return"]
        await self.send_data(Protocols.Response.AUTH, options, addr)
        choice = await self.get_data(addr)
        # Switch/case on the choice
        if choice == "Login":
            return await self.handle_login(addr)
        elif choice == "Register":
            return await self.handle_register(addr)
        else:
            await self.send_data(Protocols.Response.RETURN, None, addr)
            return await self.handle_client(addr)

    # Login a client
    #TODO db->JSON
    async def handle_login(self, addr):
        # Ask the client for the login and password
        await self.send_data(Protocols.Response.LOGIN_REQUEST, "Entrez votre nom d'utilisateur et mot de passe", addr)
        msg = await self.get_data(addr)
        if msg.get("type") == Protocols.Request.LOGIN:
            nickname = await msg.get("data").get("nickname")
            password = await msg.get("data").get("password")
            
            #TODO json file
            if self.database.check_credentials(nickname, password):
                await self.send_data(Protocols.Response.LOGIN_SUCCESS, "Connexion réussie", addr)
                self.clients[addr] = nickname
                return True
            else:
                await self.send_data(Protocols.Response.LOGIN_FAILED, "Identifiants incorrects", addr)
                #TODO réessayer
                return False
        else:
            await self.send_data(Protocols.Response.LOGIN_FAILED, "Requête invalide", addr)
            return False

    # Logout a client
    #TODO db->json
    async def handle_logout(self, addr):
        if addr in self.clients:
            nickname = self.clients[addr]
            del self.clients[addr]
            await self.send_data(Protocols.Response.LOGOUT_SUCCESS, "Déconnexion réussie", addr)
            print(f"{self.time()} User {nickname} logged out")
            return True
        else:
            await self.send_data(Protocols.Response.LOGOUT_FAILED, "Utilisateur non connecté", addr)
            return False
    
    # Disconnect a client from the game
    async def handle_disconnect(self, addr, game_id):
        if game_id in self.lobby.games:
            if self.lobby.games[game_id][addr]:
                await self.lobby.remove_client_from_game(game_id, addr)
                await self.send_data(Protocols.Response.DISCONNECTED_SUCCESS, None, self.lobby.get_other_client(game_id, addr))
                del self.clients[addr]
            else:
                await self.send_data(Protocols.Response.DISCONNECTED_FAILED, "Utilisateur introuvable", addr)
        else:
            await self.send_data(Protocols.Response.LOBBY_NOT_FOUND, "Lobby introuvable", addr)


    # Register a client
    #TODO db->json
    async def handle_register(self, addr):
        await self.send_data(Protocols.Response.REGISTER_REQUEST, "Entrez un nickname et un mot de passe", addr)
        message = await self.get_data(addr)
        
        #TODO
        if isinstance(message, dict) and "nickname" in message and "password" in message:
            nickname = message["nickname"]
            password = message["password"]
            
            if self.database.user_exists(nickname):
                await self.send_data(Protocols.Response.REGISTER_FAILED, "Nickname déjà utilisé", addr)
                return False
            
            # Hachage du mot de passe avant stockage
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            if self.database.add_user(nickname, hashed_password):
                await self.send_data(Protocols.Response.REGISTER_SUCCESS, "Inscription réussie", addr)
                return True
            else:
                await self.send_data(Protocols.Response.REGISTER_FAILED, "Erreur lors de l'inscription", addr)
                #TODO réessayer
                return False
        else:
            await self.send_data(Protocols.Response.REGISTER_FAILED, "Requête invalide", addr)
            return False
        
        

    ##########################################################################################
    # Data handling (send, receive...)
    ##########################################################################################

    # Get the UDP datagram
    async def get_data(self, addr):
        data, recv_addr = await asyncio.wait_for(self.udp_socket.recvfrom())
        if recv_addr == addr:
            return json.loads(data.decode())
        
    # Send an info to one client/player
    async def send_data(self, r_type, data, addr):
        msg = {"type": r_type, "data": data}
        msg = json.dumps(msg).encode("ascii")
        self.udp_socket.sendto(msg, addr)

    # Create unique ID for a new room
    def generate_game_id(self):
        game_id = (str(uuid.uuid4())[:6])
        return game_id


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.init_task())