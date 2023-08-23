# we will create a producer coroutine that will generate ten random numbers 
# and put them on the queue. We will also create a consumer coroutine 
# that will get numbers from the queue and report their values.
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
        # check for stop signal
        if item is None:
            break
        # report
        print(f'{time.ctime()} >got {item}')
    # all done
    print(f'{time.ctime()} Consumer: Done')

# entry point coroutine
async def main():
    # create the shared queue
    queue = asyncio.Queue()
    # run the producer and comsumers
    await asyncio.gather(producer(queue), consumer(queue))

# start the asyncio program
asyncio.run(main())

''' Result
Wed Aug 23 15:01:51 2023 Producer: Running
Wed Aug 23 15:01:51 2023 Consumer: Running
Wed Aug 23 15:01:52 2023 >got 0.45093840392588125
Wed Aug 23 15:01:53 2023 >got 0.6364806082572031
Wed Aug 23 15:01:53 2023 >got 0.584951687491824
Wed Aug 23 15:01:53 2023 >got 0.05096739235936154
Wed Aug 23 15:01:54 2023 >got 0.6201708769389819
Wed Aug 23 15:01:54 2023 >got 0.5413889963110164
Wed Aug 23 15:01:55 2023 >got 0.8466190359927783
Wed Aug 23 15:01:56 2023 >got 0.30860057191380197
Wed Aug 23 15:01:56 2023 >got 0.8534444823816788
Wed Aug 23 15:01:57 2023 Producer: Done
Wed Aug 23 15:01:57 2023 >got 0.7092381830952283
Wed Aug 23 15:01:57 2023 Consumer: Done
'''