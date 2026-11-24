import pytest
from unittest.mock import Mock
from sqlalchemy.exc import SQLAlchemyError
from models import Usuario, Produto, Pedido
from schemas import PedidoCreate, ItemPedidoCreate
from services.pedido_service import criar_pedido


@pytest.fixture
def usuario_teste(session_teste):
     usuario = Usuario(
         nome="teste",
         email="teste@gmail.com",
         senha="12345678"
     )

     session_teste.add(usuario)
     session_teste.commit()

     return usuario


def test_criar_pedido(usuario_teste, session_teste):
    usuario = usuario_teste

    produto = Produto(
        nome="Teclado",
        preco=220.00,
        estoque=10
    )

    session_teste.add(produto)
    session_teste.commit()

    pedido_schema = PedidoCreate(
        itens = [
            ItemPedidoCreate(
                id_produto=produto.id,
                quantidade=10
            )
        ]
    )

    pedido = criar_pedido(
        pedido_schema,
        usuario,
        session_teste
    )

    assert pedido is not None
    assert produto.estoque == 0
    assert session_teste.query(Pedido).filter(Pedido.id==pedido.id).first()


def test_criar_pedido_erro_rollback():
    session = Mock()
    usuario_autenticado = Mock()
    usuario_autenticado.id = 1

    session.commit.side_effect = SQLAlchemyError()

    produto = Mock()
    produto.id = 1
    produto.estoque = 10 
    produto.preco = 150.00

    session.query.return_value.filter.return_value.first.side_effect = [produto, produto, produto, produto]

    pedido_schema = PedidoCreate(
        itens= [
            ItemPedidoCreate(
                id_produto=1,
                quantidade=1
            )
        ]
    )

    with pytest.raises(SQLAlchemyError):
        criar_pedido(pedido_schema, usuario_autenticado, session)

    session.rollback.assert_called_once()

@pytest.mark.parametrize("estoque, quantidade", [(10, 11), (5, 8), (20, 25), (3, 10)])
def test_estoque_insuficiente(usuario_teste, estoque, quantidade, session_teste):
    usuario = usuario_teste

    produto = Produto(
        nome="Teclado",
        preco=220.00,
        estoque=estoque
    )

    session_teste.add(produto)
    session_teste.commit()

    pedido_schema = PedidoCreate(
        itens = [
            ItemPedidoCreate(
                id_produto=produto.id,
                quantidade=quantidade
            )
        ]
    )

    pedido = criar_pedido(
        pedido_schema, 
        usuario,
        session_teste
    )

    assert pedido is False
    assert produto.estoque == estoque
    assert session_teste.query(Pedido).count() == 0


def test_produto_inexistente(usuario_teste, session_teste):
    usuario = usuario_teste

    pedido_schema = PedidoCreate(
            itens = [
                ItemPedidoCreate(
                    id_produto=99,
                    quantidade=1
                )
            ]
        )
    
    pedido = criar_pedido(
        pedido_schema,
        usuario,
        session_teste)

    assert pedido is None
    assert session_teste.query(Pedido).count() == 0


def test_pedido_com_varios_produtos(usuario_teste, session_teste):
    usuario = usuario_teste

    teclado = Produto(
        nome="Teclado",
        preco=220.00,
        estoque=10
    )

    mouse = Produto(
        nome="Mouse",
        preco=170.00,
        estoque=8
    )

    session_teste.add(teclado)
    session_teste.add(mouse)
    session_teste.commit()

    pedido_schema = PedidoCreate(
        itens = [
            ItemPedidoCreate(
                id_produto=teclado.id,
                quantidade=2
            ),
            ItemPedidoCreate(
                id_produto=mouse.id,
                quantidade=3
            )

        ]
    )

    pedido = criar_pedido(
        pedido_schema,
        usuario,
        session_teste)

    assert pedido is not None
    assert teclado.estoque == 8
    assert mouse.estoque == 5
    assert len(pedido.itens) == 2


def test_pedido_varios_produtos_estoque_insuficiente(usuario_teste, session_teste):
    usuario = usuario_teste

    teclado = Produto(
        nome="Teclado",
        preco=220.00,
        estoque=3
    )

    mouse = Produto(
        nome="Mouse",
        preco=170.00,
        estoque=5
    )

    session_teste.add(teclado)
    session_teste.add(mouse)
    session_teste.commit()

    pedido_schema = PedidoCreate(
        itens = [
            ItemPedidoCreate(
                id_produto=teclado.id,
                quantidade=2
            ),
            ItemPedidoCreate(
                id_produto=mouse.id,
                quantidade=7
            )
        ]
    )

    pedido = criar_pedido(
        pedido_schema,
        usuario,
        session_teste)

    assert pedido is False
    assert teclado.estoque == 3
    assert mouse.estoque == 5
    assert session_teste.query(Pedido).count() == 0


def test_pedido_mesmo_produto(usuario_teste, session_teste):
    usuario = usuario_teste

    produto = Produto(
        nome="Teclado",
        preco=220.00,
        estoque=10
    )

    session_teste.add(produto)
    session_teste.commit()

    pedido_schema = PedidoCreate(
        itens = [
            ItemPedidoCreate(
                id_produto=produto.id,
                quantidade=2
            ),
            ItemPedidoCreate(
                id_produto=produto.id,
                quantidade=3
            )
        ]
    )

    pedido = criar_pedido(pedido_schema, 
                          usuario,
                          session_teste)

    assert pedido is not None
    assert produto.estoque == 5
    assert len(pedido.itens) == 2
    assert pedido.itens[0].quantidade == 2
    assert pedido.itens[1].quantidade == 3


def test_pedido_mesmo_produto_estoque_insuficiente(usuario_teste, session_teste):
    usuario = usuario_teste

    produto = Produto(
        nome="Teclado",
        preco=220.00,
        estoque=10
    )

    session_teste.add(produto)
    session_teste.commit()

    pedido_schema = PedidoCreate(
        itens = [
            ItemPedidoCreate(
                id_produto=produto.id,
                quantidade=5
            ),
            ItemPedidoCreate(
                id_produto=produto.id,
                quantidade=6
            )
        ]
    )

    pedido = criar_pedido(pedido_schema,
                          usuario,
                          session_teste)

    assert pedido is False
    assert produto.estoque == 10
    assert session_teste.query(Pedido).count() == 0