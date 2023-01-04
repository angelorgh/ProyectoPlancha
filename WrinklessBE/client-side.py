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
def getTimeTemp(color):
        # self.logging.debug('Event getTimeTemp fired')
        f = open('./data/temprules.json')
        rules = json.load(f)
        return TempRule(rules[color]).temp , TempRule(rules[color]).time

if __name__ == '__main__':
    # run the main function
    print(getTimeTemp('red'))
    # asyncio.run(main())
