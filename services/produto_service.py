from sqlalchemy.exc import SQLAlchemyError
from models import Produto


def listar_produtos(session):
    produtos = session.query(Produto).all()

    return produtos

def criar_produto(produto_schema, session):
    produto = Produto(nome=produto_schema.nome, preco=produto_schema.preco, estoque=produto_schema.estoque)
    
    try:
        session.add(produto)
        session.commit()

    except SQLAlchemyError:
        session.rollback()
        raise

    return produto


def obter_produto(id:int, session):
    produto = session.query(Produto).filter(Produto.id == id).first()
    return produto


def excluir_produto(id, session):
    produto = obter_produto(id, session)
    if not produto:
        return None

    try:
        session.delete(produto)
        session.commit()

    except SQLAlchemyError:
        session.rollback()
        raise

    return produto


def atualizar_produto(id:int, produto_schema, session):
    produto = obter_produto(id, session)
    if not produto:
        return None

    try:
        produto.nome = produto_schema.nome
        produto.preco = produto_schema.preco
        produto.estoque = produto_schema.estoque
        session.commit()

    except SQLAlchemyError:
        session.rollback()
        raise
    
    return produto