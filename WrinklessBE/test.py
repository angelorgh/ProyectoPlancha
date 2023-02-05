import serial
import time

def readFromSerial(serial):
        print('Event readFromSerial fired')
        line = serial.read_until().decode()
        print(f"Se leyo de arduino correctamente. Valor {line}")
        return(line)

def writeToSerial(serial):
        print('Event writeToSerial fired')
        serial.write(b'200')
        print('Se ha enviado')
if __name__ == '__main__':
    try:
        ser = serial.Serial("/dev/ttyACM0", 115200, timeout=3000)  # Initialize serial connection
    except:
        ser = serial.Serial("/dev/ttyACM1", 115200, timeout=3000)
    
    ser.reset_input_buffer()
    writeToSerial(ser)
    time.sleep(0.1)
    print(readFromSerial(ser))