from fastapi import FastAPI
from routers import voters, votes
from routers import candidates


app = FastAPI(title="Sistema de Votaciones")

# Registrar routers
app.include_router(voters.router)
app.include_router(candidates.router)
app.include_router(votes.router)
