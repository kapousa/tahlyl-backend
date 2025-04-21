from pydantic import BaseModel

class ToneBase(BaseModel):
    tone: str

class ToneCreate(ToneBase):
    pass

class ToneUpdate(ToneBase):
    pass

class Tone(ToneBase):
    id: str

    class Config:
        orm_mode = True