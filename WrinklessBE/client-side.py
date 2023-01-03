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

async def write_to_file(filename):
    with open(filename, 'w+') as file:
        i = 0
        while i < 1500:
            i += 1
            file.write(f'\n"{i}":"line{i}",')
            await asyncio.sleep(0.01)  # pause for 0.1 seconds

async def read_from_file(filename):
    with open(filename, 'r') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            print(data)  # add a print statement here to print the data
            await asyncio.sleep(0.1)  # pause for 0.1 seconds

async def main():
    filename = './data/data.json'
    # create two tasks using asyncio.create_task
    write_task = asyncio.create_task(write_to_file(filename))
    read_task = asyncio.create_task(read_from_file(filename))
    # wait for both tasks to complete
    await asyncio.gather(write_task, read_task)

if __name__ == '__main__':
    # run the main function
    asyncio.run(main())
