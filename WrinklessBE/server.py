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
        spec.set_measurement_mode(3)
        spec.enable_main_led()
        results = []
        try:
            results = spec.get_calibrated_values()
            spec.disable_indicator_led()
            results = [results[5], results[4], results[3], results[2], results[1], results[0]]
            results.append(89)
            results = tuple(results)
            self.logging.debug(f"Se detecto los colores correctamente. VALOR: {results}")
        except Exception as e:
            self.logging.error(f"Error leyendo los valores del sensor de espectrometria. InnerException: {e}")
        return results
    
    def useTemperatureSensor (self):
        self.logging.debug('Event useTemperatureSensor fired')
        try:
            i2c = board.I2C()  # uses board.SCL and board.SDA
            mlx = adafruit_mlx90614.MLX90614(i2c)
            temp = mlx.object_temperature
            self.logging.info(f"TEMPERATURA CAPTADA: {temp}")
            return temp
        except Exception as e:
            self.logging.error(f"Error leyendo sensor de temperatura")
            return 0
    def readFromSerial(self, expected = ''):
        self.logging.debug('Event readFromSerial fired')
        try:
            line = self.ser.read_until(expected).decode()
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
                self.writeToSerial('1')
                self.ser.reset_output_buffer()
                ready = self.readFromSerial('Waitingstart') #Validar que se quede esperando o poner un time sleep
                if(ready.strip() == 'Waitingstart'):
                    # time.sleep(10)
                    secondstep = self.readFromSerial('Waitingfabric')
                self.logging.info(f"VALOR DE EMPEZAR: {ready}")
                if secondstep.strip() == "Waitingfabric":
                    rgb = self.useSpectrometrySensor()
                    self.logging.debug(f"VALOR DE RGB: {rgb}")
                    color = self.callAiModel(rgb)
                    temprule = self.getTimeTemp(color)
                    self.writeToSerial(str(temprule.num))
                    finish = self.readFromSerial().strip()
                    self.logging.info(f"MENSAJE RECIBIDO. VALOR{finish}")
                    await websocket.send(str(temprule.time))
            if message == "200":
                temp = self.useTemperatureSensor()
                response = self.readFromSerial().strip()
                result = str(round(temp,2)) + "%"+ response#TempSensorResponse(temp, response)
                await websocket.send(result)
            #Poner logica de cancel
    def start_serial(self):
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
            self.start_serial()
            start_server = websockets.serve(self.echo, self.host, self.port)
            asyncio.get_event_loop().run_until_complete(start_server)
            self.logging.info('WEBSOCKET SERVER STARTED')
        except Exception as e:
            self.logging.error(f"Error iniciando servidor de WebSockets. InnerException: {e}")
            

