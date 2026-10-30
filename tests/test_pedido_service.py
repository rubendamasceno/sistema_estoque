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