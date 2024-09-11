import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import asyncio
from src.network.client.client import Client
from protocols import Protocols

async def test_client_past():
    client = Client("localhost", 5555)
    await client.connect()

    # Play
    response = await client.receive_data()
    print("Première réponse:", response)
    await client.send_command(Protocols.Request.WANT_TO_PLAY, None)
    auth_options = await client.receive_data()
    print("Auth options:", auth_options)

    # Login
    # Ne va potentiellement pas fonctionner
    await client.send_command(Protocols.Request.LOGIN, {"username": "past_player", "password": "password123"})
    login_response = await client.receive_data()
    print("Login response (normalement directement create ou join lobby):", login_response)

    # Create or join lobby options

    response = await client.receive_data()
    print("Lobby options:", response)

    # Create lobby
    await client.send_command(Protocols.Request.CREATE_LOBBY)
    response = await client.receive_data()
    print("Create lobby response:", response)
    game_id = response.get("data", {}).get("game_id")

    if game_id:
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
    else:
        print("Failed to create lobby")

    # Close connection
    client.running = False

if __name__ == "__main__":
    asyncio.run(test_client_past())