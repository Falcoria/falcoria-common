from redis.asyncio.client import Redis as AsyncRedis

from falcoria_common.redis.redis_keys import RedisKeyBuilder


class RedisWorkerTracker:
    def __init__(self, redis_client: AsyncRedis):
        self.redis = redis_client

    async def get_worker_ips_raw(self) -> dict[str, str]:
        """
        Returns raw worker IP data:
        {
            hostname: <raw Redis value as string>
        }
        """
        result = {}
        keys = await self.redis.keys(RedisKeyBuilder.worker_ip_key("*"))

        for key in keys:
            hostname = key.decode().split(":", 1)[1]
            raw_value = await self.redis.get(key)
            if raw_value:
                result[hostname] = raw_value.decode()

        return result