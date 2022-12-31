import subprocess
import asyncio
import websockets



# def call_script(self):
#     process = subprocess.Popen(['python', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     process.wait()
#     self.output, self.error = process.communicate()

#     if self.error != None:
#         raise Exception(self.error.decode("utf-8"))
#     self.output = self.output.decode("utf-8")

#     return self.output

# def stop_script(self):
#     process = subprocess.Popen(['python', filename])
#     try:
#         process.terminate()
#     except Exception as e:
#         # process.kill()
#         raise Exception(f"Error! Tratando de terminar el progrma. Inner exception {e}")


class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def echo(self, websocket, path):
        async for message in websocket:
            await websocket.send(message)

    def start(self):
        start_server = websockets.serve(self.echo, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)


