from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import sessionmaker, Session
from db import db
from security import SECRET_KEY, ALGORITHM
from models import Usuario

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/usuarios/login-form")

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
        tipo_token = dic_info.get("tipo")

        if tipo_token != "access":
            raise HTTPException(status_code=401, detail="Token inválido.")

    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")
    return usuario 


def verificar_admin(usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Acesso permitido para administradores.")
    
    return usuario