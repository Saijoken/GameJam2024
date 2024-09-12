import asyncio
from src.network.client.client import Client  # Changement pour un import absolu

class ServerManager:
    def __init__(self, server_ip="localhost", server_port=5555):
        self.client = Client(server_ip, server_port)
        self.loop = asyncio.get_event_loop()
        self.running = False
        self.connected = False
        
        self.isValveOpen = False
        self.enigme1potentiometer1 = False
        self.enigme1potentiometer2 = False

    async def start(self):
        if not self.connected:
            await self.client.connect()
            self.client.set_message_callback(self.handle_received_data)
            self.connected = True
        self.running = True
        self.listen_task = asyncio.create_task(self.client.listen())

    async def stop(self):
        self.running = False
        if hasattr(self, 'listen_task'):
            self.listen_task.cancel()
            try:
                await self.listen_task
            except asyncio.CancelledError:
                pass
        self.connected = False

    async def send_command(self, command, data=None):
        if not self.connected:
            await self.start()
        await self.client.send_command(command, data)

    async def handle_received_data(self, data):
        print("Données reçues du serveur:", data)
        # Traitez les données reçues ici, par exemple:
        if data['type'] == 'BROADCAST':
            message = data['data']
            # Mettez à jour les variables en fonction du message reçu
            if 'valve_opened' in message:
                self.isValveOpen = message['valve_opened']
            if 'potentiometer1' in message:
                self.enigme1potentiometer1 = message['potentiometer1']
            if 'potentiometer2' in message:
                self.enigme1potentiometer2 = message['potentiometer2']

    def run_command(self, command, data=None):
        return self.loop.run_until_complete(self.send_command(command, data))

    def start_sync(self):
        self.loop.run_until_complete(self.start())

    def stop_sync(self):
        self.loop.run_until_complete(self.stop())
