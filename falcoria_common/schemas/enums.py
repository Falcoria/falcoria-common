from enum import Enum


class ImportMode(str, Enum):
    INSERT = "insert"
    REPLACE = "replace"
    UPDATE = "update"
    APPEND = "append"


class TaskNames(str, Enum):
    NMAP_SCAN = "project.nmap.scan"
    NMAP_CANCEL = "project.nmap.cancel"
    UPDATE_WORKER_IP = "worker.update_ip"


class NmapTaskStatus(str, Enum):
    QUEUED = "queued"
    RECEIVED = "received"
    EXECUTING = "executing"
    PORTS_SCAN = "ports_scan"
    SERVICE_SCAN = "service_scan"
    COMPLETED = "completed"
    FAILED = "failed"