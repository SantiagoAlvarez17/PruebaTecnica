from sqlalchemy import Column, Integer, String
from .base import Base

class Candidate(Base):
    __tablename__ = "Candidates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    party = Column(String(120), nullable=True)
    votes = Column(Integer, default=0, nullable=False)
