from pydantic import BaseModel

class CandidateCreate(BaseModel):
    name: str
    party: str | None = None

class CandidateResponse(BaseModel):
    id: int
    name: str
    party: str | None
    votes: int

    class Config:
        orm_mode = True

