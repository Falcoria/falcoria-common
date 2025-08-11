from enum import Enum


class NmapTasks(str, Enum):
    NMAP_SCAN = "project.nmap.scan"
    NMAP_CANCEL = "project.nmap.cancel"


class WorkerTasks(str, Enum):
    UPDATE_WORKER_IP = "worker.update_ip"