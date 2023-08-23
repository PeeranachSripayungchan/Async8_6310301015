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
        try:
            # retieve the get() awaitable
            get_await = queue.get()
            # await the awaitable with a timeout
            item = await asyncio.wait_for(get_await, 0.5)
        except asyncio.TimeoutError:
            print(f'{time.ctime()} Consumer: gave up waiting...')
            continue
        # check for stop
        if item is None:
            break
        # report
        print(f'{time.ctime()} >got {item}')
    # all done
    print('Consumer: Done')

# entry point coroutine
async def main():
    # create the shared queue
    queue = asyncio.Queue()
    # run the producer and consumers
    await asyncio.gather(producer(queue), consumer(queue))

# start the asyncio program
asyncio.run(main())

''' Result
Wed Aug 23 15:04:26 2023 Producer: Running
Wed Aug 23 15:04:26 2023 Consumer: Running
Wed Aug 23 15:04:27 2023 Consumer: gave up waiting...
Wed Aug 23 15:04:27 2023 >got 0.8722600852594157
Wed Aug 23 15:04:28 2023 Consumer: gave up waiting...
Wed Aug 23 15:04:28 2023 >got 0.5420615456000506
Wed Aug 23 15:04:28 2023 Consumer: gave up waiting...
Wed Aug 23 15:04:29 2023 >got 0.8027160604320499
Wed Aug 23 15:04:29 2023 Consumer: gave up waiting...
Wed Aug 23 15:04:29 2023 >got 0.7704266940759483
Wed Aug 23 15:04:30 2023 Consumer: gave up waiting...
Wed Aug 23 15:04:30 2023 >got 0.8228339450410269
Wed Aug 23 15:04:31 2023 Consumer: gave up waiting...
Wed Aug 23 15:04:31 2023 >got 0.8362788453261857
Wed Aug 23 15:04:32 2023 Consumer: gave up waiting...
Wed Aug 23 15:04:32 2023 >got 0.8059167562733752
Wed Aug 23 15:04:32 2023 >got 0.16845637264909463
Wed Aug 23 15:04:32 2023 >got 0.1721886474601363
Wed Aug 23 15:04:33 2023 Producer: Done
Wed Aug 23 15:04:33 2023 Consumer: gave up waiting...
Wed Aug 23 15:04:33 2023 >got 0.5088437213995426
Consumer: Done
'''