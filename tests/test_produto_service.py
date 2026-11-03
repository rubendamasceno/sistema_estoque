from http import HTTPStatus
from select import select
from fastapi.testclient import TestClient
from main import app



# def test_():
#     cliente = TestClient(app) # Arrange
#     response = cliente.get("/") # act

#     assert response.status_code == HTTPStatus.OK # assert
#     assert response.json() == {"mensagem": "Olá Mundo!"}

#     with Session(engine) as session:
#         yield session

#     usuarios = session.scalars(select(usuario))
#         return {"usuario": usuarios}

# def test_usaurios(cliente, usuario):
#     from schemas import UsuarioCreate
#     usuario_schema = UsuarioPublic.model_validate(usuario).model.dump()
#     response = cliente.get("/usuarios")

#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {"usuario": [usuario_schema]}