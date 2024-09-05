import socket
from datetime import datetime
from lobby import Lobby



class Server:
    def __init__(self):
        self.lobby = Lobby()
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
    while True:
        serverSocket.listen(2)
        client, address = serverSocket.accept()
