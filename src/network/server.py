import socket
import threading
from datetime import datetime
from lobby import Lobby
import random
import string
import uuid

# Initialize server and port
SERVER = socket.gethostname()
PORT = 5555

# Create socket and initialize connection type
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = socket.gethostbyname(SERVER)

class Server:

    def __init__(self):
        self.lobby = Lobby()
        self.running = True
        #self.database = Database()     à voir

    def init_connection(self):
        # Bind port to server and handle binding error
        try:
            serverSocket.bind((server_ip, PORT))
        except socket.error as e:
            print(str(e))
        # Listen port and accept connections from client
        # Maximum of 2 connections since it's a two-player game
        serverSocket.listen(2)
        while self.running:
            client, address = serverSocket.accept()
            thread = threading.Thread(target=self.handle_client(client), args=(client, address))
            thread.start()

    # Create unique ID for a new room
    def host(self):
        game_id = (str(uuid.uuid4())[:6])
        return game_id

    # Join a game
    def join(self, game_id):
        pass

    # Handle hosting or joining a room
    def handle_client(self, client, game_id=None):
        # When clicked on PLAY, enter a nickname

        # Hosting a room
        if game_id is None:
            game_id = self.host()
            # Add game id to the db

            # Add one player
            self.lobby.players.append()
            # blabla
        # Joining a room
        if game_id:
            pass

    # Save progression
    def save(self, client, game_id):
        # Nickname+address => character progression => room, save room




















        data = client.recv(1024).decode()
        if data == "create":
            # Generate a random code for the new game
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

            # Create a new game in the lobby with the generated code
            game = self.lobby.create_game(code)

            # Send the game code to the client
            client.send(code.encode())

        elif data.isdigit():
            # Check if the code exists in the lobby
            game = self.lobby.get_game_by_code(data)

            if game:
                # Join the existing game if it has room
                if len(game.players) < 2:
                    game.join_player(client)
                    client.send("joined".encode())
                else:
                    client.send("full".encode())
            else:
                client.send("invalid".encode())