from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class ProdutoCreate(BaseModel):
    nome: str  
    preco: float = Field(ge=0, description="O preço deve ser maior ou igual a zero.")
    estoque: int = Field(ge=0, description="O estoque deve ser maior ou igual a zero")


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    preco: float
    estoque: int

    class Config:
        from_attributes=True


class ProdutoUpdate(BaseModel):
    nome: str
    preco: float = Field(ge=0, description="O preço deve ser maior ou igual a zero.")
    estoque: int = Field(ge=0, description="O estoque deve ser maior ou igual a zero.")


class LoginSchema(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=8)


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=3)
    email: EmailStr 
    senha: str = Field(min_length=8)
    admin: bool

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool

    class Config:
        from_attributes=True

class UsuarioUpdate(BaseModel):
    nome: str = Field(min_length=3)
    email: EmailStr


class ItemPedidoCreate(BaseModel):
    id_produto: int
    quantidade: int = Field(ge=1, description="Mínimo de 1 item")

class PedidoCreate(BaseModel):
    itens: list[ItemPedidoCreate] = Field(min_length=1)

class ItemPedidoResponse(BaseModel):
    id: int
    id_pedido: int
    id_produto: int
    quantidade: int
    preco_unitario: float

    class Config:
        from_attributes=True

class PedidoResponse(BaseModel):
    id: int
    id_cliente:int
    data_pedido: datetime
    itens: list[ItemPedidoResponse]

    class Config:
        from_attributes=True
