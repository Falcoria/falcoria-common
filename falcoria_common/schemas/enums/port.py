from enum import Enum


class ProtocolEnum(str, Enum):
    tcp = "tcp"
    udp = "udp"


class PortState(str, Enum):
    open = "open"
    closed = "closed"
    filtered = "filtered"
    unfiltered = "unfiltered"
    open_filtered = "open|filtered"
    closed_filtered = "closed|filtered"