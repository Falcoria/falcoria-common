from typing import List, Optional

from pydantic import BaseModel, Field

from falcoria_common.schemas.port import Port


class BaseIP(BaseModel):
    status: Optional[str] = ""
    os: Optional[str] = ""
    starttime: Optional[int] = None
    endtime: Optional[int] = None
    hostnames: Optional[List[str]] = []
    #ports: Optional[List[Port]] = []   # define ports in the derived class