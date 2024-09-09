import socket
import json
import threading

class TestClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            print(f"Attempting to connect to {self.host}:{self.port}")  # Debug print
            self.client.connect((self.host, self.port))
            print("Connected to server")
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            self.send_nickname()
        except Exception as e:
            print(f"Error connecting to server: {e}")

    def send_message(self, message_type, data):
        message = json.dumps({"type": message_type, "data": data})
        self.client.send(message.encode('ascii'))

    def send_nickname(self):
        nickname = input("Enter your nickname: ")
        self.send_message("NICKNAME", nickname)
        self.nickname = nickname

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message:
                    data = json.loads(message)
                    print(f"Received: {data}")
                    if data['type'] == "NICKNAME":
                        self.send_nickname()
                    elif data['type'] == "LOBBY_CREATED":
                        print(f"Lobby created with game ID: {data['data']['game_id']}")
                    elif data['type'] == "REQUEST_GAME_ID":
                        game_id = input("Enter game ID to join: ")
                        self.send_message("JOIN_GAME", game_id)
            except Exception as e:
                print(f"Error receiving message: {e}")

    def run(self):
        print("Starting client")  # Debug print
        self.connect()
        while True:
            command = input("Enter command (create/join/quit): ")
            if command == "create":
                self.send_message("CREATE_LOBBY", None)
            elif command == "join":
                game_id = input("Enter game ID to join: ")
                self.send_message("JOIN_GAME", game_id)
            elif command == "quit":
                print("Disconnecting...")
                self.client.close()
                break
            else:
                print("Invalid command")

if __name__ == "__main__":
    print("Script started")  # Debug print
    client = TestClient('127.0.0.1', 5555)
    client.run()