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
        key = RedisKeyBuilder.lock_ip_ports_key(project_id, ip, ports)
        was_set = await self.redis.set(key, "1", ex=ttl_seconds, nx=True)
        return was_set is True
    
    async def release_lock_ip_ports(self, project_id: str, ip: str, ports: str):
        key = RedisKeyBuilder.lock_ip_ports_key(project_id, ip, ports)
        await self.redis.delete(key)




    async def track_task_id(self, task_id: str):
        key = RedisKeyBuilder.task_ids_key(self.project)
        await self.redis.rpush(key, task_id)

    async def get_task_ids(self):
        key = RedisKeyBuilder.task_ids_key(self.project)
        return await self.redis.lrange(key, 0, -1)

    async def remove_task_id(self, task_id: str):
        key = RedisKeyBuilder.task_ids_key(self.project)
        await self.redis.lrem(key, 0, task_id)

    async def track_ip_task(self, ip: str, task_id: str):
        key = RedisKeyBuilder.ip_task_map_key(self.project)
        await self.redis.hset(key, ip, task_id)

    async def get_ip_task_map(self):
        key = RedisKeyBuilder.ip_task_map_key(self.project)
        return await self.redis.hgetall(key)

    async def remove_ip_task(self, ip: str):
        key = RedisKeyBuilder.ip_task_map_key(self.project)
        await self.redis.hdel(key, ip)

    async def get_running_targets_raw(self):
        key = RedisKeyBuilder.running_targets_key(self.project)
        entries = await self.redis.lrange(key, 0, -1)
        return [json.loads(e.decode() if isinstance(e, bytes) else e) for e in entries]

    async def track_pid_entry(self, tool: str, pid: int, hostname: str):
        key = RedisKeyBuilder.pid_tracking_key(tool, hostname, pid)
        await self.redis.set(key, self.project)

    async def remove_pid_entry(self, tool: str, pid: int, hostname: str):
        key = RedisKeyBuilder.pid_tracking_key(tool, hostname, pid)
        await self.redis.delete(key)

    async def get_all_pid_keys(self, tool: str, hostname: str):
        pattern = RedisKeyBuilder.pid_tracking_key(tool, hostname, "*")
        return await self.redis.keys(pattern)

    async def release_lock(self, key: str):
        await self.redis.delete(f"lock:{key}")

    async def get_project_task_ids(self) -> list[str]:
        key = RedisKeyBuilder.project_task_ids_key(self.project)
        task_ids = await self.redis.smembers(key)
        return [tid.decode() if isinstance(tid, bytes) else tid for tid in task_ids]
        

class BaseRedisTracker:
    def __init__(self, project: str, redis_client: SyncRedis):
        self.project = project
        self.redis = redis_client

    def store_running_target_nmap(self, task_id: str, target: RunningNmapTarget):
        key = RedisKeyBuilder.running_targets_key


    def track_task_id(self, task_id: str):
        key = RedisKeyBuilder.task_ids_key(self.project)
        self.redis.rpush(key, task_id)

    def get_task_ids(self):
        key = RedisKeyBuilder.task_ids_key(self.project)
        return self.redis.lrange(key, 0, -1)

    def remove_task_id(self, task_id: str):
        key = RedisKeyBuilder.task_ids_key(self.project)
        self.redis.lrem(key, 0, task_id)

    def track_ip_task(self, ip: str, task_id: str):
        key = RedisKeyBuilder.ip_task_map_key(self.project)
        self.redis.hset(key, ip, task_id)

    def get_ip_task_map(self):
        key = RedisKeyBuilder.ip_task_map_key(self.project)
        return self.redis.hgetall(key)

    def remove_ip_task(self, ip: str):
        key = RedisKeyBuilder.ip_task_map_key(self.project)
        self.redis.hdel(key, ip)

    def acquire_ip_lock(self, ip: str, ttl_seconds: int = 300) -> bool:
        key = RedisKeyBuilder.ip_lock_key(self.project, ip)
        was_set = self.redis.set(key, "1", ex=ttl_seconds, nx=True)
        return was_set is True

    def release_ip_lock(self, ip: str):
        key = RedisKeyBuilder.ip_lock_key(self.project, ip)
        self.redis.delete(key)
