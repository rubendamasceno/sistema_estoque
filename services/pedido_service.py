from models import Pedido, Produto, ItemPedido
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


def listar_pedidos(session):
    pedidos = session.query(Pedido).all()

    return pedidos


def criar_pedido(pedido_schema, usuario_autenticado, session: Session):
    try:
        quantidades = {}

        for item in pedido_schema.itens:
            produto = session.query(Produto).filter(Produto.id==item.id_produto).first()
        
            if not produto:
                return None
            
            if item.id_produto in quantidades:
                quantidades[item.id_produto] += item.quantidade

            else:
                quantidades[item.id_produto] = item.quantidade

        for id_produto, quantidade_total in quantidades.items():
            produto = session.query(Produto).filter(Produto.id==id_produto).first()

            if quantidade_total > produto.estoque:
                return False


        pedido = Pedido(usuario_autenticado.id)
        session.add(pedido)
        session.flush()

        for item in pedido_schema.itens:
            produto = session.query(Produto).filter(Produto.id==item.id_produto).first()
            item_pedido = ItemPedido(pedido.id, produto.id, item.quantidade, produto.preco)
            item_pedido.pedido = pedido
            session.add(item_pedido)

        for id_produto, quantidade_total in quantidades.items():
            produto = session.query(Produto).filter(Produto.id==id_produto).first()
            novo_estoque = produto.estoque - quantidade_total
            produto.estoque = novo_estoque

        session.commit()

    except SQLAlchemyError:
        session.rollback()
        raise
    return pedido


def ver_pedido(id:int, usuario_autenticado, session):
    pedido = session.query(Pedido).filter(Pedido.id==id, Pedido.id_cliente==usuario_autenticado.id).first()

    if not pedido:
        return None

    return pedido
