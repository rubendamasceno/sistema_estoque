import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from dependencies import pegar_sessao, verificar_admin
from db import Base
from models import Usuario, Produto, Pedido, ItemPedido


@pytest.fixture # Disponibiliza a sessão de teste para as funções
def session_teste():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False}, # Desativa a verificação de trheads
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


@pytest.fixture
def cliente(session_teste):
    def pegar_sessao_teste():
        yield session_teste

    def verificar_admin_teste():
        admin = Usuario(
            nome="admin",
            email="admin@gmail.com",
            senha="12345678",
            admin=True
        )
        return admin

    app.dependency_overrides[pegar_sessao] = pegar_sessao_teste

    try:
        with TestClient(app) as cliente:
            yield cliente

    finally:
        app.dependency_overrides.clear()


@pytest.fixture
def usuario_autenticado(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == 200

    login = cliente.post("/usuarios/login", json={
    "email": "teste@gmail.com",
    "senha": "12345678"
    })

    assert login.status_code == 200

    access_token = login.json()["access_token"]

    cliente.headers.update({
        "Authorization": f"Bearer {access_token}"
    })

    return cliente


@pytest.fixture
def usuario_admin(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "Adm",
        "email": "adm@gmail.com",
        "senha": "12345678",
        "admin": True
    })

    assert usuario.status_code == 200

    login = cliente.post("/usuarios/login", json={
        "email": "adm@gmail.com",
        "senha": "12345678"
    })

    assert login.status_code == 200
    
    access_token = login.json()["access_token"]

    cliente.headers.update({
        "Authorization": f"Bearer {access_token}"
    })

    return cliente