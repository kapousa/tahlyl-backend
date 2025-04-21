from pydantic import BaseModel


class Beneficiary(BaseModel):
    id: int
    name: str
