import json
import pygame

class Client(object):

    def __init__(self, address, nickname, connection):
        self.address = address
        self.nickname = nickname
        self.connection = connection

    def send_data(self, msg):
        self.connection.sendall(json.dumps(msg).encode())


