from http import HTTPStatus


def test_login(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    login = cliente.post("/usuarios/login", json={
        "email": "teste@gmail.com",
        "senha": "12345678"
    })

    assert login.status_code == HTTPStatus.OK

    dados_login = login.json()

    assert dados_login["token_type"] == "bearer"
    assert "access_token" in dados_login
    assert "refresh_token" in dados_login


def test_login_com_senha_incorreta(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    login = cliente.post("/usuarios/login", json={
        "email": "teste@gmail.com",
        "senha": "senhaerrada123"
    })

    assert login.status_code == HTTPStatus.UNAUTHORIZED
    assert login.json()["detail"] == "E-mail ou senha incorretos."


def test_login_com_email_inexistente(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    login = cliente.post("/usuarios/login", json={
        "email": "emailerrado@gmail.com",
        "senha": "12345678"
    })

    assert login.status_code == HTTPStatus.UNAUTHORIZED
    assert login.json()["detail"] == "E-mail ou senha incorretos." 


def test_login_form(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    login = cliente.post("/usuarios/login-form", data={
        "username": "teste@gmail.com",
        "password": "12345678"
    })

    assert login.status_code == HTTPStatus.OK

    dados_login = login.json()

    assert dados_login["token_type"] == "bearer"
    assert "access_token" in dados_login
    assert "refresh_token" in dados_login


def test_login_form_com_senha_incorreta(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    login = cliente.post("/usuarios/login-form", data={
        "username": "teste@gmail.com",
        "password": "senhaerrada123"
    })

    assert login.status_code == HTTPStatus.UNAUTHORIZED
    assert login.json()["detail"] == "E-mail ou senha incorretos."

def test_login_form_com_email_inexistente(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    login = cliente.post("/usuarios/login-form", data={
        "username": "emailerrado@gmail.com",
        "password": "12345678"
    })

    assert login.status_code == HTTPStatus.UNAUTHORIZED
    assert login.json()["detail"] == "E-mail ou senha incorretos."


def test_criar_usuario(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste", 
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    dados = usuario.json()

    assert usuario.status_code == HTTPStatus.OK
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert "id" in dados


def test_criar_usuario_admin(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "adm",
        "email": "adm@gmail.com",
        "senha": "12345678",
        "admin": True
    })

    dados = usuario.json()

    assert usuario.status_code == HTTPStatus.OK
    assert dados["admin"] is False 

def test_criar_usuario_email_duplicado(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={ 
    "nome": "teste",
    "email": "teste@gmail.com",
    "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    usuario_duplicado = cliente.post("/usuarios/", json={
        "nome": "teste2",
        "email": "teste@gmail.com",
        "senha": "123456789",
    })

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert usuario_duplicado.status_code == HTTPStatus.CONFLICT
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert usuario_duplicado.json()["detail"] == "Já existe um usuário com este E-mail."


def test_criar_usuario_email_invalido(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@example",
        "senha": "12345678",
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert usuario.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1
    

def test_criar_usuario_senha_curta(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "123456",
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert usuario.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1


def test_criar_usuario_nome_curto(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "te",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert usuario.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1


def test_criar_usuario_sem_nome(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert usuario.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1


def test_criar_usuario_sem_email(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "senha": "12345678",
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert usuario.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1


def test_criar_usuario_sem_senha(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
    })

    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert usuario.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 1


def test_listar_usuarios(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK
    
    consulta = usuario_admin.get("/usuarios/")
    dados = consulta.json()

    assert consulta.status_code == HTTPStatus.OK
    assert len(dados) == 2


def test_listar_usuarios_com_usuario_comum(usuario_autenticado, cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    consulta = usuario_autenticado.get("/usuarios/")

    assert consulta.status_code == HTTPStatus.FORBIDDEN


def test_listar_usuarios_sem_token(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    consulta = cliente.get("/usuarios/")

    assert consulta.status_code == HTTPStatus.UNAUTHORIZED


def test_listar_usuarios_com_token_invalido(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    consulta = cliente.get("/usuarios/", headers={"Authorization": "Bearer token_invalido"})

    assert consulta.status_code == HTTPStatus.UNAUTHORIZED


def test_buscar_usuario_pelo_id(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK
    id_usuario = usuario.json()["id"]

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_buscar_usuario_inexistente(usuario_admin):
    consulta = usuario_admin.get("/usuarios/999")

    assert consulta.status_code == HTTPStatus.NOT_FOUND
    assert consulta.json()["detail"] == "Usuário não encontrado."


def test_buscar_usuario_por_id_com_usuario_comum(usuario_autenticado, cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK
    id_usuario = usuario.json()["id"]

    consulta = usuario_autenticado.get(f"/usuarios/{id_usuario}")

    assert consulta.status_code == HTTPStatus.FORBIDDEN


def test_buscar_usaurio_por_id_sem_token(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })
    
    assert usuario.status_code == HTTPStatus.OK
    id_usuario = usuario.json()["id"]

    consulta = cliente.get(f"/usuarios/{id_usuario}")

    assert consulta.status_code == HTTPStatus.UNAUTHORIZED
    

def test_buscar_usuario_com_token_invalido(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })
        
    assert usuario.status_code == HTTPStatus.OK
    id_usuario = usuario.json()["id"]

    consulta = cliente.get(f"/usuarios/{id_usuario}", headers={"Authorization": "Bearer token_invalido"})

    assert consulta.status_code == HTTPStatus.UNAUTHORIZED


def test_atualizar_usuario(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario}", json={
        "nome": "teste atualizado",
        "email": "teste.atualizado@gmail.com",
    })

    dados = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste atualizado"
    assert dados["email"] == "teste.atualizado@gmail.com"


def test_atualizar_usuario_inexistente(usuario_admin):
    resposta = usuario_admin.put("/usuarios/999", json={
        "nome": "teste",
        "email": "teste@gmail.com",
    })

    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json()["detail"] == "Usuário não encontrado."


def test_atualizar_usuario_email_duplicado(cliente, usuario_admin):
    usuario1 = cliente.post("/usuarios/", json={
        "nome": "teste1",
        "email": "teste1@gmail.com",
        "senha": "12345678",
    })

    assert usuario1.status_code == HTTPStatus.OK

    id_usuario1 = usuario1.json()["id"]

    usuario2 = cliente.post("/usuarios/", json={
        "nome": "teste2",
        "email": "teste2@gmail.com",
        "senha": "12345678",
    })

    assert usuario2.status_code == HTTPStatus.OK

    id_usuario2 = usuario2.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario1}", json={
        "nome": "teste123",
        "email": "teste2@gmail.com",
    })

    consulta1 = usuario_admin.get(f"/usuarios/{id_usuario1}")
    dados1 = consulta1.json()

    consulta2 = usuario_admin.get(f"/usuarios/{id_usuario2}")
    dados2 = consulta2.json()

    assert resposta.status_code == HTTPStatus.CONFLICT
    assert resposta.json()["detail"] == "Já existe um usuário com este E-mail."
    assert consulta1.status_code == HTTPStatus.OK
    assert dados1["id"] == id_usuario1
    assert dados1["nome"] == "teste1"
    assert dados1["email"] == "teste1@gmail.com"
    assert dados1["admin"] is False

    assert dados2["id"] == id_usuario2
    assert dados2["email"] == "teste2@gmail.com"


def test_atualizar_usuario_email_invalido(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario}", json={
        "nome": "teste",
        "email": "teste@example",
    })

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_nome_curto(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario}", json={
        "nome": "te",
        "email": "teste@gmail.com",
    })

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_sem_nome(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario}", json={
        "email": "teste@gmail.com",
    })

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_sem_email(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.put(f"/usuarios/{id_usuario}", json={
        "nome": "teste",
    })

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_com_usuario_comum(usuario_autenticado, cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
            "nome": "teste",
            "email": "teste@gmail.com",
            "senha": "12345678",
            "admin": False
        })
    
    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_autenticado.put(f"/usuarios/{id_usuario}", json={
        "nome": "teste",
    })

    assert resposta.status_code == HTTPStatus.FORBIDDEN

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    
    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_atualizar_usuario_sem_token(cliente):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })
        
    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    consulta = cliente.put(f"/usuarios/{id_usuario}", json={
        "nome": "teste123",
        "email": "email123@gmail.com",
    })

    assert consulta.status_code == HTTPStatus.UNAUTHORIZED


def test_atualizar_usuario_com_token_invalido(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })
    
    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = cliente.put(f"/usuarios/{id_usuario}", json={
        "nome": "teste",
    }, headers={"Authorization": "Bearer token_invalido"})

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_excluir_usuario(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_admin.delete(f"/usuarios/{id_usuario}")
    dados_resposta = resposta.json()

    assert resposta.status_code == HTTPStatus.OK
    assert dados_resposta["id"] == id_usuario

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
   
    assert consulta.status_code == HTTPStatus.NOT_FOUND
   


def test_excluir_usuario_inexistente(usuario_admin):
    resposta = usuario_admin.delete(f"/usuarios/999")

    assert resposta.status_code == HTTPStatus.NOT_FOUND
    assert resposta.json()["detail"] == "Usuário não encontrado."


def test_excluir_usuario_com_usuario_comum(usuario_autenticado, cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = usuario_autenticado.delete(f"/usuarios/{id_usuario}")

    assert resposta.status_code == HTTPStatus.FORBIDDEN

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_excluir_usuario_sem_token(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = cliente.delete(f"/usuarios/{id_usuario}")

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False


def test_excluir_usuario_invalido(cliente, usuario_admin):
    usuario = cliente.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    resposta = cliente.delete(f"/usuarios/{id_usuario}", headers={"Authorization": "Bearer token_invalido"})

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED

    consulta = usuario_admin.get(f"/usuarios/{id_usuario}")
    dados = consulta.json()

    assert consulta.status_code == HTTPStatus.OK
    assert dados["id"] == id_usuario
    assert dados["nome"] == "teste"
    assert dados["email"] == "teste@gmail.com"
    assert dados["admin"] is False