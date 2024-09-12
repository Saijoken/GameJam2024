import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

import asyncio
from src.network.client.client import Client
from protocols import Protocols

async def test_client_future():
    client = Client("127.0.0.1", 5555)
    await client.connect()

    # Play
    await client.send_command(Protocols.Request.WANT_TO_PLAY)
    response = await client.receive_data()
    print("Auth options:", response)

    await client.send_command(Protocols.Request.LOGIN, {"username": "future_player", "password": "password456"})
    response = await client.receive_data()
    print("Login response:", response)

    # Attendez la réponse du serveur avant d'envoyer la commande suivante
    if response.get('type') == Protocols.Response.LOGIN_SUCCESS:
        await client.send_command(Protocols.Request.CREATE_LOBBY)
        response = await client.receive_data()
        print("Create lobby response:", response)

    # Join lobby
    await client.send_command(Protocols.Request.JOIN_LOBBY, {"game_id": "ask_for_game_id"})
    response = await client.receive_data()
    print("Join lobby response:", response)

    # Error
    game_id = response.get("data", {}).get("game_id")

    # Choose future player
    await client.send_command(Protocols.Request.CHOOSE_ROLE, {"role": "future", "game_id": game_id})
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
    asyncio.run(test_client_future())