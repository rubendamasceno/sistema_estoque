from fastapi import APIRouter, HTTPException, Depends
from dependencies import pegar_sessao, verificar_token, verificar_admin
from services.pedido_service import criar_pedido, listar_pedidos, ver_pedido
from schemas import PedidoCreate, PedidoResponse
from models import Usuario


pedido_router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@pedido_router.get("/", response_model=list[PedidoResponse])
def listar_pedidos_rota(session=Depends(pegar_sessao), admin=Depends(verificar_admin)):
    pedidos = listar_pedidos(session)

    return pedidos


@pedido_router.post("/", response_model=PedidoResponse)
def criar_pedido_rota(pedido_schema:PedidoCreate, session=Depends(pegar_sessao), usuario_autenticado: Usuario = Depends(verificar_token)):
    pedido = criar_pedido(pedido_schema, usuario_autenticado, session)

    if pedido is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    if pedido is False:
        raise HTTPException(status_code=409, detail="Estoque insuficiente.")

    return pedido 
    

@pedido_router.get("/{id}", response_model=PedidoResponse)
def ver_pedido_rota(id:int, session=Depends(pegar_sessao), usuario_autenticado: Usuario = Depends(verificar_token)):
    pedido = ver_pedido(id, usuario_autenticado, session)

    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")

    return pedido