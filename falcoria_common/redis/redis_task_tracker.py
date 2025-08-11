import json
from redis.asyncio.client import Redis as AsyncRedis
from redis.client import Redis as SyncRedis

from falcoria_common.redis.redis_keys import RedisKeyBuilder
from falcoria_common.schemas.nmap import RunningNmapTarget


class BaseAsyncRedisTracker:
    def __init__(self, project: str, redis_client: AsyncRedis):
        self.project = project
        self.redis = redis_client
    
    async def acquire_lock_ip_ports(self, project_id: str, ip: str, ports: str, ttl_seconds: int) -> bool:
        """Acquire a lock for a specific IP and ports in a project."""
        key = RedisKeyBuilder.lock_ip_ports_key(project_id, ip, ports)
        was_set = await self.redis.set(key, "1", ex=ttl_seconds, nx=True)
        return was_set is True
    
    async def release_lock_ip_ports(self, project_id: str, ip: str, ports: str):
        """Release the lock for a specific IP and ports in a project."""
        key = RedisKeyBuilder.lock_ip_ports_key(project_id, ip, ports)
        await self.redis.delete(key)

    async def get_ip_task_map(self):
        """Get the mapping of IPs to task IDs for the project."""
        key = RedisKeyBuilder.ip_task_map_key(self.project)
        return await self.redis.hgetall(key)

    async def get_running_targets_raw(self):
        key = RedisKeyBuilder.running_targets_key(self.project)
        entries = await self.redis.lrange(key, 0, -1)
        return [json.loads(e.decode() if isinstance(e, bytes) else e) for e in entries]
  

class BaseRedisTracker:
    def __init__(self, project: str, redis_client: SyncRedis):
        self.project = project
        self.redis = redis_client

    def remove_ip_task(self, ip: str):
        key = RedisKeyBuilder.ip_task_map_key(self.project)
        self.redis.hdel(key, ip)

    def release_ip_lock(self, ip: str):
        key = RedisKeyBuilder.ip_lock_key(self.project, ip)
        self.redis.delete(key)