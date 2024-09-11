import asyncio
import asyncudp
import json

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.running = True

    async def connect(self):
        self.client_socket = await asyncudp.create_socket(remote_addr=(self.server_ip, self.server_port))
        print(f"Connected to server")

    # Send any data
    async def send_data(self, data):
        message = json.dumps(data).encode()
        self.client_socket.sendto(message)

    # Send formated message
    async def send_command(self, command, data=None):
        message = {
            "type": command,
            "data": data
        }
        await self.send_data(message)

    # 
    async def receive_data(self):
        data,addr = await self.client_socket.recvfrom()
        return json.loads(data.decode())

    async def listen(self):
        while self.running:
            try:
                data = await self.receive_data()
                print("Received from server:", data)
            except Exception as e:
                print(f"Error receiving data: {e}")
                if not self.running:
                    break

    async def run(self):
        await self.connect()
        listen_task = asyncio.create_task(self.listen())
        await listen_task

if __name__ == "__main__":
    client = Client("localhost", 5555)
    asyncio.run(client.run())