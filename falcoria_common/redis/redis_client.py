from redis.asyncio import Redis as AsyncRedis
from redis import Redis as SyncRedis


class FalcoriaRedisClient:
    @staticmethod
    def create_async_redis(host: str, port: int, db: int, password: str) -> AsyncRedis:
        return AsyncRedis(
            host=host,
            port=port,
            db=db,
            password=password
        )

    @staticmethod
    def create_sync_redis(host: str, port: int, db: int, password: str) -> SyncRedis:
        return SyncRedis(
            host=host,
            port=port,
            db=db,
            password=password
        )