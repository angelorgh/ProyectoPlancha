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
from WrinklessBE.models.TempSensor import TempSensorResponse
from datetime import date
import os
import board
import adafruit_mlx90614
import WrinklessBE.sensors.AS7262_Pi as spec
this_dir = os.path.dirname(__file__) # Path to loader.py
class WebSocketServer:
    def __init__(self, host, port, ser = None):
        self.host = host
        self.port = port
        self.logging = logging
        self.date = date.today()
        self.logging.basicConfig(filename=f"./WrinklessBE/data/{self.date}_log.txt", level=logging.DEBUG)
        self.serial = ser
    
    def useSpectrometrySensor (self):
        self.logging.debug('Event useSpectrometrySensor fired')
        spec.soft_reset()
        spec.set_gain(3)
        spec.set_integration_time(50)
        spec.set_measurement_mode(2)
        spec.enable_main_led()
        try:
            results = spec.get_calibrated_values()
            self.logging.info(f"Se detecto los colores correctamente. VALOR: {results}")
        except Exception as e:
            self.logging.error(f"Error leyendo los valores del sensor de espectrometria. InnerException: {e}")
        return results
    def useTemperatureSensor (self):
        self.logging.debug('Event useTemperatureSensor fired')
        try:
            i2c = board.I2C()  # uses board.SCL and board.SDA
            mlx = adafruit_mlx90614.MLX90614(i2c)
            temp = mlx.object_temperature
            self.logging.info("TEMPERATURA CAPTADA: {temp}")
            return temp
        except Exception as e:
            self.logging.error(f"Error leyendo sensor de temperatura")
            return 0
    def readFromSerial(self):
        self.logging.debug('Event readFromSerial fired')
        try:
            line = self.ser.read_until().decode()
            self.logging.info(f"Se leyo de arduino correctamente. Valor {line}")
            return(line)
        except Exception as e:
            self.logging.error(f"Error leyendo de arduino. InnerException: {e}")

    def writeToSerial(self, message):
        self.logging.debug('Event writeToSerial fired')
        try:
            self.ser.reset_input_buffer()
            self.ser.write(message.encode('utf-8'))
            self.logging.info(f"Se ha enviado a serial correctamente. Valor: {message}") 
        except Exception as e:
            self.logging.error(f"Error enviando informacion a serial. Valor enviado{message}. InnerException: {e}")
    
    def callAiModel (self, rgb):
        self.logging.debug('Event callAiModel fired')
        try:
            name = SpectColorClassifier.classify(rgb)
            self.logging.info(f"Se corrio modelo AI exitosamente. Valor:{name}")
            return name
        except Exception as e:
            self.logging.error(f"Error corriendo modelo de Color. InnerException: {e}")
    
    def parseRGBColor (self,rgbstring):
        self.logging.debug('Event parseRGBColor fired')
        rgb = rgbstring.split(',')
        return rgb
    
    def getTimeTemp(self, color):
        self.logging.debug(f"Event getTimeTemp fired. COLOR: {color}")
        f = open(f"{this_dir}/data/temprules.json")
        rules = json.load(f)
        return TempRule(rules[color])

    async def echo(self, websocket):
        async for message in websocket:
            if message == "100":
                self.writeToSerial('100')
                self.ser.reset_output_buffer()
                ready = self.readFromSerial()
                self.logging.info(f"VALOR DE EMPEZAR: {ready}")
                parseready = str(ready)
                ifcon = str("Hola")
                if parseready.strip() == ifcon:
                    self.logging.debug("ENTRO AL IF")
                    # rgbstring = self.readFromSerial()
                    rgbstring = self.useSpectrometrySensor(self)
                    rgb = tuple(rgbstring)
                    self.logging.debug(f"VALOR DE RGB: {rgb}")
                    color = self.callAiModel(self, rgb)
                    temprule = self.getTimeTemp(color)
                    self.writeToSerial(str(temprule.num))
                    finish = self.readFromSerial()
                    self.logging.info(f"MENSAJE RECIBIDO. VALOR{finish}")
                    await websocket.send(temprule)
            self.logging.debug(f"NO ENTRO AL IF. Valor paseArduino: {parseready} Valor parseado: {ifcon}")
            if message == "200":
                temp = self.useTemperatureSensor(self)
                response = self.readFromSerial()
                result = TempSensorResponse(temp, response)
                await websocket.send(result)
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
            

