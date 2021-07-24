import asyncio


async def count(counter):
    print(f'Количество записей в списке: {len(counter)}')
    while True:
        await asyncio.sleep(1 / 1000)
        counter.append(1)


async def print_every_one_sec(counter):
    while True:
        await asyncio.sleep(1)
        print(f'- 1 секунда прошла. '
              f'Количество записей в списке: {len(counter)}')


async def print_every_five_sec():
    while True:
        await asyncio.sleep(5)
        print(f'----- 5 секунд прошло. ')


async def print_every_ten_sec():
    while True:
        await asyncio.sleep(10)
        print(f'---------- 10 секунд прошло. ')


async def main():
    counter = []

    tasks = [
        count(counter),
        print_every_one_sec(counter),
        print_every_five_sec(),
        print_every_ten_sec(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
