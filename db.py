from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está definida en el archivo .env")

# Crear motor de conexión
engine = create_engine(
    DATABASE_URL,
    echo=True,              # Muestra las consultas SQL en consola
    pool_pre_ping=True,
    pool_recycle=1800,
    fast_executemany=True
)

# Sesiones
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Dependencia para inyección en FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
