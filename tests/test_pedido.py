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


