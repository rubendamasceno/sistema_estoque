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
    assert consulta.status_code == HTTPStatus.OK
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
    assert consulta.status_code == HTTPStatus.OK
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
    assert consulta.status_code == HTTPStatus.OK
    assert dados == []


def test_criar_usuario_nome_curto(cliente):
    resposta = cliente.post("/usuarios/", json={
        "nome": "te",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    consulta = cliente.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
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
    assert consulta.status_code == HTTPStatus.OK
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
    assert consulta.status_code == HTTPStatus.OK
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
    assert consulta.status_code == HTTPStatus.OK
    assert dados == []


def test_criar_usuario_sem_admin(cliente):
    resposta = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678"
    })

    consulta = cliente.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
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


def test_buscar_usuario_inexistente(cliente):
    resposta = cliente.get("/usuarios/999")

    assert resposta.status_code == HTTPStatus.NOT_FOUND


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
        "admin": False
    })

    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste atualizado"
    assert dados["email"] == "teste.atualizado@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_inexistente(cliente):
    resposta = cliente.put("/usuarios/999", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "admin": False
    })

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_atualizar_usuario_email_duplicado(cliente):
    usuario1 = cliente.post("/usuarios/", json={
        "nome": "teste1",
        "email": "teste1@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario1.status_code == HTTPStatus.OK

    id_usuario1 = usuario1.json()["id"]

    usuario2 = cliente.post("/usuarios/", json={
        "nome": "teste2",
        "email": "teste2@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario2.status_code == HTTPStatus.OK

    id_usuario2 = usuario2.json()["id"]

    resposta = cliente.put(f"/usuarios/{id_usuario1}", json={
        "nome": "teste123",
        "email": "teste2@gmail.com",
        "admin": True
    })

    consulta = cliente.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.CONFLICT
    assert consulta.status_code == HTTPStatus.OK
    assert dados[0]["id"] == id_usuario1
    assert dados[0]["nome"] == "teste1"
    assert dados[0]["email"] == "teste1@gmail.com"
    assert dados[0]["admin"] is  False
    assert dados[1]["id"] == id_usuario2
    assert dados[1]["email"] == "teste2@gmail.com"


def test_atualizar_usuario_email_invalido(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = cliente.put(f"/usuarios/{id_usuario}", json={
        "nome": "teste",
        "email": "teste@example",
        "admin": True
    })

    consulta = cliente.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_nome_curto(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = cliente.put(f"/usuarios/{id_usuario}", json={
        "nome": "te",
        "email": "teste@gmail.com",
        "admin": True
    })

    consulta = cliente.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_sem_nome(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = cliente.put(f"/usuarios/{id_usuario}", json={
        "email": "teste@gmail.com",
        "admin": True
    })

    consulta = cliente.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_sem_email(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = cliente.put(f"/usuarios/{id_usuario}", json={
        "nome": "teste",
        "admin": True
    })

    consulta = cliente.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
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


def test_excluir_usuario_inexistente(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = cliente.delete(f"/usuarios/999")

    consulta = cliente.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario



