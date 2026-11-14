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


def test_usuario_email_duplicado(usuario_admin):
    usuario = usuario_admin.post("/usuarios/", json={ 
    "nome": "teste",
    "email": "teste@gmail.com",
    "senha": "12345678",
    "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    usuario_duplicado = usuario_admin.post("/usuarios/", json={
        "nome": "teste2",
        "email": "teste@gmail.com",
        "senha": "123456789",
        "admin": False
    })

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert usuario_duplicado.status_code == HTTPStatus.CONFLICT
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"


def test_usuario_email_invalido(usuario_admin):
    resposta = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@example",
        "senha": "12345678",
        "admin": False
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1
    

def test_criar_usuario_senha_curta(usuario_admin):
    resposta = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "123456",
        "admin": False
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1


def test_criar_usuario_nome_curto(usuario_admin):
    resposta = usuario_admin.post("/usuarios/", json={
        "nome": "te",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1


def test_criar_usuario_sem_nome(usuario_admin):
    resposta = usuario_admin.post("/usuarios/", json={
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1


def test_criar_usuario_sem_email(usuario_admin):
    resposta = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "senha": "12345678",
        "admin": False
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1


def test_criar_usuario_sem_senha(usuario_admin):
    resposta = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "admin": False
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1


def test_criar_usuario_sem_admin(usuario_admin):
    resposta = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678"
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1


def test_listar_usuarios(usuario_admin):
    usuario = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK
    
    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 2


def test_buscar_ususario_pelo_id(usuario_admin):
    usuario = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK
    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_buscar_usuario_inexistente(usuario_admin):
    resposta = usuario_admin.get("/usuarios/999")

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_atualizar_usuario(usuario_admin):
    usuario = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": True
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario}", json={
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


def test_atualizar_usuario_inexistente(usuario_admin):
    resposta = usuario_admin.put("/usuarios/999", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "admin": False
    })

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_atualizar_usuario_email_duplicado(usuario_admin):
    usuario1 = usuario_admin.post("/usuarios/", json={
        "nome": "teste1",
        "email": "teste1@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario1.status_code == HTTPStatus.OK

    id_usuario1 = usuario1.json()["id"]

    usuario2 = usuario_admin.post("/usuarios/", json={
        "nome": "teste2",
        "email": "teste2@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario2.status_code == HTTPStatus.OK

    id_usuario2 = usuario2.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario1}", json={
        "nome": "teste123",
        "email": "teste2@gmail.com",
        "admin": True
    })

    consulta1 = usuario_admin.get(f"/usuarios/{id_usuario1}")
    dados1 = consulta1.json()

    consulta2 = usuario_admin.get(f"/usuarios/{id_usuario2}")
    dados2 = consulta2.json()

    assert resposta.status_code == HTTPStatus.CONFLICT
    assert consulta1.status_code == HTTPStatus.OK
    assert dados1["id"] == id_usuario1
    assert dados1["nome"] == "teste1"
    assert dados1["email"] == "teste1@gmail.com"
    assert dados1["admin"] is False

    assert dados2["id"] == id_usuario2
    assert dados2["email"] == "teste2@gmail.com"


def test_atualizar_usuario_email_invalido(usuario_admin):
    usuario = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario}", json={
        "nome": "teste",
        "email": "teste@example",
        "admin": True
    })

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_nome_curto(usuario_admin):
    usuario = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario}", json={
        "nome": "te",
        "email": "teste@gmail.com",
        "admin": True
    })

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_sem_nome(usuario_admin):
    usuario = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario}", json={
        "email": "teste@gmail.com",
        "admin": True
    })

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_sem_email(usuario_admin):
    usuario = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario}", json={
        "nome": "teste",
        "admin": True
    })

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_excluir_usuario(usuario_admin):
    usuario = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.delete(f"/usuarios/{id_usuario}")
    dados_resposta = resposta.json()

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")

    assert resposta.status_code == HTTPStatus.OK
    assert consulta.status_code == HTTPStatus.NOT_FOUND
    assert dados_resposta["id"] == id_usuario


def test_excluir_usuario_inexistente(usuario_admin):
    usuario = usuario_admin.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
        "admin": False
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.delete(f"/usuarios/999")

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario



