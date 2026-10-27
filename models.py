from db import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, CheckConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


class Produto(Base):
    __tablename__ = "produtos"

    __table_args__ = (
        CheckConstraint("preco >= 0"),
        CheckConstraint("estoque >= 0")
    )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(100), nullable=False)
    preco = Column("preco", Float, nullable=False)
    estoque = Column("estoque", Integer, default=0, nullable=False)

    def __init__(self, nome:str, preco:float, estoque: int = 0):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(50), nullable=False)
    email = Column("email", String(100), nullable=False, unique=True)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean, nullable=False, default=True)
    admin = Column("admin", Boolean, nullable=False, default=False)

    def __init__(self, nome:str, email:str, senha:str, admin:bool = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_cliente = Column("id_cliente", Integer, ForeignKey("usuarios.id"), nullable=False)
    data_pedido = Column("data_pedido", DateTime, default=datetime.now )
    itens = relationship(
        "ItemPedido",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )

    def __init__(self, id_cliente:int):
        self.id_cliente = id_cliente


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    __table_args__ = (
        CheckConstraint("quantidade >= 1"),
        CheckConstraint("preco_unitario >= 0")
    )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    id_pedido = Column("id_pedido", Integer, ForeignKey("pedidos.id"), nullable=False)
    id_produto = Column("id_produto", Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column("quantidade", Integer, nullable=False)
    preco_unitario = Column("preco_unitario", Float, nullable=False)
    pedido = relationship(
        "Pedido",
        back_populates="itens"
    )

    def __init__(self, id_pedido:int, id_produto:int, quantidade:int, preco_unitario:float):
        self.id_pedido = id_pedido
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario