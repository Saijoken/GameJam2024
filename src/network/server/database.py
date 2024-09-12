import json
import os
import hashlib

class Database:

    def __init__(self, file):
        self.file = file
        self.data = self.load_data()

    # Load the game/players state from the JSON file
    def load_data(self):
        if os.path.exists(self.file):
            with open(self.file, 'r') as f:
                return json.load(f)
        else:
            return json.JSONDecodeError
        
    # Save the game/players state in the JSON file
    def save_data(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f)

    # Check if nickname is already taken
    def exist_nickname(self, nickname):
        for lobby in self.data.values():
            if nickname in lobby:
                return True
        return False

    # Add a new player/client into the database
    def add_user(self, lobby, nickname, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.data[lobby][nickname] = {
            "password": hashed_password,
            "game": None
        }
        self.save_data()
        return True

    # Check password on login
    def check_password(self, nickname, password, lobby):
        if lobby in self.data:
            if nickname in self.data[lobby]:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                return self.data[lobby][nickname]["password"] == hashed_password
        return False
    
    # Save the game state : room/riddle
    def save_game_state(self, nickname, lobby, room, riddle):
        if lobby in self.data and nickname in self.data[lobby]:
            self.data[lobby][nickname]["game"] = {
                "room": room,
                "riddle": riddle
            }
            self.save_data()
            return True
        return False


    # Load the game state
    def load_game_state(self, nickname, lobby):
        if lobby in self.data and nickname in self.data[lobby]:
            return self.data[lobby][nickname].get("game", None)
        return None

        
    