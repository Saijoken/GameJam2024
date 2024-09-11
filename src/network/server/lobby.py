import asyncio
from datetime import datetime

class Lobby(object):

    def __init__(self):
        # Dict structure : { "game1" : { "game_id" : game_id, "clients": [client1, client2], "game_started": False }}
        self.games = {}

    # Add the game_id as the lobby id and add the first client after a connection
    async def add_game(self, game_id, addr):
        self.games[game_id] = {
            "game_id": game_id,
            "clients": [addr],
            "game_started": False
        }

    # Get lobby from game (join)
    async def get_game(self, game_id):
        return self.games.get(game_id, None)

    # Get length of players
    async def get_len(self, game_id):
        return len(self.games[game_id]["clients"])

    # Add a client (player) to an existing lobby
    async def add_client_to_game(self, game_id, client):
        if game_id in self.games:
            if self.games["clients"]:
                self.games[game_id]["clients"].append(client)

    # Remove a client (player) from an existing lobby when suddenly disconnected
    async def remove_client_from_game(self, game_id, client):
        if game_id in self.games:
            if client in self.games[game_id]["clients"]:
                self.games[game_id]["clients"].remove(client)
    

    # Check if a lobby is full
    #def is_full(self, game_id):
        #return len(self.games[game_id]["clients"]) == 2

    # Start the game once the lobby has two clients
    #def start_game(self, game_id):
        #if self.get_len(game_id) == 2:
            #self.games[game_id]["game_started"] = True

