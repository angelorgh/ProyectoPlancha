import asyncio
import websockets
import serial

class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def readFromSerial(self):
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                return(line)

    async def echo(self, websocket, path):
        async for message in websocket:
            if message == "300":
                await websocket.send(self.readFromSerial())

    def start(self):
        start_server = websockets.serve(self.echo, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
