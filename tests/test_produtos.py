from http import HTTPStatus

def test_criar_produto(cliente):
    resposta = cliente.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["nome"] == "Teclado"
    assert dados["preco"] == 150.00
    assert dados["estoque"] == 10
    assert "id" in dados 


def test_produto_preco_negativo(cliente):
    resposta = cliente.post("/produtos/", json={
        "nome": "Teclado",
        "preco": -150.00,
        "estoque": 10
    })

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY



def test_produto_estoque_negativo(cliente):
    resposta = cliente.post("/produtos/", json={
        "nome": "Mouse",
        "preco": 80.00,
        "estoque": -5
    })

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_listar_produtos(cliente):
    cliente.post("/produtos/", json={
            "nome": "Teclado",
            "preco": 150.00,
            "estoque": 10
        })

    resposta = cliente.get("/produtos/")
    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert len(dados) == 1
    assert dados[0]["nome"] == "Teclado"
    assert dados[0]["preco"] == 150.00
    assert dados[0]["estoque"] == 10


def test_buscar_produto_id(cliente):
    produto = cliente.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    id_produto = produto.json()["id"]

    resposta = cliente.get(f"/produtos/{id_produto}")
    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Teclado"
    assert dados["preco"] == 150.00
    assert dados["estoque"] == 10
    

def test_buscar_produto_inexistente(cliente):
    resposta = cliente.get("/produtos/999")

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_atualizar_produto(cliente):
    produto = cliente.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    id_produto = produto.json()["id"]

    resposta = cliente.put(f"/produtos/{id_produto}", json={
        "nome": "Teclado Mecânico",
        "preco": 200.00,
        "estoque": 5
    })

    resposta_get = cliente.get(f"/produtos/{id_produto}")
    dados = resposta_get.json()


    assert resposta_get.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Teclado Mecânico"
    assert dados["preco"] == 200.00
    assert dados["estoque"] == 5


def test_atualizar_produto_inexistente(cliente):
    resposta = cliente.put("/produtos/999", json={
        "nome": "Teclado Mecânico",
        "preco": 200.00,
        "estoque": 5

    })

    assert resposta.status_code == HTTPStatus.NOT_FOUND 


def test_atualizar_produto_preco_negativo(cliente):
    produto = cliente.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    id_produto = produto.json()["id"]

    resposta = cliente.put(f"/produtos/{id_produto}", json={
        "nome": "Teclado Mecânico",
        "preco": -200.00,
        "estoque": 5
    })

    resposta_get = cliente.get(f"/produtos/{id_produto}")
    dados = resposta_get.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert dados["id"] == id_produto
    assert dados["nome"] == "Teclado"
    assert dados["preco"] == 150
    assert dados["estoque"] == 10


def test_atualizar_produto_estoque_negativo(cliente):
    produto = cliente.post("/produtos/", json={
        "nome": "Mouse",
        "preco": 200.00,
        "estoque": 10
    })

    id_produto = produto.json()["id"]

    resposta = cliente.put(f"/produtos/{id_produto}", json={
        "nome": "Mouse Gamer",
        "preco": 150.00,
        "estoque": -5
    })

    resposta_get = cliente.get(f"/produtos/{id_produto}")
    dados = resposta_get.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert dados["id"] == id_produto
    assert dados["nome"] == "Mouse"
    assert dados["preco"] == 200.00
    assert dados["estoque"] == 10


def test_deletar_produto(cliente):
    produto = cliente.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 200.00,
        "estoque": 10
    })

    id_produto = produto.json()["id"]

    resposta = cliente.delete(f"/produtos/{id_produto}")
    dados_resposta = resposta.json()

    consulta = cliente.get("/produtos/")

    assert resposta.status_code == HTTPStatus.OK
    assert dados_resposta["id"] == id_produto
    assert len(consulta.json()) == 0


def test_deletar_produto_inexistente(cliente):
    resposta = cliente.delete("/produtos/999")

    assert resposta.status_code == HTTPStatus.NOT_FOUND














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