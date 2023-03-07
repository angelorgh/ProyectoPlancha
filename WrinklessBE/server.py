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
import os
this_dir = os.path.dirname(__file__) # Path to loader.py
class WebSocketServer:
    def __init__(self, host, port, ser = None):
        self.host = host
        self.port = port
        self.logging = logging
        self.logging.basicConfig(filename='./WrinklessBE/data/log.txt', level=logging.DEBUG)
        self.serial = ser
    
    def readFromSerial(self):
        self.logging.debug('Event readFromSerial fired')
        try:
            line = self.ser.read_until().decode()
            self.logging.info(f"Se leyo de arduino correctamente. Valor {line}")
            return(line)
        except Exception as e:
            self.logging.error(f"Error leyendo de arduino. InnerException: {e}")
        # ser.reset_input_buffer()
        # while True:
        #     self.logging.info(f"Valor del serial: {ser.in_waiting}")
        #     if ser.in_waiting > 0:
        #         line = ser.readline().decode('utf-8').rstrip()
        #         self.logging.info(f"Se leyo de arduino correctamente. Valor {line}")
        #         return(line)

    def writeToSerial(self, message):
        self.logging.debug('Event writeToSerial fired')
        try:
            self.ser.reset_input_buffer()
            self.ser.write(message.encode('utf-8'))
            self.logging.info(f"Se ha enviado a serial correctamente. Valor: {message}") 
        except Exception as e:
            self.logging.error(f"Error enviando informacion a serial. Valor enviado{message}. InnerException: {e}")
    
    def callAiModel (rgb, *_ar):
        # self.logging.debug('Event callAiModel fired')
        try:
            name = SpectColorClassifier.classify(rgb)
            # self.logging.info(f"Se corrio modelo AI exitosamente. Valor:{name}")
            print(f"Se corrio modelo AI exitosamente. Valor:{name}")
            return name
        except Exception as e:
            # self.logging.error(f"Error corriendo modelo de Color. InnerException: {e}")
            print(f"Error corriendo modelo de Color. InnerException: {e}")
            
    
    def parseRGBColor (self,rgbstring):
        self.logging.debug('Event parseRGBColor fired')
        rgb = rgbstring.split(',')
        return rgb
    
    def getTimeTemp(self, color):
        self.logging.debug('Event getTimeTemp fired')
        f = open(f"{this_dir}/data/temprules.json'")
        rules = json.load(f)
        return TempRule(rules[color])

    async def echo(self, websocket):
        async for message in websocket:
            if message == "100":
                self.writeToSerial('100')
                time.sleep(1.5)
                rgbstring = self.readFromSerial()
                rgb = tuple(rgbstring.split(','))
                self.logging.debug(f"VALOR DE RGB: {rgb}")
                color = self.callAiModel(self, rgb)
                temprule = self.getTimeTemp(color)
                self.writeToSerial(str(temprule.num))
                finish = self.readFromSerial()
                self.logging.info(f"MENSAJE RECIBIDO. VALOR{finish}")
                await websocket.send(temprule)
    def start_serial(self, *_ar):
        try:
            self.ser = serial.Serial("/dev/ttyACM0", 115200, timeout=3000)  # Initialize serial connection
            time.sleep(1)
        except:
            self.ser = serial.Serial("/dev/ttyACM1", 115200, timeout=3000)
            time.sleep(1)
        finally:
            self.logging.info('SERIAL PORT OPEN')

    def start(self):
        self.logging.debug('Starting WebSocket')
        try:
            self.start_serial(self)
            start_server = websockets.serve(self.echo, self.host, self.port)
            asyncio.get_event_loop().run_until_complete(start_server)
            self.logging.info('WEBSOCKET SERVER STARTED')
        except Exception as e:
            self.logging.error(f"Error iniciando servidor de WebSockets. InnerException: {e}")
            
    
