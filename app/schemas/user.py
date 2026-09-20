from datetime import date

from pydantic import BaseModel, Field, field_validator

import re





class UserCreate(BaseModel):

    phone_number: str

    province_id: int | None = None

    city_id: int | None = None







class UserCityUpdate(BaseModel):

    city_id: int

    province_id: int | None = None







class UserOpportunityProfileUpdate(BaseModel):

    first_name: str

    last_name: str

    gender: str

    birth_date: date

    iban: str

    education: str | None = None

    email: str | None = None



    @field_validator("iban")
    @classmethod
    def validate_iban(
        cls,
        value: str
    ):

        if not re.match(
            r"^IR\d{24}$",
            value
        ):

            raise ValueError(
                "شماره شبا باید با IR شروع شود و شامل 24 رقم باشد"
            )


        return value







class UserResponse(BaseModel):

    id: int

    phone_number: str

    role: str

    province_id: int | None = None

    city_id: int | None = None

    city_name: str | None = None


    first_name: str | None = None

    last_name: str | None = None

    gender: str | None = None

    birth_date: date | None = None

    iban: str | None = None

    education: str | None = None

    email: str | None = None


    profile_completed: bool





    class Config:

        from_attributes = True