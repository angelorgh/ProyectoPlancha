# import threading

# lock = threading.Lock()

# def writeFile():
#     with lock:
#         with open('./data/data.json', 'w+') as file:
#             i = 0
#             while i < 16000:
#                 i += 1
#                 file.write(f'\n"{i}":"line{i}",')

# if __name__ == '__main__':
#     thread = threading.Thread(target=writeFile)
#     thread.start()
#     with lock:
#         with open("./data/data.json", 'r') as file:
#             print(file.read())

import asyncio
import json
from models.TempRules import TempRule
from AI.Spect_ColorClassifier import SpectColorClassifier
import serial
async def write_to_file(filename):
    with open(filename, 'w+') as file:
        i = 0
        while i < 100:
            i += 1
            file.write(f'\n"{i}":"line{i}",')
            await asyncio.sleep(0.1)  # pause for 0.1 seconds

async def read_from_file(filename):
    with open(filename, 'r+') as file:
        while True:
            data = file.read(1024)
            # if not data:
            #     break  # exit the loop if there is no more data to read
            print(data)
            await asyncio.sleep(0.1)

async def main():
    filename = './data/data.json'
    # create two tasks using asyncio.create_task
    write_task = asyncio.create_task(write_to_file(filename))
    read_task = asyncio.create_task(read_from_file(filename))
    # wait for both tasks to complete
    await asyncio.gather(write_task, read_task)
def readFromSerial():
        print('Event readFromSerial fired')
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        # ser.reset_input_buffer()
        while True:
            print(f"Valor del serial: {ser.in_waiting}")
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(f"Se leyo de arduino correctamente. Valor {line}")
                return(line)
def writeToSerial(message):
        print('Event writeToSerial fired')
        try:
            ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            ser.reset_output_buffer()
            # ser.reset_input_buffer()
            ser.write(message.encode('utf-8'))
            # ser.reset_input_buffer()
        except Exception as e:
            print(f"Error enviando informacion a serial. Valor enviado{message}. InnerException: {e}")
        finally:
            print(f"Se ha enviado a serial correctamente. Valor: {message}")   
if __name__ == '__main__':
    # run the main function
    print(readFromSerial())
    # writeToSerial("200")
