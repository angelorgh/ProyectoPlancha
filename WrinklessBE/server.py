import subprocess
import asyncio
import websockets



def call_script(self):
    process = subprocess.Popen(['python', filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    self.output, self.error = process.communicate()

    if self.error != None:
        raise Exception(self.error.decode("utf-8"))
    self.output = self.output.decode("utf-8")

    return self.output

def stop_script(self):
    process = subprocess.Popen(['python', filename])
    try:
        process.terminate()
    except Exception as e:
        # process.kill()
        raise Exception(f"Error! Tratando de terminar el progrma. Inner exception {e}")

class Server:
    async def echo(websocket, path):
        async for message in websocket:
            await websocket.send(message)

    start_server = websockets.serve(echo, "localhost", 8000)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
