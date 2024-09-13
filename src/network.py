import socket
import pickle

class Network:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            received_data = self.client.recv(2048)
            try:
                return pickle.loads(received_data)
            except pickle.UnpicklingError:
                print(f"Erreur de désérialisation. Données reçues : {received_data}")
                return None
        except socket.error as e:
            print(f"Erreur réseau : {e}")
            return None