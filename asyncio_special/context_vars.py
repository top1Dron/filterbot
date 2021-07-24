import asyncio
from contextvars import ContextVar


MyCounter = ContextVar('counter', default=0)



async def increase():
    my_conter = MyCounter.get()
    my_conter += 1
    MyCounter.set(my_conter)


async def count():
    while True:
        await increase()
        my_counter = MyCounter.get()
        print(f'Счётчик: {my_counter}')
        await asyncio.sleep(1 / 10)


asyncio.run(count())