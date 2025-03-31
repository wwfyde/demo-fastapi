import redis as redis_sync
import redis.asyncio as redis

from demo_fastapi.core.config import settings

# 使其为全局变量
pool = redis.ConnectionPool.from_url(
    settings.redis_dsn,
    decode_responses=True,
    protocol=3,
    health_check_interval=2,
    retry_on_timeout=True,
    max_connections=10,
)
# 同步池
pool_sync = redis_sync.Redis(
    settings.redis_dsn, decode_responses=True, protocol=3, health_check_interval=2
)
