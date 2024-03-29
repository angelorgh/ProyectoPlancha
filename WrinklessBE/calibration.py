import board
import adafruit_mlx90614
import WrinklessBE.sensors.AS7262_Pi as spec
import logging
from datetime import date

class Calibration:
    def __init__(self) :
        self.logging = logging
        self.date = date.today()
        self.logging.basicConfig(filename=f"./WrinklessBE/data/{self.date}_calibration_log.txt", level=logging.INFO)
    
    def calibrate_tempsensor (self):
        self.logging.info("Event calibrate_tempsensor started")
        i2c = board.I2C()  # uses board.SCL and board.SDA
        mlx = adafruit_mlx90614.MLX90614(i2c)
        object = ''
        try:
            object = mlx.object_temperature
            self.logging.info(f"Se logro leer la temperatura correctamente. Valor: {object}")
        except Exception as e:
            self.logging.error(f"Error en el sensor de temperatura. InnerException: {e}")
            raise Exception(f"Error en el sensor de temperatura. InnerException: {e}")
        finally:
            return object

    def calibrate_spectsensor (self):
        self.logging.info("Event calibrate_spectsensor started")
        spec.soft_reset()
        spec.set_gain(3)
        spec.set_integration_time(50)
        spec.set_measurement_mode(3)
        spec.enable_main_led()
        results = []
        try:
            results = spec.get_calibrated_values()
            spec.disable_main_led()
            results = [results[0], results[1], results[2], results[3], results[4], results[5]]
            results.append(89)
            results = tuple(results)
            self.logging.info(f"Se detecto los colores correctamente. VALOR: {results}")
        except Exception as e:
            self.logging.error(f"Error leyendo los valores del sensor de espectrometria. InnerException: {e}")
            raise Exception(f"Error leyendo los valores del sensor de espectrometria. InnerException: {e}")
        finally:
            return results
        
    def calibrate(self):
        self.logging.info("CALIBRATION STARTED")
        errortemp = ''
        errorspect = ''
        try:
            temp = self.calibrate_tempsensor()
        except Exception as e:
            errortemp = e
        try:
            spect = self.calibrate_spectsensor()
        except Exception as e2:
            errorspect = e2
        if(errortemp != '' or errorspect != ''):
            return f"ERROR!:\nError en sensor de spectometria: {errortemp}\nError en sensor de temperatura: {errorspect}"
        self.logging.info("CALIBRATION ENDED")
        return f"Temperatura: {temp}\n Colores:{spect}"