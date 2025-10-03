from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from db import get_db
from models.voter import Voter
from models.candidate import Candidate
from models.vote import Vote
from schemas.vote import VoteCreate, VoteResponse, VoteStatistics

router = APIRouter(prefix="/votes", tags=["Votes"])

# POST /votes → emitir un voto
@router.post("/", response_model=VoteResponse)
def create_vote(vote: VoteCreate, db: Session = Depends(get_db)):
    # Validar que el votante exista
    voter = db.query(Voter).filter(Voter.id == vote.voter_id).first()
    if not voter:
        raise HTTPException(status_code=404, detail="Votante no encontrado")

    # Validar que el candidato exista
    candidate = db.query(Candidate).filter(Candidate.id == vote.candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")

    # Validar que el votante no haya votado antes
    if voter.has_voted:
        raise HTTPException(status_code=400, detail="El votante ya emitió su voto")

    # Validación extra: que un votante no pueda votar por sí mismo
    if voter.name == candidate.name:
        raise HTTPException(status_code=400, detail="Un votante no puede votar por sí mismo")

    # Registrar el voto
    new_vote = Vote(voter_id=vote.voter_id, candidate_id=vote.candidate_id)
    db.add(new_vote)

    # Actualizar estado del votante y contador del candidato
    voter.has_voted = True
    candidate.votes += 1

    db.commit()
    db.refresh(new_vote)
    return new_vote


# GET /votes → listar todos los votos
@router.get("/", response_model=list[VoteResponse])
def list_votes(db: Session = Depends(get_db)):
    return db.query(Vote).all()


# GET /votes/statistics → estadísticas generales
@router.get("/statistics", response_model=list[VoteStatistics])
def get_statistics(db: Session = Depends(get_db)):
    total_votes = db.query(func.count(Vote.id)).scalar()
    if total_votes == 0:
        return []

    results = (
        db.query(
            Candidate.id.label("candidate_id"),
            Candidate.name.label("candidate_name"),
            Candidate.votes.label("total_votes"),
        ).all()
    )

    stats = []
    for r in results:
        percentage = (r.total_votes / total_votes) * 100 if total_votes > 0 else 0
        stats.append(
            VoteStatistics(
                candidate_id=r.candidate_id,
                candidate_name=r.candidate_name,
                total_votes=r.total_votes,
                percentage=round(percentage, 2),
            )
        )
    return stats


# GET /votes/top3 → top 3 candidatos más votados
@router.get("/top3", response_model=list[VoteStatistics])
def get_top3_candidates(db: Session = Depends(get_db)):
    total_votes = db.query(func.count(Vote.id)).scalar()
    if total_votes == 0:
        return []

    results = (
        db.query(
            Candidate.id.label("candidate_id"),
            Candidate.name.label("candidate_name"),
            Candidate.votes.label("total_votes"),
        )
        .order_by(Candidate.votes.desc())
        .limit(3)
        .all()
    )

    stats = []
    for r in results:
        percentage = (r.total_votes / total_votes) * 100 if total_votes > 0 else 0
        stats.append(
            VoteStatistics(
                candidate_id=r.candidate_id,
                candidate_name=r.candidate_name,
                total_votes=r.total_votes,
                percentage=round(percentage, 2),
            )
        )
    return stats


# GET /votes/participation → porcentaje de participación
@router.get("/participation")
def get_participation(db: Session = Depends(get_db)):
    total_voters = db.query(func.count(Voter.id)).scalar()
    voters_who_voted = db.query(func.count(Voter.id)).filter(Voter.has_voted == True).scalar()

    if total_voters == 0:
        return {"participation": 0.0}

    participation = (voters_who_voted / total_voters) * 100
    return {"participation": round(participation, 2)}


# GET /votes/winner → candidato ganador actual
@router.get("/winner")
def get_winner(db: Session = Depends(get_db)):
    winner = db.query(Candidate).order_by(Candidate.votes.desc()).first()
    if not winner:
        return {"message": "No hay votos registrados aún"}
    return {
        "candidate_id": winner.id,
        "candidate_name": winner.name,
        "party": winner.party,
        "votes": winner.votes,
    }


# GET /votes/by_party → distribución de votos por partido
@router.get("/by_party")
def get_votes_by_party(db: Session = Depends(get_db)):
    total_votes = db.query(func.count(Vote.id)).scalar()
    if total_votes == 0:
        return []

    results = (
        db.query(
            Candidate.party,
            func.sum(Candidate.votes).label("votes")
        )
        .group_by(Candidate.party)
        .all()
    )

    stats = []
    for r in results:
        percentage = (r.votes / total_votes) * 100 if total_votes > 0 else 0
        stats.append({
            "party": r.party if r.party else "Independiente",
            "votes": r.votes,
            "percentage": round(percentage, 2)
        })
    return stats

