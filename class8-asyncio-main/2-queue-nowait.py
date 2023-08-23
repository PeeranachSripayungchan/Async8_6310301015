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
        print(f'{time.ctime()} Producer: put {value}')
    # send an all done signal
    await queue.put(None)
    print(f'{time.ctime()} Producer: Done')
# coroutine to consume work
async def consumer(queue):
    print(f'{time.ctime()} Consumer: Running')
    # consume work
    while True:
        # get a unit of work without blocking
        try:
            item = await queue.get()
        except asyncio.QueueEmpty:
            print(f'{time.ctime()} Consumer: got nothing, waiting a while...')
            await asyncio.sleep(0.5)
            continue
        # check for stop
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
    # run the producer and consumers
    await asyncio.gather(producer(queue), consumer(queue))

# start the asyncio program
asyncio.run(main())

''' Result
Wed Aug 23 15:02:51 2023 Producer: Running
Wed Aug 23 15:02:51 2023 Consumer: Running
Wed Aug 23 15:02:51 2023 Producer: put 0.14945179188957314
Wed Aug 23 15:02:51 2023 >got 0.14945179188957314
Wed Aug 23 15:02:52 2023 Producer: put 0.3704998566768919
Wed Aug 23 15:02:52 2023 >got 0.3704998566768919
Wed Aug 23 15:02:52 2023 Producer: put 0.2491374183362226
Wed Aug 23 15:02:52 2023 >got 0.2491374183362226
Wed Aug 23 15:02:52 2023 Producer: put 0.12323612214924151
Wed Aug 23 15:02:52 2023 >got 0.12323612214924151
Wed Aug 23 15:02:52 2023 Producer: put 0.40794186931152177
Wed Aug 23 15:02:52 2023 >got 0.40794186931152177
Wed Aug 23 15:02:53 2023 Producer: put 0.7940363416780953
Wed Aug 23 15:02:53 2023 >got 0.7940363416780953
Wed Aug 23 15:02:54 2023 Producer: put 0.9858167187791953
Wed Aug 23 15:02:54 2023 >got 0.9858167187791953
Wed Aug 23 15:02:54 2023 Producer: put 0.14664711736511993
Wed Aug 23 15:02:54 2023 >got 0.14664711736511993
Wed Aug 23 15:02:54 2023 Producer: put 0.06427579669174599
Wed Aug 23 15:02:54 2023 >got 0.06427579669174599
Wed Aug 23 15:02:55 2023 Producer: put 0.7816132531122842
Wed Aug 23 15:02:55 2023 Producer: Done
Wed Aug 23 15:02:55 2023 >got 0.7816132531122842
Wed Aug 23 15:02:55 2023 Consumer: Done
'''