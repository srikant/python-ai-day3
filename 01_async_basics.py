import asyncio

import time

def sync_task(name, delay):
    print(f"Task {name} started")
    time.sleep(delay)
    print(f"Task {name} finished")

async def async_task(name, delay):
    print(f"Task {name} started")
    await asyncio.sleep(delay)
    print(f"Task {name} finished")


def run_sync():
    print("===Sync Tasks===")
    start = time.time()
    sync_task("A", 2)
    sync_task("B", 2)
    sync_task("C", 2)
    end = time.time()
    print(f"Total time: {end - start}")

async def run_async():
    print("===Async Tasks===")
    start = time.time()
    await asyncio.gather(
        async_task("A", 2),
        async_task("B", 2),
        async_task("C", 2)
    )
    end = time.time()
    print(f"Total time: {end - start}")


if __name__ == "__main__":
    run_sync()
    asyncio.run(run_async())