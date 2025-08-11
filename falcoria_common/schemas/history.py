from pydantic import BaseModel

from falcoria_common.schemas.enums.history import PortChangeType


class IPPortHistoryOut(BaseModel):
    ip: str
    port: int
    protocol: str
    change_type: PortChangeType
    old_value: str | None = None
    new_value: str | None = None
    created_at: int