from Spect_ColorClassifier import SpectColorClassifier
import time
testrgb = (332,163,283,602,1533,1955,89)
start = time.time()
name = SpectColorClassifier.classify(testrgb)

print(f"{name} - tiempo {time.time()- start}")

rgbstring = '332,163,283,602,1533,1955,89'
rgb = rgbstring.split(',')
print(f"Value: {rgb} - Type: {type(rgb)}")
print(type(testrgb))