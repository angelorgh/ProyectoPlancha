from Spect_ColorClassifier import SpectColorClassifier
import time
rgb = (332,163,283,602,1533,1955,89)
start = time.time()
name = SpectColorClassifier.classify(rgb)

print(f"{name} - tiempo {time.time()- start}")

