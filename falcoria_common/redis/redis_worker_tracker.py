from redis.asyncio.client import Redis as AsyncRedis

from falcoria_common.redis.redis_keys import RedisKeyBuilder


class RedisWorkerTracker:
    def __init__(self, redis_client: AsyncRedis):
        self.redis = redis_client

    async def get_worker_data_raw(self) -> dict[str, dict[str, str]]:
        """
        Returns raw worker data from Redis hashes:
        {
            hostname: {
                "ip": "...",
                "last_updated": "...",
                "last_seen": "..."
            }
        }
        """
        result: dict[str, dict[str, str]] = {}
        keys = await self.redis.keys(RedisKeyBuilder.worker_key("*"))

        for key in keys:
            hostname = key.decode().split(":", 1)[1]
            raw_fields = await self.redis.hgetall(key)
            if raw_fields:
                result[hostname] = {k.decode(): v.decode() for k, v in raw_fields.items()}

        return result