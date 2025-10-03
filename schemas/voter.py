from pydantic import BaseModel, EmailStr

class VoterCreate(BaseModel):
    name: str
    email: EmailStr

class VoterResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    has_voted: bool

    class Config:
        orm_mode = True
