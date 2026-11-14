from http import HTTPStatus


def test_criar_pedido(usuario_autenticado):
    produto = usuario_autenticado.post("/produtos/",json={
        "nome": "Teclado",
        "preco": 200.00,
        "estoque": 10
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    pedido = usuario_autenticado.post("/pedidos/", json={
        "itens": [
            {
                "id_produto": id_produto,
                "quantidade": 5
            }
        ]
    })

    get_pedidos = usuario_autenticado.get("/pedidos/")
    dados_pedidos = get_pedidos.json()

    get_produto = usuario_autenticado.get(f"/produtos/{id_produto}")
    dados_produto = get_produto.json()

    assert pedido.status_code == HTTPStatus.OK
    assert get_pedidos.status_code == HTTPStatus.OK
    assert get_produto.status_code == HTTPStatus.OK
    assert dados_pedidos[0]["itens"][0]["id_produto"] == id_produto
    assert dados_pedidos[0]["itens"][0]["quantidade"] == 5
    assert dados_produto["estoque"] == 5


def test_criar_pedido_produto_inexistente(usuario_autenticado):
    pedido = usuario_autenticado.post("/pedidos/", json={
        "itens": [
            {
                "id_produto": 999,
                "quantidade": 5
            }
        ]
    })

    assert pedido.status_code == HTTPStatus.NOT_FOUND
    assert pedido.json()["detail"] == "Produto não encontrado."


def test_criar_pedido_produto_estoque_insuficiente(usuario_autenticado):
    produto = usuario_autenticado.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 200.00,
        "estoque": 5
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    pedido = usuario_autenticado.post("/pedidos/", json={
        "itens": [
            {
                "id_produto": id_produto,
                "quantidade": 7
            }
        ]
    })

    get_pedidos = usuario_autenticado.get("/pedidos/")
    dados_pedidos = get_pedidos.json()

    get_produto = usuario_autenticado.get(f"/produtos/{id_produto}")
    dados_produto = get_produto.json()

    assert pedido.status_code == HTTPStatus.CONFLICT
    assert get_pedidos.status_code == HTTPStatus.OK
    assert dados_pedidos == []
    assert get_produto.status_code == HTTPStatus.OK
    assert dados_produto["estoque"] == 5


def test_buscar_pedido_pelo_id(usuario_autenticado):
    produto = usuario_autenticado.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 200.00,
        "estoque": 5
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    pedido = usuario_autenticado.post("/pedidos/", json={
        "itens": [
            {
                "id_produto": id_produto,
                "quantidade": 3
            }
        ]
    })

    id_pedido = pedido.json()["id"]

    get_pedidos = usuario_autenticado.get(f"/pedidos/{id_pedido}")
    dados_pedido = get_pedidos.json()

    get_produto = usuario_autenticado.get(f"/produtos/{id_produto}")
    dados_produto = get_produto.json()

    assert pedido.status_code == HTTPStatus.OK
    assert get_pedidos.status_code == HTTPStatus.OK
    assert get_produto.status_code == HTTPStatus.OK
    assert dados_pedido["id"] == id_pedido
    assert dados_pedido["itens"][0]["id_produto"] == id_produto
    assert dados_pedido["itens"][0]["quantidade"] == 3
    assert dados_produto["estoque"] == 2


def test_buscar_pedido_inexistente(usuario_autenticado):
    consulta = usuario_autenticado.get("/pedidos/99")

    assert consulta.status_code == HTTPStatus.NOT_FOUND
    assert consulta.json()["detail"] == "Pedido não encontrado."


def test_buscar_pedido_de_outro_usuario(usuario_autenticado):
    produto = usuario_autenticado.post("/produtos/", json={
        "nome": "Teclado",
        "preco": 200.00,
        "estoque": 5
    })

    assert produto.status_code == HTTPStatus.OK

    id_produto = produto.json()["id"]

    pedido = usuario_autenticado.post("/pedidos/", json={
        "itens": [
            {
                "id_produto": id_produto,
                "quantidade": 3
            }
        ]
    })

    id_pedido = pedido.json()["id"]

    usuario2 = usuario_autenticado.post("/usuarios/", json={
        "nome": "teste2", 
        "email": "teste2@gmail.com",
        "senha": "123456789",
        "admin": False 
    })

    assert usuario2.status_code == HTTPStatus.OK

    login = usuario_autenticado.post("/usuarios/login", json={
        "email": "teste2@gmail.com",
        "senha": "123456789"
    })

    assert login.status_code == HTTPStatus.OK

    access_token = login.json()["access_token"]

    usuario_autenticado.headers.update({
        "authorization": f"Bearer {access_token}"
    })

    consulta = usuario_autenticado.get(f"/pedidos/{id_pedido}")

    assert consulta.status_code == HTTPStatus.NOT_FOUND
    assert consulta.json()["detail"] == "Pedido não encontrado."


def test_listar_pedido_sem_token(cliente):
    resposta = cliente.get("/pedidos/1")

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED


def test_pedido_token_invalido(cliente):
    resposta = cliente.get("/pedidos/1", headers={"Authorization": "Bearer token_invalido"})

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED