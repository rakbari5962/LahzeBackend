from pydantic import BaseModel


class ProvinceResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True