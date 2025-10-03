from db import engine
from models.base import Base
from models.voter import Voter
from models.candidate import Candidate
from models.vote import Vote

def main():
    # Esto NO crea tablas nuevas porque ya existen en SQL Server,
    # pero valida que el mapeo ORM es correcto.
    Base.metadata.create_all(bind=engine)
    print("Modelos cargados correctamente y sincronizados con la BD.")

if __name__ == "__main__":
    main()
