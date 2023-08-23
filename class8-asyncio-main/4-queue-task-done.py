from random import random
import asyncio
import time

# coroutine to generate work
async def producer(queue):
    print(f'{time.ctime()} Producer: Running')
    # generate work
    for i in range(10):
        # generate a value
        value = random()
        # block tp simulate work
        await asyncio.sleep(value)
        # add to the queue
        await queue.put(value)
        # print(f'{time.ctime()} Producer: put {value}')
    # send an all done signal
    await queue.put(None)
    print(f'{time.ctime()} Producer: Done')
# coroutine to consume work
async def consumer(queue):
    print(f'{time.ctime()} Consumer: Running')
    # consume work
    while True:
        # get a unit of work
        item = await queue.get()
        # report 
        print(f'{time.ctime()} >got {item}')
        # block while processing
        if item:
            await asyncio.sleep(item)
        # mark the task as done
        queue.task_done()

# entry point coroutine
async def main():
    # create the shared queue
    queue = asyncio.Queue()
    # start the consumer
    _ = asyncio.create_task(consumer(queue))
    # start the producer and wait for it to finsih
    await asyncio.create_task(producer(queue))
    # wait for all items to be processed
    await queue.join()

# start the asyncio program
asyncio.run(main())

''' Result
Wed Aug 23 15:08:58 2023 Consumer: Running
Wed Aug 23 15:08:58 2023 Producer: Running
Wed Aug 23 15:08:59 2023 >got 0.5958197336814517
Wed Aug 23 15:08:59 2023 >got 0.9368464955495379
Wed Aug 23 15:09:00 2023 >got 0.15289499259708306
Wed Aug 23 15:09:01 2023 >got 0.20487631829533615
Wed Aug 23 15:09:01 2023 >got 0.1268202125521558
Wed Aug 23 15:09:01 2023 >got 0.9310098506640163
Wed Aug 23 15:09:02 2023 >got 0.47805124001476584
Wed Aug 23 15:09:02 2023 >got 0.8815276298263229
Wed Aug 23 15:09:03 2023 >got 0.3383282523076949
Wed Aug 23 15:09:04 2023 Producer: Done
Wed Aug 23 15:09:04 2023 >got 0.9535600156955537
Wed Aug 23 15:09:05 2023 >got None
'''