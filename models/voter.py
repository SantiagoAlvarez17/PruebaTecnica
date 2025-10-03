from sqlalchemy import Column, Integer, String, Boolean
from .base import Base

class Voter(Base):
    __tablename__ = "Voters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    has_voted = Column(Boolean, default=False, nullable=False)
