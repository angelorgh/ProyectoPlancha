import asyncio
from fileinput import filename
import websockets
import serial
from WrinklessBE.AI.Spect_ColorClassifier import SpectColorClassifier
import logging

class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.logging = logging
        self.logging.basicConfig(filename='./WrinklessBE/data/log.txt', level=logging.DEBUG)
    
    def readFromSerial(self):
        self.logging.debug('Event readFromSerial fired')
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                return(line)

    def writeToSerial(self):
        self.logging.debug('Event writeToSerial fired')
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        ser.reset_input_buffer()
        ser.write("Start")
    
    def callAiModel (self, rgb):
        self.logging.debug('Event callAiModel fired')
        try:
            name= SpectColorClassifier.classify(rgb)
            return name
        except Exception as e:
            self.logging.error(f"Error corriendo modelo de Color. InnerException: {e}")
    
    def parseRGBColor (self,rgbstring):
        self.logging.debug('Event parseRGBColor fired')
        rgb = rgbstring.split(',')
        return rgb

    async def echo(self, websocket, path):
        async for message in websocket:
            if message == "300":
                await websocket.send(self.readFromSerial())
            if message == "100":
                rgb = self.readFromSerial()
                name = self.callAiModel(self, rgb)
                await websocket.send(name)

    def start(self):
        self.logging.debug('Starting WebSocket')
        try:
            start_server = websockets.serve(self.echo, self.host, self.port)
            asyncio.get_event_loop().run_until_complete(start_server)
            self.logging.debug('WEBSOCKET SERVER STARTED')
        except Exception as e:
            self.logging.error(f"Error iniciando servidor de WebSockets. InnerException: {e}")
    
