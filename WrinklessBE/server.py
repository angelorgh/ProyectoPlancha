import asyncio
from fileinput import filename
from sklearn.cluster import mean_shift
import websockets
import serial
from WrinklessBE.AI.Spect_ColorClassifier import SpectColorClassifier
import logging
import json
import time
from WrinklessBE.models.TempRules import TempRule
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
            self.logging.info(f"Valor del serial: {ser.in_waiting}")
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                self.logging.info(f"Se leyo de arduino correctamente. Valor {line}")
                return(line)

    def writeToSerial(self, message):
        self.logging.debug('Event writeToSerial fired')
        try:
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            ser.reset_input_buffer()
            ser.write(message.encode())
        except Exception as e:
            self.logging.error(f"Error enviando informacion a serial. Valor enviado{message}. InnerException: {e}")
        finally:
            self.logging.info(f"Se ha enviado a serial correctamente. Valor: {message}")        
    
    def callAiModel (self, rgb):
        self.logging.debug('Event callAiModel fired')
        try:
            name = SpectColorClassifier.classify(rgb)
            return name
        except Exception as e:
            self.logging.error(f"Error corriendo modelo de Color. InnerException: {e}")
        finally:
            self.logging.info(f"Se corrio modelo AI exitosamente. Valor:{name}")
    
    def parseRGBColor (self,rgbstring):
        self.logging.debug('Event parseRGBColor fired')
        rgb = rgbstring.split(',')
        return rgb
    
    def getTimeTemp(self, color):
        self.logging.debug('Event getTimeTemp fired')
        f = open('./data/temprules.json')
        rules = json.load(f)
        return TempRule(rules[color])

    async def echo(self, websocket, path):
        async for message in websocket:
            if message == "100":
                self.writeToSerial('200')
                time.sleep(10)
                rgb = self.readFromSerial()
                color = self.callAiModel(self, rgb)
                temprule = self.getTimeTemp(color)
                self.writeToSerial(str(temprule.num))
                finish = self.readFromSerial()
                self.logging.info(f"MENSAJE RECIBIDO. VALOR{finish}")
                await websocket.send(temprule)

    def start(self):
        self.logging.debug('Starting WebSocket')
        try:
            start_server = websockets.serve(self.echo, self.host, self.port)
            asyncio.get_event_loop().run_until_complete(start_server)
        except Exception as e:
            self.logging.error(f"Error iniciando servidor de WebSockets. InnerException: {e}")
        finally:
            self.logging.info('WEBSOCKET SERVER STARTED')
    
