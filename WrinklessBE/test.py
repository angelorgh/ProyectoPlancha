import board
import adafruit_mlx90614
import WrinklessBE.sensors.AS7262_Pi as spec
import logging
from datetime import date

class Calibration:
    def __init__(self) :
        self.logging = logging
        self.date = date.today()
        self.logging.basicConfig(filename=f"./WrinklessBE/data/{self.date}_calibration_log.txt", level=logging.DEBUG)
    i2c = board.I2C()  # uses board.SCL and board.SDA

    mlx = adafruit_mlx90614.MLX90614(i2c)


    print("Ambent Temp: ", mlx.ambient_temperature)
    print("Object Temp: ", mlx.object_temperature)