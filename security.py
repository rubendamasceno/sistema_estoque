from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone


load_dotenv()
# Carrega as variáveis de ambiente do seu codigo

SECRET_KEY= os.getenv("SECRET_KEY")
# Combinado com a senha do usuario cria uma terceira chave, que seria a hash daquele usuario

ALGORITHM = os.getenv("ALGORITHM")
# Algorítmo usado para assinar o JWT

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
# Tempo de duração do access token


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Quem vai fazer a criptografia

def gerar_hash(senha:str):
    senha_criptografada = bcrypt_context.hash(senha)
    return senha_criptografada


def verificar_senha(senha:str, usuario):
    senha_valida = bcrypt_context.verify(senha, usuario.senha)
    if not senha_valida:
        return False
    return senha_valida

def criar_token(id_usuario, duracao_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), tipo_token="access"):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {
        "sub": str(id_usuario),
        "exp": data_expiracao,
        "tipo": tipo_token 
    }     
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)   
    return jwt_codificado