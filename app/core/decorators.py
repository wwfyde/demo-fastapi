import asyncio
import time
from functools import wraps


def time_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")
        return result

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {elapsed_time:.4f} seconds")
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return wrapper


@time_decorator
def sleep(seconds):
    time.sleep(seconds)


@time_decorator
async def sleep_async(seconds):
    await asyncio.sleep(seconds)


if __name__ == "__main__":

    sleep(5)
    asyncio.run(sleep_async(5))
