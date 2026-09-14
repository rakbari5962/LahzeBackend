from pydantic import BaseModel





class BusinessProfileUpdate(BaseModel):

    description: str | None = None

    phone: str | None = None