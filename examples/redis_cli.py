import asyncio

import redis.asyncio as redis


async def get_redis_connection():
    pool = redis.ConnectionPool(
        decode_responses=True,
        protocol=3

    )
    return redis.Redis(connection_pool=pool, decode_responses=True, protocol=3)


async def main():
    r = await get_redis_connection()
    async with r:
        await r.set('a', 'my-value你好', )
        print(await r.get('a'))


if __name__ == '__main__':
    asyncio.run(main(), debug=True)
