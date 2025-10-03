from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.voter import Voter
from models.candidate import Candidate 
from schemas.voter import VoterCreate, VoterResponse

router = APIRouter(prefix="/voters", tags=["Voters"])

# POST /voters → registrar un nuevo votante
@router.post("/", response_model=VoterResponse)
def create_voter(voter: VoterCreate, db: Session = Depends(get_db)):
    # Validar que no exista ya como votante
    existing_voter = db.query(Voter).filter(Voter.email == voter.email).first()
    if existing_voter:
        raise HTTPException(status_code=400, detail="El email ya está registrado como votante")

    # Validar que no exista como candidato
    existing_candidate = db.query(Candidate).filter(Candidate.name == voter.name).first()
    if existing_candidate:
        raise HTTPException(status_code=400, detail="Este nombre ya está registrado como candidato")

    new_voter = Voter(name=voter.name, email=voter.email)
    db.add(new_voter)
    db.commit()
    db.refresh(new_voter)
    return new_voter

# GET /voters → listar todos los votantes
@router.get("/", response_model=list[VoterResponse])
def list_voters(db: Session = Depends(get_db)):
    return db.query(Voter).all()

# GET /voters/{id} → obtener un votante por ID
@router.get("/{id}", response_model=VoterResponse)
def get_voter(id: int, db: Session = Depends(get_db)):
    voter = db.query(Voter).filter(Voter.id == id).first()
    if not voter:
        raise HTTPException(status_code=404, detail="Votante no encontrado")
    return voter

# DELETE /voters/{id} → eliminar un votante
@router.delete("/{id}")
def delete_voter(id: int, db: Session = Depends(get_db)):
    voter = db.query(Voter).filter(Voter.id == id).first()
    if not voter:
        raise HTTPException(status_code=404, detail="Votante no encontrado")
    db.delete(voter)
    db.commit()
    return {"message": "Votante eliminado correctamente"}


