from http import HTTPStatus


def test_criar_usuario(cliente):
    resposta = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
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


def test_usuario_email_duplicado(cliente):
    usuario = cliente.post("/usuarios/", json={ 
    "nome": "teste",
    "email": "teste@gmail.com",
    "senha": "12345678",
    "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    usuario_duplicado = cliente.post("/usuarios/", json={
        "nome": "teste2",
        "email": "teste@gmail.com",
        "senha": "123456789",
        "admin": False
    })

    consulta = cliente.get(f"/usuarios/")
    dados = consulta.json()

    assert usuario_duplicado.status_code == HTTPStatus.CONFLICT
    assert len(dados) == 1
    assert dados[0]["id"] == id_usuario
    assert dados[0]["nome"] == "teste"
    assert dados[0]["email"] == "teste@gmail.com"


def test_usuario_email_invalido(cliente):
    resposta = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@example",
        "senha": "12345678",
        "admin": False
    })

    consulta = cliente.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert dados == []
    

def test_criar_usuario_senha_curta(cliente):
    resposta = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "123456",
        "admin": False
    })

    consulta = cliente.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert dados == []


def test_criar_usuario_nome_curto(cliente):
    resposta = cliente.post("/usuarios/", json={
        "nome": "te",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    consulta = cliente.get("usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert dados == []


def test_criar_usuario_sem_nome(cliente):
    resposta = cliente.post("/usuarios/", json={
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    consulta = cliente.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert dados ==[]


def test_criar_usuario_sem_email(cliente):
    resposta = cliente.post("/usuarios/", json={
        "nome": "teste",
        "senha": "12345678",
        "admin": False
    })

    consulta = cliente.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert dados == []


def test_criar_usuario_sem_senha(cliente):
    resposta = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "admin": False
    })

    consulta = cliente.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert dados == []




def test_listar_usuarios(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": True
    })

    assert usuario.status_code == HTTPStatus.OK
    
    consulta = cliente.get("/usuarios/")
    dados = consulta.json()

    assert usuario.status_code == HTTPStatus.OK
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1
    assert dados[0]["nome"] == "teste"
    assert dados[0]["email"] == "teste@gmail.com"
    assert dados[0]["admin"] is True


def test_buscar_ususario_por_id(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": True
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = cliente.get(f"/usuarios/{id_usuario}")
    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is True


def test_atualizar_usuario(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": True
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = cliente.put(f"/usuarios/{id_usuario}", json={
        "nome": "teste atualizado",
        "email": "teste.atualizado@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste atualizado"
    assert dados["email"] == "teste.atualizado@gmail.com"
    assert dados["admin"] is False


def test_excluir_usuario(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = cliente.delete(f"/usuarios/{id_usuario}")
    dados_resposta = resposta.json()

    consulta = cliente.get(f"/usuarios/{id_usuario}")

    assert resposta.status_code == HTTPStatus.OK
    assert consulta.status_code == HTTPStatus.NOT_FOUND
    assert dados_resposta["id"] == id_usuario

