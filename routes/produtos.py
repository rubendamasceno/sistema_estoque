from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.produto_service import obter_produto, listar_produtos, criar_produto, excluir_produto, atualizar_produto
from schemas import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from dependencies import pegar_sessao, verificar_admin


produtos_router = APIRouter(prefix="/produtos", tags=["Produtos"])


@produtos_router.get("/", response_model=list[ProdutoResponse])
def listar_produtos_rota(session: Session = Depends(pegar_sessao)):
    produtos = listar_produtos(session)

    return produtos


@produtos_router.post("/", response_model=ProdutoResponse)
def criar_produto_rota(produto_schema:ProdutoCreate, session: Session = Depends(pegar_sessao), admin=Depends(verificar_admin)): 
    produto = criar_produto(produto_schema, session)

    return produto


@produtos_router.get("/{id}", response_model=ProdutoResponse)
def buscar_produto(id: int, session: Session = Depends(pegar_sessao)):
    produto = obter_produto(id, session)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    return produto


@produtos_router.delete("/{id}", response_model=ProdutoResponse)
def excluir_produto_rota(id: int, session: Session = Depends(pegar_sessao), admin=Depends(verificar_admin)):
    produto = excluir_produto(id, session) 
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    return produto


@produtos_router.put("/{id}", response_model=ProdutoResponse)
def atualizar_produto_rota(id: int, produto_schema: ProdutoUpdate, session: Session = Depends(pegar_sessao), admin=Depends(verificar_admin)):
    produto = atualizar_produto(id, produto_schema, session)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    
    return produto
    