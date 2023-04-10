import asyncio
from fileinput import filename
from sklearn.cluster import mean_shift
import websockets
import serial
from WrinklessBE.AI.Spect_ColorClassifier import SpectColorClassifier
import logging
import json
from os import path
import time
from WrinklessBE.models.TempRules import TempRule
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
        self.logdirectory = f"./WrinklessBE/data/{self.date}_log.txt"
        self.logging.basicConfig(filename=f"./WrinklessBE/data/{self.date}_log.txt", level=logging.INFO)
        self.serial = ser

    def useSpectrometrySensor (self):
        self.logging.info('Event useSpectrometrySensor fired')
        spec.soft_reset()
        spec.set_gain(3)
        spec.set_integration_time(50)
        spec.set_measurement_mode(3)
        spec.enable_main_led()
        results = []
        try:
            results = spec.get_calibrated_values()
            spec.disable_main_led()
            results = [results[5], results[4], results[3], results[2], results[1], results[0]]
            results.append(89)
            results = tuple(results)
            self.logging.info(f"Se detecto los colores correctamente. VALOR: {results}")
        except Exception as e:
            self.logging.error(f"Error leyendo los valores del sensor de espectrometria. InnerException: {e}")
        return results
    
    def useTemperatureSensor (self):
        self.logging.info('Event useTemperatureSensor fired')
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
        self.logging.info('Event readFromSerial fired')
        try:
            if(expected != ''):
                line = self.ser.read_until(expected).decode()
                self.logging.info(f"Se leyo de arduino correctamente. Valor {line}")
                return(line)
            line = self.ser.read_until().decode()
            self.logging.info(f"Se leyo de arduino correctamente. Valor {line}")
            return(line)
        except Exception as e:
            self.logging.error(f"Error leyendo de arduino. InnerException: {e}")
    
    def readFromSerialOnce(self):
        self.logging.info('Event readFromSerial fired')
        try:
            if(self.ser.in_waiting > 0):
                line = self.ser.readline().decode()
                self.logging.info(f"Se leyo de arduino correctamente. Valor {line}")
                return line
            else:
                self.logging.info(f"No se encontro nada en el input buffer")
                return ''
        except Exception as e:
            self.logging.error(f"Error leyendo de arduino. InnerException: {e}")

    def writeToSerial(self, message):
        self.logging.info('Event writeToSerial fired')
        try:
            self.ser.reset_input_buffer()
            if type(message) == int:
                self.ser.write(message)
            else:
                self.ser.write(message.encode('utf-8'))
            self.logging.info(f"Se ha enviado a serial correctamente. Valor: {message}") 
        except Exception as e:
            self.logging.error(f"Error enviando informacion a serial. Valor enviado {message}. InnerException: {e}")
    
    def callAiModel (self, rgb):
        self.logging.info('Event callAiModel fired')
        try:
            name = SpectColorClassifier.classify(rgb)
            self.logging.info(f"Se corrio modelo AI exitosamente. Valor:{name}")
            return name
        except Exception as e:
            self.logging.error(f"Error corriendo modelo de Color. InnerException: {e}")
    
    def parseRGBColor (self,rgbstring):
        self.logging.info('Event parseRGBColor fired')
        rgb = rgbstring.split(',')
        return rgb
    
    def getTimeTemp(self, color):
        self.logging.info(f"Event getTimeTemp fired. COLOR: {color}")
        f = open(f"{this_dir}/data/temprules.json")
        rules = json.load(f)
        return TempRule(rules[color])

    async def echo(self, websocket):
        async for message in websocket:
            if message == "100":
                try:
                    self.logging.info("HONNING STARTED")
                    self.writeToSerial('Start')
                    honning = self.readFromSerial().strip()
                    self.ser.reset_input_buffer()
                    self.ser.reset_output_buffer()
                    self.logging.info(f"HONNING ENDED. Valor: {honning}")
                    await websocket.send(honning)
                except Exception as e:
                    self.logging.error(f"ERROR in honning! {e}")
                    await websocket.send(e)

            if message == "200":
                
                #self.ser.reset_output_buffer()
                # ready = self.readFromSerial('Waitingstart') #Validar que se quede esperando o poner un time sleep
                # if(ready.strip() == 'Waitingstart'):
                #     # time.sleep(10)
                #     secondstep = self.readFromSerial('Waitingfabric')
                
                self.ser.reset_output_buffer()
                self.writeToSerial('1')
                secondstep = self.readFromSerial().strip()
                self.logging.info(f"VALOR DE EMPEZAR: {secondstep}")
                if secondstep == 'Emergency':
                    await websocket.send('-1')
                if secondstep == "Waitingfabric":
                    rgb = self.useSpectrometrySensor()
                    self.logging.info(f"VALOR DE RGB: {rgb}")
                    color = self.callAiModel(rgb)
                    temprule = self.getTimeTemp(color)
                    self.writeToSerial(str(temprule.num))
                    finish = self.readFromSerial().strip()
                    if finish  == 'Emergency':
                        await websocket.send('-1')
                    self.logging.info(f"MENSAJE RECIBIDO. VALOR{finish}")
                    await websocket.send(str(temprule.time)+ "%"+finish)

            if message == "300":
                temp = self.useTemperatureSensor()
                response = self.readFromSerialOnce().strip()
                if response  == 'Emergency':
                    self.logging.warn(f"Se detecto valor de emergencia: {response}")
                    await websocket.send('-1')
                self.logging.info(f"VALOR QUE LEYO LUEGO DE QUE EMPEZO EL PLANCHADO: {response}")
                result = str(round(temp,2)) + "%"+ ''#response
                self.logging.info(f"Valor de respuesta: {result}")
                await websocket.send(result)

            if message == "400":
                response4 = self.readFromSerialOnce().strip()
                if response4 == 'Emergency':
                    self.logging.warn("SE PRESIONO BOTON DE EMERGENCIA")
                    await websocket.send('-1')
                await websocket.send('')

            if message == "500":
                response4 = self.readFromSerialOnce().strip()
                if response4 == 'Emergency':
                    self.logging.warn("SE PRESIONO BOTON DE EMERGENCIA")
                    await websocket.send('-1')
                await websocket.send(response4)
            if message == "600":
                self.writeToSerial('Cancel')
                response5 = self.readFromSerialOnce().strip()
                if response5 == 'Emergency':
                    self.logging.warn("SE PRESIONO BOTON DE EMERGENCIA")
                    await websocket.send('-1')
                if response5 == 'Waitingstart':
                    await websocket.send(response4)
                else:
                    await websocket.send("Error")
            #Poner logica de cancel
    def start_serial(self):
        try:
            self.ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1000)  # Initialize serial connection
            time.sleep(1)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        except:
            self.ser = serial.Serial("/dev/ttyACM1", 115200, timeout=1000)
            time.sleep(1)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
        finally:
            self.logging.info('SERIAL PORT OPEN')

    def clean_logger (self):
        self.logging.info('Starting WebSocket')
        if path.exists(self.logdirectory):
            self.logging.info("Se borro el log file")
            open(self.logdirectory, "w").close()
    
    def start(self):
        self.logging.info('Starting WebSocket')
        try:
            self.clean_logger()
            self.start_serial()
            start_server = websockets.serve(self.echo, self.host, self.port)
            asyncio.get_event_loop().run_until_complete(start_server)
            self.logging.info('WEBSOCKET SERVER STARTED')
        except Exception as e:
            self.logging.error(f"Error iniciando servidor de WebSockets. InnerException: {e}")
            

