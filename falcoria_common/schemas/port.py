from typing import Optional, List

from pydantic import BaseModel, Field

from falcoria_common.schemas.enums.port import ProtocolEnum, PortState


class PortBase(BaseModel):
    protocol: ProtocolEnum = Field(default=ProtocolEnum.tcp)
    state: PortState = Field(default=PortState.open)
    reason: Optional[str] = None
    service: Optional[str] = Field(default="", description="Service name (e.g., http, ssh)")
    product: Optional[str] = Field(default="", description="Service product (e.g., OpenSSH, nginx)")
    version: Optional[str] = Field(default="", description="Service version (e.g., 7.9p1, 1.18.0)")
    extrainfo: Optional[str] = Field(default="", description="Additional information about the service")
    cpe: Optional[List[str]] = Field(default_factory=list, description="List of detected CPEs")
    servicefp: Optional[str] = None
    scripts: Optional[dict] = Field(default_factory=dict, description="Structured script output")


class PortNumber(BaseModel):
    number: int = Field(
        ge=0,
        le=65535,
        description="The port number, ranging from 0 to 65535."
    )


class Port(PortBase, PortNumber):
    """Represents a network port with its attributes."""
    pass