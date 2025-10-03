from pydantic import BaseModel

class VoteCreate(BaseModel):
    voter_id: int
    candidate_id: int

class VoteResponse(BaseModel):
    id: int
    voter_id: int
    candidate_id: int

    class Config:
        orm_mode = True

class VoteStatistics(BaseModel):
    candidate_id: int
    candidate_name: str
    total_votes: int
    percentage: float
