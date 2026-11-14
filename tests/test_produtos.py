from http import HTTPStatus

def test_criar_produto(usuario_admin):
    resposta = usuario_admin.post("/produtos/", json={
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


def test_produto_preco_negativo(usuario_admin):
    resposta = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": -150.00,
        "estoque": 10
    })

    consulta = usuario_admin.get("/produtos/")

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(consulta.json()) == 0



def test_produto_estoque_negativo(usuario_admin):
    resposta = usuario_admin.post("/produtos/", json={
        "nome": "Mouse",
        "preco": 80.00,
        "estoque": -5
    })

    consulta = usuario_admin.get("/produtos/")

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(consulta.json()) == 0


def test_listar_produtos(usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
            "nome": "Teclado",
            "preco": 150.00,
            "estoque": 10
        })

    resposta = usuario_admin.get("/produtos/")
    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert len(dados) == 1
    assert dados[0]["nome"] == "Teclado"
    assert dados[0]["preco"] == 150.00
    assert dados[0]["estoque"] == 10


def test_buscar_produto_por_id(usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    resposta = usuario_admin.get(f"/produtos/{id_produto}")
    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Teclado"
    assert dados["preco"] == 150.00
    assert dados["estoque"] == 10
    

def test_buscar_produto_inexistente(usuario_admin):
    resposta = usuario_admin.get("/produtos/999")

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_atualizar_produto(usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    resposta = usuario_admin.put(f"/produtos/{id_produto}", json={
        "nome": "Teclado Mecânico",
        "preco": 200.00,
        "estoque": 5
    })

    resposta_get = usuario_admin.get(f"/produtos/{id_produto}")
    dados = resposta_get.json()


    assert resposta.status_code == HTTPStatus.OK
    assert resposta_get.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Teclado Mecânico"
    assert dados["preco"] == 200.00
    assert dados["estoque"] == 5


def test_atualizar_produto_inexistente(usuario_admin):
    resposta = usuario_admin.put("/produtos/999", json={
        "nome": "Teclado Mecânico",
        "preco": 200.00,
        "estoque": 5

    })

    assert resposta.status_code == HTTPStatus.NOT_FOUND 


def test_atualizar_produto_preco_negativo(usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK
    
    id_produto = produto.json()["id"]

    resposta = usuario_admin.put(f"/produtos/{id_produto}", json={
        "nome": "Teclado Mecânico",
        "preco": -200.00,
        "estoque": 5
    })

    resposta_get = usuario_admin.get(f"/produtos/{id_produto}")
    dados = resposta_get.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert resposta_get.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Teclado"
    assert dados["preco"] == 150
    assert dados["estoque"] == 10


def test_atualizar_produto_estoque_negativo(usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Mouse",
        "preco": 200.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    resposta = usuario_admin.put(f"/produtos/{id_produto}", json={
        "nome": "Mouse Gamer",
        "preco": 150.00,
        "estoque": -5
    })

    resposta_get = usuario_admin.get(f"/produtos/{id_produto}")
    dados = resposta_get.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert resposta_get.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Mouse"
    assert dados["preco"] == 200.00
    assert dados["estoque"] == 10


def test_deletar_produto(usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 200.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    resposta = usuario_admin.delete(f"/produtos/{id_produto}")
    dados_resposta = resposta.json()

    consulta = usuario_admin.get(f"/produtos/{id_produto}")

    assert resposta.status_code == HTTPStatus.OK
    assert consulta.status_code == HTTPStatus.NOT_FOUND
    assert dados_resposta["id"] == id_produto


def test_deletar_produto_inexistente(usuario_admin):
    resposta = usuario_admin.delete("/produtos/999")

    assert resposta.status_code == HTTPStatus.NOT_FOUND