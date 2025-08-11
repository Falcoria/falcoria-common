from enum import Enum


class NmapTaskStatus(str, Enum):
    QUEUED = "queued"
    RECEIVED = "received"
    EXECUTING = "executing"
    PORTS_SCAN = "ports_scan"
    SERVICE_SCAN = "service_scan"
    COMPLETED = "completed"
    FAILED = "failed"
