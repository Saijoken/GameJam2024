import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import asyncio
from src.network.client.client import Client
from protocols import Protocols

async def test_client_past():
    client = Client("localhost", 5555)
    await client.connect()

    # Login
    await client.send_command(Protocols.Request.LOGIN, {"username": "past_player", "password": "password123"})
    response = await client.receive_data()
    print("Login response:", response)

    # Create lobby
    await client.send_command(Protocols.Request.CREATE_LOBBY)
    response = await client.receive_data()
    print("Create lobby response:", response)
    game_id = response.get("data", {}).get("game_id")

    # Choose past player
    await client.send_command(Protocols.Request.CHOOSE_ROLE, {"role": "past", "game_id": game_id})
    response = await client.receive_data()
    print("Choose role response:", response)

    # Wait for game to start
    while True:
        response = await client.receive_data()
        print("Received:", response)
        if response.get("type") == Protocols.Response.GAME_STARTED:
            break

    # Close connection
    client.running = False

if __name__ == "__main__":
    asyncio.run(test_client_past())