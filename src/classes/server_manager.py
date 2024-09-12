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
            self.connected = True
        self.running = True
        self.listen_task = asyncio.create_task(self.listen())

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

    async def listen(self):
        while self.running:
            try:
                data = await self.client.receive_data()
                await self.handle_received_data(data)
            except Exception as e:
                print(f"Erreur lors de la réception des données : {e}")
                if not self.running:
                    break

    async def handle_received_data(self, data):
        print("Données reçues du serveur:", data)

    def run_command(self, command, data=None):
        return self.loop.run_until_complete(self.send_command(command, data))
    
    


    def start_sync(self):
        self.loop.run_until_complete(self.start())

    def stop_sync(self):
        self.loop.run_until_complete(self.stop())
