from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# Cria o Banco de dados SQLite
db = create_engine("sqlite:///db.sqlite")

# Cria a Base de dados
Base = declarative_base()
