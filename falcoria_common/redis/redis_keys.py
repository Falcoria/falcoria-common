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
    def worker_key(hostname: str) -> str:
        return f"worker:{hostname}"

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