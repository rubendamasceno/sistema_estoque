from http import HTTPStatus


def test_criar_produto(usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    dados = produto.json()

    assert produto.status_code == HTTPStatus.OK
    assert dados["nome"] == "Teclado"
    assert dados["preco"] == 150.00
    assert dados["estoque"] == 10
    assert "id" in dados 


def test_criar_produto_com_preco_negativo(usuario_admin, cliente):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": -150.00,
        "estoque": 10
    })

    consulta = cliente.get("/produtos/")

    assert produto.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert consulta.json() == []


def test_criar_produto_com_estoque_negativo(usuario_admin, cliente):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Mouse",
        "preco": 80.00,
        "estoque": -5
    })

    consulta = cliente.get("/produtos/")

    assert produto.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert consulta.json() == []


def test_criar_produto_com_usuario_comum(usuario_autenticado, cliente):
    produto = usuario_autenticado.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 220.00,
        "estoque": 5
    })

    assert produto.status_code == HTTPStatus.FORBIDDEN

    consulta = cliente.get("/produtos/")

    assert consulta.status_code == HTTPStatus.OK
    assert consulta.json() == []


def test_criar_produto_sem_token(cliente):
    produto = cliente.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 220.00,
        "estoque": 5
    })

    assert produto.status_code == HTTPStatus.UNAUTHORIZED

    consulta = cliente.get("/produtos/")

    assert consulta.status_code == HTTPStatus.OK
    assert consulta.json() == []


def test_criar_produto_com_token_invalido(cliente):
    produto = cliente.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 220.00,
        "estoque": 5
    }, headers={"Authorization": "Bearer token_invalido"})

    assert produto.status_code == HTTPStatus.UNAUTHORIZED

    consulta = cliente.get("/produtos/")

    assert consulta.status_code == HTTPStatus.OK
    assert consulta.json() == []


def test_listar_produtos(cliente, usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
            "nome": "Teclado",
            "preco": 150.00,
            "estoque": 10
        })

    assert produto.status_code == HTTPStatus.OK

    resposta = cliente.get("/produtos/")
    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert len(dados) == 1
    assert dados[0]["nome"] == "Teclado"
    assert dados[0]["preco"] == 150.00
    assert dados[0]["estoque"] == 10


def test_buscar_produto_por_id(cliente, usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    resposta = cliente.get(f"/produtos/{id_produto}")
    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Teclado"
    assert dados["preco"] == 150.00
    assert dados["estoque"] == 10
    

def test_buscar_produto_inexistente(cliente):
    consulta = cliente.get("/produtos/999")

    assert consulta.status_code == HTTPStatus.NOT_FOUND


def test_buscar_produto_por_id_sem_token(cliente, usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    consulta = cliente.get(f"/produtos/{id_produto}")
    dados = consulta.json()

    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto 



def test_atualizar_produto(usuario_admin, cliente):
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

    consulta = cliente.get(f"/produtos/{id_produto}")
    dados = consulta.json()


    assert resposta.status_code == HTTPStatus.OK
    assert consulta.status_code == HTTPStatus.OK
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


def test_atualizar_produto_preco_negativo(usuario_admin, cliente):
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

    consulta = cliente.get(f"/produtos/{id_produto}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Teclado"
    assert dados["preco"] == 150
    assert dados["estoque"] == 10


def test_atualizar_produto_estoque_negativo(usuario_admin, cliente):
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

    consulta = cliente.get(f"/produtos/{id_produto}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Mouse"
    assert dados["preco"] == 200.00
    assert dados["estoque"] == 10


def test_atualizar_produto_com_usuario_comum(usuario_autenticado, usuario_admin, cliente):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK
    
    id_produto = produto.json()["id"]

    resposta = usuario_autenticado.put(f"/produtos/{id_produto}", json={
        "nome": "Teclado Mecânico",
        "preco": 200.00,
        "estoque": 5
    })

    assert resposta.status_code == HTTPStatus.FORBIDDEN

    consulta = cliente.get(f"/produtos/{id_produto}")
    dados = consulta.json()


    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Teclado"
    assert dados["preco"] == 150
    assert dados["estoque"] == 10


def test_atualizar_produto_sem_token(cliente, usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 150.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    resposta = cliente.put(f"/produtos/{id_produto}", json={
        "nome": "Teclado Mecânico",
        "preco": 200.00,
        "estoque": 5
    })

    consulta = cliente.get(f"/produtos/{id_produto}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Teclado"
    assert dados["preco"] == 150
    assert dados["estoque"] == 10


def test_atualizar_produto_com_token_invalido(usuario_admin, cliente):
    produto = usuario_admin.post("/produtos/", json={
            "nome": "Teclado",
            "preco": 150.00,
            "estoque": 10
        })
    
    assert produto.status_code == HTTPStatus.OK
    
    id_produto = produto.json()["id"]
    
    resposta = cliente.put(f"/produtos/{id_produto}", json={
        "nome": "Teclado Mecânico",
        "preco": 200.00,
        "estoque": 5
        }, headers={"Authorization": "Bearer token_invalido"})
    
    consulta = cliente.get(f"/produtos/{id_produto}")
    dados = consulta.json()
    
    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_produto
    assert dados["nome"] == "Teclado"
    assert dados["preco"] == 150
    assert dados["estoque"] == 10


def test_deletar_produto(usuario_admin, cliente):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 200.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    resposta = usuario_admin.delete(f"/produtos/{id_produto}")
    dados_resposta = resposta.json()

    consulta = cliente.get(f"/produtos/{id_produto}")

    assert resposta.status_code == HTTPStatus.OK
    assert consulta.status_code == HTTPStatus.NOT_FOUND
    assert dados_resposta["id"] == id_produto


def test_deletar_produto_inexistente(usuario_admin):
    resposta = usuario_admin.delete("/produtos/999")

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_excluir_produto_com_usuario_comum(usuario_autenticado, usuario_admin, cliente):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 200.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    resposta = usuario_autenticado.delete(f"/produtos/{id_produto}")

    assert resposta.status_code == HTTPStatus.FORBIDDEN

    consulta = cliente.get(f"/produtos/{id_produto}")
    dados_get = consulta.json()
    
    assert consulta.status_code == HTTPStatus.OK
    assert dados_get["id"] == id_produto


def test_excluir_produto_com_usuario_sem_token(cliente, usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 200.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    resposta = cliente.delete(f"/produtos/{id_produto}")

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED

    consulta = cliente.get(f"/produtos/{id_produto}")
    dados_get = consulta.json()
    
    assert consulta.status_code == HTTPStatus.OK
    assert dados_get["id"] == id_produto


def test_excluir_produto_com_usuario_com_token_invalido(cliente, usuario_admin):
    produto = usuario_admin.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 200.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    resposta = cliente.delete(f"/produtos/{id_produto}", headers={"Authorization": "Bearer token_invalido"})

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED

    consulta = cliente.get(f"/produtos/{id_produto}")
    dados_get = consulta.json()
    
    assert consulta.status_code == HTTPStatus.OK
    assert dados_get["id"] == id_produto