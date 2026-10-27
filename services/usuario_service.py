from sqlalchemy.exc import SQLAlchemyError
from models import Usuario
from schemas import UsuarioCreate
from security import gerar_hash


def obter_usuario(id:int, session):
    usuario = session.query(Usuario).filter(Usuario.id==id).first()

    return usuario


def autenticar_usuario(email, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()

    return usuario


def listar_usuarios(session):
    usuarios = session.query(Usuario).all()

    return usuarios

def criar_usuario(usuario_schema:UsuarioCreate, session):
    if autenticar_usuario(usuario_schema.email, session):
        return False
    
    senha_criptografada = gerar_hash(usuario_schema.senha)
    usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, admin=usuario_schema.admin)
    
    try:
        session.add(usuario)
        session.commit()

    except SQLAlchemyError:
        session.rollback()
        raise

    return usuario


def excluir_usuario(id:int, session):
    usuario = obter_usuario(id, session)

    if not usuario:
        return None

    try:
        session.delete(usuario)
        session.commit()

    except SQLAlchemyError:
        session.rollback()
        raise
        
    return usuario


def atualizar_usuario(id, usuario_schema, session):
    usuario = obter_usuario(id, session)

    if not usuario:
        return None

    if session.query(Usuario).filter(Usuario.email==usuario_schema.email, Usuario.id != id).first():
        return False
    
    try:
        usuario.nome = usuario_schema.nome
        usuario.email = usuario_schema.email
        session.commit()
        
    except SQLAlchemyError:
        session.rollback()
        raise

    return usuario
