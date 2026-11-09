from http import HTTPStatus

def test_criar_usuario(cliente):
    resposta = cliente.post("/usuarios/", json={
        "nome": "ruben",
        "email": "ruben@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["nome"] == "ruben"
    assert dados["email"] == "ruben@gmail.com"
    assert "id" in dados


def test_criar_usuario_admin(cliente):
    resposta = cliente.post("/usuarios/", json={
        "nome": "adm",
        "email": "adm@gmail.com",
        "senha": "12345678",
        "admin": True
    })

    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["nome"] == "adm"
    assert dados["email"] == "adm@gmail.com"
    assert "id" in dados


def test_listar_usuarios(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "ruben",
        "email": "ruben@gmail.com",
        "senha": "12345678",
        "admin": True
    })
    
    consulta = cliente.get("/usuarios/")

    assert usuario.status_code == HTTPStatus.OK
    assert consulta.status_code == HTTPStatus.OK
    assert len(consulta.json()) == 1
    assert consulta.json()[0]["nome"] == "ruben"
    assert consulta.json()[0]["email"] == "ruben@gmail.com"
    assert consulta.json()[0]["admin"] is True