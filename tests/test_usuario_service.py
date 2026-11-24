import pytest
from unittest.mock import Mock
from sqlalchemy.exc import SQLAlchemyError
from services.usuario_service import obter_usuario, autenticar_usuario, listar_usuarios, criar_usuario, excluir_usuario, atualizar_usuario
from schemas import UsuarioCreate, UsuarioUpdate
from models import Usuario


def test_listar_usuarios(session_teste):
    usuario = Usuario(
        nome="teste",
        email="teste@gmail.com",
        senha="senha_hash"
    )
    session_teste.add(usuario)
    session_teste.commit()

    usuarios = listar_usuarios(session_teste)

    assert len(usuarios) == 1
    assert usuarios[0].nome == "teste"


def test_listar_usuarios_vazio(session_teste):
    usuarios = listar_usuarios(session_teste)

    assert usuarios == []


def test_obter_usuario(session_teste):
    usuario = Usuario(
        nome="teste",
        email="teste@gmail.com",
        senha="senha_hash"
    )
    session_teste.add(usuario)
    session_teste.commit()

    usuario_encontrado = obter_usuario(usuario.id, session_teste)

    assert usuario_encontrado is not None
    assert usuario_encontrado.id == usuario.id
    assert usuario_encontrado.nome == "teste"


def test_obter_usuario_inexistente(session_teste):
    usuario = obter_usuario(999, session_teste)

    assert usuario is None


def test_autenticar_usuario(session_teste):
    usuario = Usuario(
        nome="teste",
        email="teste@gmail.com",
        senha="senha_hash"
    )
    session_teste.add(usuario)
    session_teste.commit()

    usuario_encontrado = autenticar_usuario(
        "teste@gmail.com",
        session_teste
    )

    assert usuario_encontrado is not None
    assert usuario_encontrado.email == "teste@gmail.com"


def test_autenticar_usuario_inexistente(session_teste):
    usuario = autenticar_usuario("inexistente@gmail.com", session_teste)

    assert usuario is None


def test_criar_usuario(session_teste):
    usuario_schema = UsuarioCreate(
        nome="teste",
        email="teste@gmail.com",
        senha="12345678"
    )

    usuario = criar_usuario(usuario_schema, session_teste)

    assert usuario.id is not None
    assert usuario.nome == "teste"
    assert usuario.email == "teste@gmail.com"
    assert usuario.senha != "12345678"

    usuario_banco = session_teste.query(Usuario).first()
    assert usuario_banco is not None


def test_criar_usuario_email_existente(session_teste):
    usuario_schema = UsuarioCreate(
        nome="teste",
        email="teste@gmail.com",
        senha="12345678"
    )

    criar_usuario(usuario_schema, session_teste)

    usuario_duplicado = criar_usuario(usuario_schema, session_teste)

    assert usuario_duplicado is False
    assert session_teste.query(Usuario).count() == 1


def test_criar_usuario_erro_rollback():
    session = Mock()

    session.query.return_value.filter.return_value.first.return_value = None

    session.commit.side_effect = SQLAlchemyError()

    usuario_schema = UsuarioCreate(
        nome="Teste",
        email="teste@gmail.com",
        senha="12345678"
    )

    with pytest.raises(SQLAlchemyError):
        criar_usuario(usuario_schema, session)

    session.rollback.assert_called_once()


def test_excluir_usuario(session_teste):
    usuario = Usuario(
        nome="teste",
        email="teste@gmail.com",
        senha="senha_hash"
    )
    session_teste.add(usuario)
    session_teste.commit()

    usuario_excluido = excluir_usuario(usuario.id, session_teste)

    assert usuario_excluido is not None
    assert usuario_excluido.email == "teste@gmail.com"
    assert session_teste.query(Usuario).count() == 0


def test_excluir_usuario_inexistente(session_teste):
    usuario = excluir_usuario(999, session_teste)

    assert usuario is None
    assert session_teste.query(Usuario).count() == 0


def test_atualizar_usuario(session_teste):
    usuario = Usuario(
        nome="teste",
        email="teste@gmail.com",
        senha="senha_hash"
    )
    session_teste.add(usuario)
    session_teste.commit()

    usuario_schema = UsuarioUpdate(
        nome="Teste",
        email="teste.novo@gmail.com"
    )

    usuario_atualizado = atualizar_usuario(
        usuario.id,
        usuario_schema,
        session_teste
    )

    assert usuario_atualizado.nome == "Teste"
    assert usuario_atualizado.email == "teste.novo@gmail.com"


def test_excluir_usuario_erro_rollback():
    session = Mock()

    session.commit.side_effect = SQLAlchemyError()

    session.query.return_value.filter.return_value.first.return_value = Mock()

    with pytest.raises(SQLAlchemyError):
        excluir_usuario(1, session)

    session.rollback.assert_called_once()


def test_atualizar_usuario_inexistente(session_teste):
    usuario_schema = UsuarioUpdate(
        nome="Teste",
        email="teste.novo@gmail.com"
    )

    usuario = atualizar_usuario(999, usuario_schema, session_teste)

    assert usuario is None


def test_atualizar_usuario_email_existente(session_teste):
    usuario1 = Usuario(
        nome="teste1",
        email="teste1@gmail.com",
        senha="senha_hash"
    )

    usuario2 = Usuario(
        nome="teste2",
        email="teste2@gmail.com",
        senha="senha_hash"
    )

    session_teste.add_all([usuario1, usuario2])
    session_teste.commit()

    usuario_schema = UsuarioUpdate(
        nome="Teste",
        email="teste2@gmail.com"
    )

    usuario_atualizado = atualizar_usuario(
        usuario1.id,
        usuario_schema,
        session_teste
    )

    assert usuario_atualizado is False

    usuario_banco = session_teste.query(Usuario).filter(Usuario.id == usuario1.id).first()

    assert usuario_banco.email == "teste1@gmail.com"


def test_atualizar_usuario_erro_rollback():
    session = Mock()

    session.commit.side_effect = SQLAlchemyError()

    session.query.return_value.filter.return_value.first.side_effect = [Mock(), None]

    usuario_schema = UsuarioUpdate(
        nome="teste",
        email="teste@gmail.com",
        senha="12345678"
    )

    with pytest.raises(SQLAlchemyError):
        atualizar_usuario(1, usuario_schema, session)

    session.rollback.assert_called_once()
