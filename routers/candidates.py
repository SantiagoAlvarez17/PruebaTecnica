from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.candidate import Candidate
from models.voter import Voter
from schemas.candidate import CandidateCreate, CandidateResponse

router = APIRouter(prefix="/candidates", tags=["Candidates"])

# POST /candidates → registrar un nuevo candidato
@router.post("/", response_model=CandidateResponse)
def create_candidate(candidate: CandidateCreate, db: Session = Depends(get_db)):
    # Validar que no exista un candidato con el mismo nombre
    existing_candidate = db.query(Candidate).filter(Candidate.name == candidate.name).first()
    if existing_candidate:
        raise HTTPException(status_code=400, detail="El candidato ya está registrado")

    # Validar que no exista como votante
    existing_voter = db.query(Voter).filter(Voter.name == candidate.name).first()
    if existing_voter:
        raise HTTPException(status_code=400, detail="Este nombre ya está registrado como votante")

    new_candidate = Candidate(name=candidate.name, party=candidate.party)
    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)
    return new_candidate

# GET /candidates → listar todos los candidatos
@router.get("/", response_model=list[CandidateResponse])
def list_candidates(db: Session = Depends(get_db)):
    return db.query(Candidate).all()

# GET /candidates/{id} → obtener un candidato por ID
@router.get("/{id}", response_model=CandidateResponse)
def get_candidate(id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    return candidate

# DELETE /candidates/{id} → eliminar un candidato
@router.delete("/{id}")
def delete_candidate(id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    db.delete(candidate)
    db.commit()
    return {"message": "Candidato eliminado correctamente"}
