from sqlalchemy import text
from db import engine

def main():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sys.databases"))
            print("Conexión exitosa. Bases de datos disponibles:")
            for row in result:
                print("-", row[0])
    except Exception as e:
        print("Error de conexión:", e)

if __name__ == "__main__":
    main()
