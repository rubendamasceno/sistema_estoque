import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db import Base
import models

@pytest.fixture # Disponibiliza a sessão de teste para as funções
def session_teste():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False}, # Desativa a vrificação de trheads
        poolclass=StaticPool # Reutiliza a mesma conexão do banco de teste
    )

    Base.metadata.create_all(bind=engine)

    SessionTeste = sessionmaker(bind=engine)

    session = SessionTeste()

    try:
        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=engine) # Limpeza das tabelas no banco
        engine.dispose() # Libera os recursos de engine  