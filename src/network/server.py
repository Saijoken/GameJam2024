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
            # Send the game id to the client
            client.send(game_id.encode())
            # Add game id to the db

            # Add one player
            # Allow another connection : Wait and listen

        # Joining a room
        if game_id:
            pass

    # Save progression
    def save(self):
        pass
