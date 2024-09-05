import socket
from datetime import datetime
from lobby import Lobby
import random
import string



class Server:
    def __init__(self):
        self.lobby = Lobby()
        self.running = True
        #self.database = Database()     à voir

    # Initialize server and port
    server = socket.gethostname()
    port = 5555

    # Create socket and initialize connection type
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = socket.gethostbyname(server)

    # Binding port to server and handling binding error
    try:
        serverSocket.bind((server_ip, port))
    except socket.error as e:
        print(str(e))

    # Listen port and accept connections from client
    # Maximum of 2 connections since it's a two-player game
    def run(self):
        while self.running:
            serverSocket.listen(2)
            client, address = serverSocket.accept()

    def handle_client(self, client):
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