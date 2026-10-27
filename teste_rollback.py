from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from db import db
from models import Usuario

Session = sessionmaker(bind=db)
session = Session()

try:
    usuario = Usuario(
        "Teste Rollback",
        "teste3@gmail.com",
        "hash_de_teste"
    )

    session.add(usuario)
    session.commit()

    print("A operação foi concluída.")

except IntegrityError:
    print("O banco rejeitou o cadastro.")
    session.rollback()
    print("Rollback executado.")

    usuarios = session.query(Usuario).all()
    print(f"Sessão reutilizada. Usuários encontrados: {len(usuarios)}")

finally:
    session.close()
