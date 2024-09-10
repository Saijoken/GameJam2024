import json
import socket
import threading

class Client(object):

    def __init__(self, server_ip, port):
        # Initialize server and port
        self.server_ip = str(server_ip)
        self.port = 5555
        # Create socket and initialize connection type
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_data(self, msg):
        self.connection.sendall(json.dumps(msg).encode())

    def send_data_with_type(self, data_type, data):
        msg = json.dumps({"type": data_type, "data": data})
        self.client.send(msg.encode('ascii'))
