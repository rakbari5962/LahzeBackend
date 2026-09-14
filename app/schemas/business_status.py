from enum import Enum

from pydantic import BaseModel





class BusinessStatusEnum(str, Enum):

    DRAFT = "DRAFT"

    PROFILE_INCOMPLETE = "PROFILE_INCOMPLETE"

    READY = "READY"

    ACTIVE = "ACTIVE"

    SUSPENDED = "SUSPENDED"







class BusinessStatusUpdate(BaseModel):

    status: BusinessStatusEnum