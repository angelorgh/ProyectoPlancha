#!/usr/bin/env python3
import serial
import json
import websockets
import asyncio

async def send_message(message):
    async with websockets.connect("ws://localhost:8000") as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        return response