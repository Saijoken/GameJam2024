import json
import asyncudp
import asyncio
from protocols import Protocols
from lobby import Lobby
#from game import Game
from datetime import datetime
import uuid
import traceback
from database import Database


class Server:

    def __init__(self):
        self.PORT = 5555
        #self.SERVER = socket.gethostname()
        #self.server_ip = socket.gethostbyname(self.SERVER)
        self.server_ip = "127.0.0.1"
        self.udp_socket = None
        self.waiting_for_pair = None
        self.lobby = Lobby()
        self.running = True
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
            
            # Create UDP socket with asyncudp module
            self.udp_socket = await asyncudp.create_socket(local_addr=(self.server_ip, self.PORT))
            print(f"{self.time()} [SERVER ON]")
            
            while self.running:
                try:
                    # UDP doesn't use connections
                    print(f"{self.time()} En attente de données")
                    data, addr = await self.udp_socket.recvfrom()
                    print(f"Reçu {data} de {addr}")
                    # Create the first task (the debut of the game, handle_client)
                    # Now handle_client doesn't use connections anymore just data
                    asyncio.create_task(self.handle_client(data, addr))
                except Exception as e:
                    print(f"Erreur lors de la création de la tâche: {str(e)}")
        except Exception as e:
            print(f"Erreur dans init_connection: {str(e)}")
        finally:
            if self.udp_socket:
                self.udp_socket.close()

    # Handle choice between play, credits, quit
    # If play then handle login/register
    # If login/register successful then handle joining or creating a lobby
    async def handle_client(self, data, addr, game_id=None):
        try:
            # Send menu to client
            options = ["Play", "Credits", "Settings", "Quit"]
            await self.send_data(Protocols.Response.MENU, options, addr)
            # Wait for the response
            await asyncio.sleep(0.1)
            response = await self.receive_data(addr)
            print(f"Client response: {response}")
            choice = response.get('type')
            if choice == Protocols.Request.WANT_TO_PLAY:
                auth_success = await self.handle_auth(addr)
                # Log pour voir si l'authentification est atteinte
                print(f"Authentication success: {auth_success}")
                if auth_success:
                    lobby_opt = ["Create a lobby", "Join a lobby"]
                    await self.send_data(Protocols.Response.CREATE_JOIN, lobby_opt, addr)
                    # Wait for the response
                    response = await self.receive_data(addr)
                    choice = response.get('type')
                    if choice == Protocols.Request.CREATE_LOBBY:
                        game_id = await self.create_lobby(addr)
                        if game_id and self.lobby.get_len(game_id) == 2:
                            await self.choose_role(addr)
                    elif choice == Protocols.Request.JOIN_LOBBY:
                        success = await self.join_lobby(addr)
                        if success and self.lobby.get_len(game_id) == 2:
                            await self.choose_role(addr)
            elif choice == Protocols.Request.CHOOSE_CREDITS:
                pass
            elif choice == Protocols.Request.CHOOSE_SETTINGS:
                pass
            else:
                #TODO Quit, close the client, close the socket? close the window
                pass
                #print(f"Unexpected request type: {response_type}")

        except Exception as e:
            print(f"Error in handle_client: {str(e)}")
            traceback.print_exc()




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
        print("Started handling authentication")
        auth_options = ["Login", "Register", "Return"]
        await self.send_data(Protocols.Response.AUTH, auth_options, addr)
    
        auth_choice = await self.receive_data(addr)
        auth_choice_type = auth_choice.get('type')
    
        if auth_choice_type == Protocols.Request.LOGIN:
            return await self.handle_login(addr)
        elif auth_choice_type == Protocols.Request.REGISTER:
            return await self.handle_register(addr)
        else:
            await self.send_data(Protocols.Response.RETURN, None, addr)
            return False

    # Login a client
    async def handle_login(self, addr):
        # Ask the client for the login and password
        await self.send_data(Protocols.Response.LOGIN_REQUEST, "Entrez votre nom d'utilisateur et mot de passe", addr)
        msg = await self.receive_data(addr)
        if msg.get('type') == Protocols.Request.LOGIN:
            nickname = await msg.get('data').get('nickname')
            password = await msg.get('data').get('password')
            
            if self.database.exist_nickname(nickname):
                if self.database.check_password(nickname, password):
                    await self.send_data(Protocols.Response.LOGIN_SUCCESS, "Connexion réussie", addr)
                    self.clients[addr] = nickname
                    return True
                else:
                    await self.send_data(Protocols.Response.LOGIN_FAILED, "Identifiants incorrects", addr)
                    #TODO réessayer
                    return False
            else:
                await self.send_data(Protocols.Response.LOGIN_FAILED, "Identifiants incorrects", addr)
                #TODO réessayer
                return False
        else:
            await self.send_data(Protocols.Response.LOGIN_FAILED, "Requête invalide", addr)
            return False

    # Logout a client
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
    async def handle_register(self, addr):
        await self.send_data(Protocols.Response.REGISTER_REQUEST, "Entrez un nickname et un mot de passe", addr)
        msg = await self.get_data(addr)
        # Check if nickname and password exist, are coherent and correct
        data = msg.get('data')
        nickname = data["nickname"]
        password = data["password"]
        if self.database.exist_nickname(nickname):
            await self.send_data(Protocols.Response.REGISTER_FAILED, "Nickname déjà utilisé", addr)
            #TODO réessayer
            return False
        self.database.add_user(nickname, password)
        await self.send_data(Protocols.Response.REGISTER_SUCCESS, "Inscription réussie", addr)
        return True
        
        

    ##########################################################################################
    # Data handling (send, receive...)
    ##########################################################################################

    # Receive the info/response from client
    # And decode it at the same time
    async def receive_data(self, addr):
        rcv_data, rcv_addr = await asyncio.wait_for(self.udp_socket.recvfrom(), timeout=30)
        if rcv_addr == addr:
            return json.loads(rcv_data.decode())
        else:
            print(f"Received response from unexpected address: {rcv_addr}")
            return False
        
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