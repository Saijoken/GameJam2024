import json
import asyncudp
import asyncio
from protocols import Protocols
from lobby import Lobby
from datetime import datetime
import uuid
import traceback
import database


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
        
        print(f"{self.time()} [SERVER] Initialized")

    # Time function
    def time(self):
        return datetime.now().strftime("[%d/%m - %H:%M:%S]")


    ##########################################################################################
    # First connection client-server and client handling
    ##########################################################################################

    async def init_task(self):
        while self.running:
            try:
                print(f"{self.time()} [SERVER] Starting initialization")
                print(f"{self.time()} [SERVER] server_ip: {self.server_ip}")
                
                # Create UDP socket with asyncudp module
                self.udp_socket = await asyncudp.create_socket(local_addr=(self.server_ip, self.PORT))
                print(f"{self.time()} [SERVER ON] Listening on {self.server_ip}:{self.PORT}")
                
                while self.running:
                    try:
                        print(f"{self.time()} [SERVER] Waiting for data...")
                        data, addr = await self.udp_socket.recvfrom()
                        print(f"{self.time()} [SERVER] Received {data} from {addr}")
                        asyncio.create_task(self.handle_client(data, addr))
                    except asyncudp.ClosedError:
                        print(f"{self.time()} [WARNING] UDP socket closed unexpectedly. Reopening...")
                        break  # Break the inner loop to recreate the socket
                    except Exception as e:
                        print(f"{self.time()} [ERROR] Error handling client: {str(e)}")
                        traceback.print_exc()
            except Exception as e:
                print(f"{self.time()} [ERROR] Error in init_task: {str(e)}")
                traceback.print_exc()
            finally:
                if self.udp_socket:
                    self.udp_socket.close()
                    print(f"{self.time()} [SERVER] Socket closed")
            
            # Wait before attempting to recreate the socket
            await asyncio.sleep(5)

    # Handle choice between play, credits, quit
    # If play then handle login/register
    # If login/register successful then handle joining or creating a lobby
    async def handle_client(self, data, addr, game_id=None):
        try:
            print(f"{self.time()} [SERVER] Handling client {addr}")
            
            decoded_data = json.loads(data.decode())
            print("Données décodées:", decoded_data)
            message_type = decoded_data.get('type')
            message_data = decoded_data.get('data')
            
            if message_type == Protocols.Request.BROADCAST:
                await self.broadcast_message(message_data)
                return  # Ajoutez cette ligne pour sortir de la fonction après le broadcast
            
            # Send menu to client
            options = ["Play", "Credits", "Settings", "Quit"]
            await self.send_data(Protocols.Response.MENU, options, addr)
            print(f"{self.time()} [SERVER] Sent menu options to {addr}")
            # Wait for the response
            await asyncio.sleep(0.1)
            response = await self.receive_data(addr)
            print(f"{self.time()} [SERVER] Received response from {addr}: {response}")
            choice = response.get('type')
            if choice == Protocols.Request.WANT_TO_PLAY:
                auth_success = await self.handle_auth(addr)
                # Log pour voir si l'authentification est atteinte
                print(f"{self.time()} [SERVER] Authentication success: {auth_success}")
                if auth_success:
                    lobby_opt = ["Create a lobby", "Join a lobby"]
                    await self.send_data(Protocols.Response.CREATE_JOIN, lobby_opt, addr)
                    # Wait for the response
                    response = await self.receive_data(addr)
                    choice = response.get('type')
                    if choice == Protocols.Request.CREATE_LOBBY:
                        game_id = await self.create_lobby(addr)
                        if game_id and self.lobby.get_len(game_id) == 2:
                            await self.choose_role(addr, game_id)
                    elif choice == Protocols.Request.JOIN_LOBBY:
                        success = await self.join_lobby(addr)
                        if success and self.lobby.get_len(game_id) == 2:
                            await self.choose_role(addr, game_id)
            elif choice == Protocols.Request.CHOOSE_CREDITS:
                # As it is static and doesn't require a response
                # We can pass, it is handled by the client
                pass
            elif choice == Protocols.Request.CHOOSE_SETTINGS:
                pass
            else:
                self.udp_socket.close()
        except Exception as e:
            print(f"{self.time()} [ERROR] Error in handle_client: {str(e)}")
            traceback.print_exc()

    # Choose between past and future before playing
    async def choose_role(self, addr, game_id):
        print(f"{self.time()} [SERVER] Role selection for {addr} in game {game_id}")
        options = ["Past", "Future"]
        await self.send_data(Protocols.Response.CHOOSE_ROLE, options, addr)
        choice = await self.receive_data(addr)
        nickname = self.clients[addr]
        with open('src/network/server/infos.json', 'r') as f:
            data = json.load(f)
        data[game_id][nickname]['role'] = choice
        with open('src/network/server/infos.json', 'w') as f:
            json.dump(data, f, indent=4)
        print(f"{self.time()} [SERVER] Role {choice} chosen by {nickname} in game {game_id}")
        return choice

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
        game_id = self.generate_game_id()
        print(f"{self.time()} [SERVER] Creating lobby with game_id: {game_id} for {addr}")
        self.lobby.add_game(game_id, addr)
        # The client who creates the lobby is waiting for another connection
        self.waiting_for_pair = addr

        # Send game_id to the client
        await self.send_data(Protocols.Response.LOBBY_CREATED, {"game_id": game_id}, addr)
        print(f"{self.time()} [SERVER] Lobby {game_id} created, waiting for players...")
        while self.lobby.get_len(game_id) < 2:
            await asyncio.sleep(1)
        print(f"{self.time()} [SERVER] Lobby {game_id} is full")
        return game_id


    # Join a lobby
    async def join_lobby(self, game_id, addr):
        print(f"{self.time()} [SERVER] {addr} attempting to join lobby")
        # Ask the client for the game_id
        await self.send_data(Protocols.Response.REQUEST_GAME_ID, None, addr)
        msg = await self.get_data(addr)
        game_id = msg.get("data")
        if game_id in self.lobby.games:
            if self.lobby.get_len(game_id) == 1:
                await self.lobby.add_client_to_game(game_id, addr)
                print(f"{self.time()} [SERVER] {addr} joined lobby {game_id}")
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
        print(f"{self.time()} [SERVER] Handling authentication for {addr}")
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
    async def handle_login(self, addr, data):
        try:
            print(f"{self.time()} [SERVER] Handling login for {addr}")
            counter = 3
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
                        while counter > 0:
                            await self.handle_login(addr)
                            counter -= 1
                            if counter == 0:
                                return False
                else:
                    await self.send_data(Protocols.Response.LOGIN_FAILED, "Identifiants incorrects", addr)
                    while counter > 0:
                        await self.handle_login(addr)
                        counter -= 1
                        if counter == 0:
                            return False
            else:
                await self.send_data(Protocols.Response.LOGIN_FAILED, "Requête invalide", addr)
                return False
        except Exception as e:
            print(f"[ERROR] Error handling login: {str(e)}")
            import traceback
            traceback.print_exc()

    # Logout a client
    async def handle_logout(self, addr):
        print(f"{self.time()} [SERVER] Handling logout for {addr}")
        if addr in self.clients:
            nickname = self.clients[addr]
            del self.clients[addr]
            await self.send_data(Protocols.Response.LOGOUT_SUCCESS, "Déconnexion réussie", addr)
            print(f"{self.time()} [SERVER] User {nickname} logged out")
            return True
        else:
            await self.send_data(Protocols.Response.LOGOUT_FAILED, "Utilisateur non connecté", addr)
            return False
    
    # Disconnect a client from the game
    async def handle_disconnect(self, addr, game_id):
        print(f"{self.time()} [SERVER] Handling disconnect for {addr} in game {game_id}")
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
        print(f"{self.time()} [SERVER] Handling registration for {addr}")
        counter = 3
        await self.send_data(Protocols.Response.REGISTER_REQUEST, "Entrez un nickname et un mot de passe", addr)
        msg = await self.get_data(addr)
        # Check if nickname and password exist, are coherent and correct
        data = msg.get('data')
        nickname = data["nickname"]
        password = data["password"]
        if self.database.exist_nickname(nickname):
            await self.send_data(Protocols.Response.REGISTER_FAILED, "Nickname déjà utilisé", addr)
            while counter > 0:
                await self.handle_register(addr)
                counter -= 1
                if counter == 0:
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
        print(f"{self.time()} [SERVER] Waiting to receive data from {addr}")
        rcv_data, rcv_addr = await asyncio.wait_for(self.udp_socket.recvfrom(), timeout=30)
        if rcv_addr == addr:
            decoded_data = json.loads(rcv_data.decode())
            print(f"{self.time()} [SERVER] Received data from {addr}: {decoded_data}")
            return decoded_data
        else:
            print(f"{self.time()} [WARNING] Received response from unexpected address: {rcv_addr}")
            return False
        
    # Send an info to one client/player
    async def send_data(self, r_type, data, addr):
        msg = {"type": r_type, "data": data}
        encoded_msg = json.dumps(msg).encode("ascii")
        self.udp_socket.sendto(encoded_msg, addr)
        print(f"{self.time()} [SERVER] Sent to {addr}: {msg}")

    # Send an info to all clients
    async def sendall_data(self, r_type, data):
        msg = {"type": r_type, "data": data}
        encoded_msg = json.dumps(msg).encode("ascii")
        print(f"{self.time()} [SERVER] Broadcasting to all clients: {msg}")
        for addr in self.clients.keys():
            self.udp_socket.sendto(encoded_msg, addr)
            print(f"{self.time()} [SERVER] Sent to {addr}")

    # Create unique ID for a new room
    def generate_game_id(self):
        game_id = (str(uuid.uuid4())[:6])
        return game_id
    
    async def broadcast_message(self, message):
        print(f"{self.time()} [SERVER] Broadcasting message to all clients: {message}")
        for addr in self.clients.keys():
            await self.send_data(Protocols.Response.BROADCAST, message, addr)


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.init_task())