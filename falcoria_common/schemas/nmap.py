import json

from uuid import UUID
from typing import List, Optional
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from .enums import ImportMode, NmapTaskStatus


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