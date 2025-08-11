from enum import Enum


class PortChangeType(str, Enum):
    STATE = "state"
    SERVICE = "service"
    PRODUCT = "product"
    VERSION = "version"
