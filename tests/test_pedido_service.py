from sqlalchemy.orm import Session
from models import Usuario, Produto, Pedido
from schemas import PedidoCreate, ItemPedidoCreate
from services.pedido_service import criar_pedido

def test_criar_pedido(session_teste):
    usuario = Usuario(
        nome="teste",
        email="teste@gmail.com",
        senha="12345678"
    )

    produto = Produto(
        nome="Teclado",
        preco=320.00,
        estoque=10
    )

    session_teste.add(usuario)
    session_teste.add(produto)
    session_teste.commit()

    pedido_schema = PedidoCreate(
        itens = [
            ItemPedidoCreate(
                id_produto=produto.id,
                quantidade=2
            )
        ]
    )

    pedido = criar_pedido(
        pedido_schema,
        usuario,
        session_teste
    )

    assert pedido is not None
    assert produto.estoque == 8

    id_pedido = pedido.id

    with Session(bind=session_teste.get_bind()) as session_verificacao:
        pedido_salvo = session_verificacao.query(Pedido).filter(Pedido.id==id_pedido).first()

        assert pedido_salvo is not None


def test_estoque_insuficiente(session_teste):
    usuario = Usuario(
        nome="teste",
        email="teste@gmail.com",
        senha="12345678"
    )

    produto = Produto(
        nome="Teclado",
        preco=220.00,
        estoque=5
    )

    session_teste.add(usuario)
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

    assert pedido is False
    assert produto.estoque == 5


def test_produto_inexistente(session_teste):
    usuario = Usuario(
        nome="teste",
        email="teste@gmail.com",
        senha="teste12345678"
    )

    session_teste.add(usuario)
    session_teste.commit()

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


def test_pedido_varios_produtos(session_teste):
    usuario = Usuario(
        nome="teste",
        email="teste@gmail.com",
        senha="teste12345678"
    )

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

    session_teste.add_all([usuario, teclado, mouse])
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



    