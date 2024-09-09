import json
import socket
import threading

class Client(object):

    def __init__(self, server_ip):
        # Initialize server and port
        self.SERVER = str(server_ip)
        self.PORT = 5555
        # Create socket and initialize connection type
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_data(self, msg):
        self.connection.sendall(json.dumps(msg).encode())
