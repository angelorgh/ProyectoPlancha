import serial
# ser = serial.Serial("/dev/ttyS0", 9600)
ser = serial.Serial('COM5', 9600)
message = ser.readline().decode("utf-8")
print(message)
ser.close()