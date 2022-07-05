import asyncio


async def helper(x, sorted_seq):
    await asyncio.sleep(x / 1_000)
    sorted_seq.append(x)


async def sleep_sort(seq):
    tasks = set()
    sorted_seq = []
    for x in seq:
        tasks.add(asyncio.create_task(helper(x, sorted_seq)))
    for task in tasks:
        await task
    return sorted_seq


def main(seq):
    return asyncio.run(sleep_sort(seq))
