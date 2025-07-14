import json


class RedisKeyBuilder:
    @staticmethod
    def lock_ip_ports_key(project_id: str, ip: str, ports: str) -> str:
        return f"lock:project:{project_id}:ip:{ip}:ports:{ports}"

    @staticmethod
    def project_task_ids_key(project_id: str) -> str:
        return f"project:{project_id}:task_ids"

    @staticmethod
    def user_task_ids_key(user_id: str) -> str:
        return f"user:{user_id}:task_ids"

    @staticmethod
    def project_ip_task_ids_key(project_id: str, ip: str) -> str:
        return f"project:{project_id}:ip:{ip}:task_ids"
    
    @staticmethod
    def task_metadata_nmap_key(task_id: str) -> str:
        return f"task:{task_id}:metadata:nmap"

    @staticmethod
    def worker_ip_key(hostname: str) -> str:
        return f"worker_ip:{hostname}"

    @staticmethod
    def running_tasks_key(task_id: str, hostname: str) -> str:
        return f"running:task:{task_id}:host:{hostname}"

    @staticmethod
    def running_tool_key(tool: str, hostname: str) -> str:
        """ Returns a key for tracking running tools on a specific host. Worker only"""
        return f"running:tool:{tool}:host:{hostname}"


    @staticmethod
    def task_ids_key(project: str) -> str:
        return f"project:{project}:task_ids"
    
    @staticmethod
    def ip_task_map_key(project: str) -> str:
        return f"project:{project}:ip_task_map"
    
    @staticmethod
    def ip_lock_key(project: str, ip: str) -> str:
        return f"project:{project}:ip_task_lock:{ip}"
    
    @staticmethod
    def running_targets_key(project: str) -> str:
        return f"project:{project}:running_targets"
    
    @staticmethod
    def worker_ip_pattern() -> str:
        return "worker_ip:*"
    
    @staticmethod
    def pid_tracking_key(tool: str, hostname: str, pid: int) -> str:
        return f"running:{tool}:{hostname}:{pid}"
    
    @staticmethod
    def task_metadata_key(task_id: str) -> str:
        return f"task:{task_id}"




class RedisValueBuilder:
    @staticmethod
    def pid_entry(pid: int, hostname: str) -> str:
        """ Creates a JSON string representing a PID entry. """
        return json.dumps({"pid": pid, "host": hostname})
    
    @staticmethod
    def parse_pid_entry(entry) -> dict | None:
        """ Parses a PID entry from Redis. Used by workers to identify themselves. """
        try:
            if isinstance(entry, bytes):
                entry = entry.decode()
            info = json.loads(entry)
            if not isinstance(info, dict) or "host" not in info or "pid" not in info:
                return None
            return info
        except Exception:
            return None