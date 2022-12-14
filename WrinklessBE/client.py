#!/usr/bin/env python3
import serial
import json
import websockets
import asyncio

def readFromSerial ():
    file = open('data.txt','w+')

    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            file.write('\n' + line)

async def send_message(message):
    async with websockets.connect("ws://localhost:8000") as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        return response