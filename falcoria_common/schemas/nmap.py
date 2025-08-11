from uuid import UUID
from typing import List

from pydantic import BaseModel, Field

from falcoria_common.schemas.enums.common import ImportMode


class TaskUser(BaseModel):
    id: UUID | str
    username: str


class NmapTask(BaseModel):
    """Used for sending nmap tasks from tasker to workers via RabbitMQ."""
    ip: str
    hostnames: List[str] = Field(
        default_factory=list,
        description="List of hostnames associated with the target IP"
    )
    project: UUID
    open_ports_opts: str
    service_opts: str
    timeout: int
    include_services: bool
    mode: ImportMode
    user: TaskUser
    open_ports_str: str
    track_history: bool


class RunningNmapTarget(BaseModel):
    """Used for tracking running nmap tasks on workers."""
    ip: str
    hostnames: list[str]
    worker: str
    started_at: int


class NmapTaskMetadata(BaseModel):
    """Metadata for nmap tasks in Redis Queue."""
    ip: str
    open_ports: str


class NmapRunningTarget(BaseModel):
    ip: str
    hostnames: list[str]
    worker: str
    started_at: int


class NmapTaskSummary(BaseModel):
    active_or_queued: int
    running: int
    running_targets: List[NmapRunningTarget]


class ServiceOptsBase(BaseModel):
    aggressive_scan: bool = Field(default=False, description="Enable aggressive scan mode (-A)")
    default_scripts: bool = Field(default=False, description="Use default Nmap scripts (-sC)")
    os_detection: bool = Field(default=False, description="Enable OS detection (-O)")
    traceroute: bool = Field(default=False, description="Trace hop path to each host (--traceroute)")


class RunNmapRequestBase(BaseModel):
    hosts: List[str]
    #open_ports_opts: OpenPortsOpts
    #service_opts: ServiceOpts
    timeout: int = Field(..., ge=1, le=60*60*24, description="Timeout in seconds for the scan")
    include_services: bool = Field(..., description="Include service detection in the scan")
    mode: ImportMode = Field(..., description="Import mode for the scan results")
    track_history: bool = True