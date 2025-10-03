from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class Vote(Base):
    __tablename__ = "Votes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    voter_id = Column(Integer, ForeignKey("Voters.id"), nullable=False, unique=True)
    candidate_id = Column(Integer, ForeignKey("Candidates.id"), nullable=False)
