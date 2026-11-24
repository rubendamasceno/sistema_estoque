import pytest
from unittest.mock import Mock
from sqlalchemy.exc import SQLAlchemyError
from models import Produto
from schemas import ProdutoCreate, ProdutoUpdate
from services.produto_service import listar_produtos, criar_produto, obter_produto, excluir_produto, atualizar_produto



def test_listar_produtos(session_teste):
    produto = Produto(
        nome="Teclado",
        preco=150.00,
        estoque=10
    )
    
    session_teste.add(produto)
    session_teste.commit()

    produtos = listar_produtos(session_teste)

    assert len(produtos) == 1
    assert produtos[0].nome == "Teclado"


def test_listar_produtos_vazio(session_teste):
    produtos = listar_produtos(session_teste)

    assert produtos == []


def test_criar_produto(session_teste):
    produto_schema = ProdutoCreate(
        nome="Mouse",
        preco=80.00,
        estoque=15
    )

    produto = criar_produto(produto_schema, session_teste)

    assert produto.id is not None
    assert produto.nome == "Mouse"
    assert produto.preco == 80.00
    assert produto.estoque == 15


def test_criar_produto_erro_rollback():
    session = Mock()

    session.commit.side_effect = SQLAlchemyError()

    produto_schema = ProdutoCreate(
        nome="Teclado",
        preco=100,
        estoque=10
    )

    with pytest.raises(SQLAlchemyError):
        criar_produto(produto_schema, session)

    session.rollback.assert_called_once()


def test_obter_produto(session_teste):
    produto = Produto(
        nome="Monitor",
        preco=900.00,
        estoque=5
    )

    session_teste.add(produto)
    session_teste.commit()

    produto_encontrado = obter_produto(produto.id, session_teste)

    assert produto_encontrado is not None
    assert produto_encontrado.id == produto.id
    assert produto_encontrado.nome == "Monitor"


def test_obter_produto_inexistente(session_teste):
    produto = obter_produto(999, session_teste)

    assert produto is None


def test_excluir_produto(session_teste):
    produto = Produto(
        nome="Teclado",
        preco=150.00,
        estoque=10
    )

    session_teste.add(produto)
    session_teste.commit()

    produto_excluido = excluir_produto(produto.id, session_teste)

    assert produto_excluido is not None
    assert produto_excluido.nome == "Teclado"
    assert session_teste.query(Produto).count() == 0


def test_excluir_produto_erro_rollback():
    session = Mock()

    session.query.return_value.filter.return_value.first.return_value = Mock()

    session.commit.side_effect = SQLAlchemyError()

    with pytest.raises(SQLAlchemyError):
        excluir_produto(1, session)

    session.rollback.assert_called_once()

def test_excluir_produto_inexistente(session_teste):
    produto = excluir_produto(999, session_teste)

    assert produto is None
    assert session_teste.query(Produto).count() == 0


def test_atualizar_produto(session_teste):
    produto = Produto(
        nome="Teclado",
        preco=150.00, 
        estoque=10
    )
    
    session_teste.add(produto)
    session_teste.commit()

    produto_schema = ProdutoUpdate(
        nome="Teclado Mecânico",
        preco=250.00,
        estoque=20
    )

    produto_atualizado = atualizar_produto(
        produto.id,
        produto_schema,
        session_teste
    )

    assert produto_atualizado.nome == "Teclado Mecânico"
    assert produto_atualizado.preco == 250.00
    assert produto_atualizado.estoque == 20


def test_atualizar_produto_erro_rollback():
    session = Mock()

    session.query.return_value.filter.return_value.first.return_value = Mock()

    produto_schema = ProdutoCreate(
        nome="Mouse",
        preco=220.00,
        estoque=10
    )

    session.commit.side_effect = SQLAlchemyError()

    with pytest.raises(SQLAlchemyError):
        atualizar_produto(1, produto_schema, session)

    session.rollback.assert_called_once()


def test_atualizar_produto_inexistente(session_teste):
    produto_schema = ProdutoUpdate(
        nome="Teclado",
        preco=150.00,
        estoque=10
    )

    produto = atualizar_produto(999, produto_schema, session_teste)

    assert produto is None
