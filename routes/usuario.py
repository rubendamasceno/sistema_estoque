from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, oauth2_schema, verificar_admin
from security import verificar_senha, criar_token, SECRET_KEY, ALGORITHM
from schemas import UsuarioCreate, UsuarioResponse, UsuarioUpdate, LoginSchema
from models import Usuario
from services.usuario_service import obter_usuario, autenticar_usuario, listar_usuarios, criar_usuario, excluir_usuario, atualizar_usuario
from datetime import timedelta

usuario_router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
    
@usuario_router.post("/login")
def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, session)
    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")
    
    senha_valida = verificar_senha(login_schema.senha, usuario)
    if not senha_valida:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7), tipo_token="refresh")
    access_token = criar_token(usuario.id)
    return {
        "refresh_token": refresh_token,
        "access_token": access_token,
        "token_type": "bearer"
    }


@usuario_router.post("/login-form")
def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, session)
    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

    senha_digitada = verificar_senha(dados_formulario.password, usuario)
    if not senha_digitada:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7), tipo_token="refresh")
    access_token = criar_token(usuario.id)
    return {
        "refresh_token":refresh_token,
        "access_token": access_token,
        "token_type": "bearer"
    }
    

@usuario_router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios_rota(session=Depends(pegar_sessao), admin=Depends(verificar_admin)):
    usuarios = listar_usuarios(session)
    
    return usuarios
    

@usuario_router.post("/", response_model=UsuarioResponse)
def criar_usuario_rota(usuario_schema:UsuarioCreate, session=Depends(pegar_sessao)):
    usuario = criar_usuario(usuario_schema, session)

    if usuario is False:
        raise HTTPException(status_code=409, detail="Já existe um usuário com este E-mail.")

    return usuario


@usuario_router.get("/{id}", response_model=UsuarioResponse)
def obter_usuario_rota(id:int, session=Depends(pegar_sessao), admin=Depends(verificar_admin)):
    usuario = obter_usuario(id, session)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    return usuario


@usuario_router.delete("/{id}", response_model=UsuarioResponse)
def excluir_usuario_rota(id:int, session=Depends(pegar_sessao), admin=Depends(verificar_admin)):
    usuario = excluir_usuario(id, session)

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    return usuario


@usuario_router.put("/{id}", response_model=UsuarioResponse)
def atualizar_usuario_rota(id:int, usuario_schema:UsuarioUpdate,  session=Depends(pegar_sessao), admin=Depends(verificar_admin)):
    usuario = atualizar_usuario(id, usuario_schema, session)

    if usuario is None: 
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    if usuario is False:
        raise HTTPException(status_code=409, detail="Já existe um usuário com este E-mail.")
    
    return usuario


@usuario_router.post("/refresh")
def use_refresh_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        tipo_token = dic_info.get("tipo")
        id_usuario = dic_info.get("sub")

        if tipo_token != "refresh":
            raise HTTPException(status_code=401, detail="É necessário um refresh token.")

        if not id_usuario:
            raise HTTPException(status_code=401, detail="Refresh token inválido: Usuário não identificado.")

        try:
            id_usuario = int(id_usuario)

        except (ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Refresh_token inválido: ID do usuário incorreto.")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token inválido ou expirado.")

    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")

    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


