from pydantic import BaseModel

class ToneBase(BaseModel):
    id: str
    tone: str

class ToneCreate(ToneBase):
    pass


class ToneUpdate(ToneBase):
    pass

class Tone(ToneBase):
    pass

    class Config:
        orm_mode = True