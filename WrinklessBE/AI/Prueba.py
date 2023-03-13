from Spect_ColorClassifier import SpectColorClassifier
import AS7262_Pi as spec
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
            results = [results[5], results[4], results[3], results[2], results[1], results[0]]
            results.append(89)
            print(type(results))
            results = tuple(results)
            print(f"Se detecto los colores correctamente. VALOR: {results}")
        except Exception as e:
            print(f"Error leyendo los valores del sensor de espectrometria. InnerException: {e}")
        return results

testrgb = useSpectrometrySensor()
name = SpectColorClassifier.classify(testrgb)

print(f"{name} - tiempo {time.time()- start}")

# rgbstring = '332,163,283,602,1533,1955,89'
# rgb = rgbstring.split(',')
# print(f"Value: {rgb} - Type: {type(rgb)}")
# print(type(testrgb))