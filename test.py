import tkinter as tk
import asyncio
import websockets

class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def echo(self, websocket, path):
        async for message in websocket:
            await websocket.send(message)

    def start(self):
        start_server = websockets.serve(self.echo, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)

async def send_message(message):
    async with websockets.connect("ws://localhost:8000") as websocket:
        await websocket.send(message)

def on_button_click():
    asyncio.get_event_loop().run_until_complete(send_message("300"))

server = WebSocketServer("localhost", 8000)
server.start()
root = tk.Tk()
button = tk.Button(root, text="Send Message", command=on_button_click)
button.pack()
root.mainloop()
