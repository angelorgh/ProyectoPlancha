from Spect_ColorClassifier import SpectColorClassifier
import sensors.AS7262_Pi as spec
import time
# testrgb = (332,163,283,602,1533,1955,89)

start = time.time()

def useSpectrometrySensor ():
        print('Event useSpectrometrySensor fired')
        spec.soft_reset()
        spec.set_gain(3)
        spec.set_integration_time(50)
        spec.set_measurement_mode(2)
        spec.enable_main_led()
        try:
            results = spec.get_calibrated_values()
            print(f"Se detecto los colores correctamente. VALOR: {results}")
        except Exception as e:
            print(f"Error leyendo los valores del sensor de espectrometria. InnerException: {e}")
        return tuple(results)

testrgb = useSpectrometrySensor()
name = SpectColorClassifier.classify(testrgb)

print(f"{name} - tiempo {time.time()- start}")

# rgbstring = '332,163,283,602,1533,1955,89'
# rgb = rgbstring.split(',')
# print(f"Value: {rgb} - Type: {type(rgb)}")
# print(type(testrgb))