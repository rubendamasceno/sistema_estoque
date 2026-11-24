from http import HTTPStatus
from security import criar_token, timedelta, SECRET_KEY, ALGORITHM
from jose import jwt


def test_verificar_access_token_valido(usuario_autenticado):
    pedido = usuario_autenticado.get("/pedidos/999")

    assert pedido.status_code == HTTPStatus.NOT_FOUND


def test_verificar_access_token_invalido(cliente):
    pedido = cliente.get("/pedidos/999", headers={"Authorization": "Bearer access_token_invalido"})

    assert pedido.status_code == HTTPStatus.UNAUTHORIZED


def test_verificar_token_expirado(usuario_autenticado):
    usuario = usuario_autenticado.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })

    assert usuario.status_code == HTTPStatus.OK
    id_usuario = usuario.json()["id"]
    
    token_expirado = criar_token(
        id_usuario,
        duracao_token=timedelta(minutes=-1)
    )

    pedido = usuario_autenticado.get("/pedidos/999", headers={"Authorization": f"Bearer {token_expirado}"})

    assert pedido.status_code == HTTPStatus.UNAUTHORIZED


def test_verificar_access_token_sem_sub(usuario_autenticado):
    dic_info = {
        "tipo": "access"
    }

    token_sem_sub = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    pedido = usuario_autenticado.get("/pedidos/999", headers={"Authorization": f"Bearer {token_sem_sub}"})

    assert pedido.status_code == HTTPStatus.UNAUTHORIZED


def test_verificar_access_token_com_sub_invalido(usuario_autenticado):
    dic_info = {
        "sub": "abc",
        "tipo": "access"
    }

    token_sub_invalido = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    pedido = usuario_autenticado.get("/pedidos/999", headers={"Authorization": f"Bearer {token_sub_invalido}"})

    assert pedido.status_code == HTTPStatus.UNAUTHORIZED


def test_verificar_access_token_usuario_inexistente(usuario_autenticado):
    dic_info = {
        "sub": str(999),
        "tipo": "access"
    }

    token_usuario_inexistente = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    pedido = usuario_autenticado.get("/pedidos/999", headers={"Authorization": f"Bearer {token_usuario_inexistente}"})

    assert pedido.status_code == HTTPStatus.UNAUTHORIZED


def test_verificar_refresh_token_como_access_token(usuario_autenticado):
    usuario = usuario_autenticado.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })
    assert usuario.status_code == HTTPStatus.OK
    id_usuario = usuario.json()["id"]

    refresh_token = criar_token(
        id_usuario,
        duracao_token=timedelta(days=7),
        tipo_token="refresh"
    )

    pedido = usuario_autenticado.get("/pedidos/999", headers={"Authorization": f"Bearer {refresh_token}"})

    assert pedido.status_code == HTTPStatus.UNAUTHORIZED


def test_refresh_token_valido(usuario_autenticado):
    usuario = usuario_autenticado.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",
    })
    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    refresh_token = criar_token(
        id_usuario,
        duracao_token=timedelta(days=7),
        tipo_token="refresh"
    )

    rota_refresh = usuario_autenticado.post("/usuarios/refresh", headers={"Authorization": f"Bearer {refresh_token}"})

    dados = rota_refresh.json()

    assert rota_refresh.status_code == HTTPStatus.OK
    assert "access_token" in dados
    assert dados["token_type"] == "bearer"
    
def test_verificar_refresh_token_invalido(usuario_autenticado):
    rota_refresh = usuario_autenticado.post("/usuarios/refresh", headers={"Authorization": "Bearer refresh_token_invalido"})

    assert rota_refresh.status_code == HTTPStatus.UNAUTHORIZED


def test_virificar_refresh_token_expirado(usuario_autenticado): 
    usuario = usuario_autenticado.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",      
    })

    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    refresh_token = criar_token(
        id_usuario,
        duracao_token=timedelta(days=-1),
        tipo_token="refresh"
    )

    rota_refresh = usuario_autenticado.post("/usuarios/refresh", headers={"Authorization": f"Bearer {refresh_token}"})

    assert rota_refresh.status_code == HTTPStatus.UNAUTHORIZED


def test_utilizar_access_token_como_refresh_token(usuario_autenticado):
    usuario = usuario_autenticado.post("/usuarios/", json={
        "nome": "teste",
        "email": "teste@gmail.com",
        "senha": "12345678",         
    })
    assert usuario.status_code == HTTPStatus.OK

    id_usuario = usuario.json()["id"]

    access_token = criar_token(
        id_usuario, 
        duracao_token=timedelta(minutes=30),
        tipo_token="access"
    )

    rota_refresh = usuario_autenticado.post("/usuarios/refresh", headers={"Authorization": f"Bearer {access_token}"})

    assert rota_refresh.status_code == HTTPStatus.UNAUTHORIZED


def test_verificar_refresh_token_sem_sub(usuario_autenticado):
    dic_info = {
        "tipo": "refresh"
    }

    refresh_token_sem_sub = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    rota_refresh = usuario_autenticado.post("/usuarios/refresh", headers={"Authorization": f"Bearer {refresh_token_sem_sub}"})

    assert rota_refresh.status_code == HTTPStatus.UNAUTHORIZED


def test_verificar_refersh_token_com_sub_invalido(usuario_autenticado):
    dic_info = {
        "sub": "abc",
        "tipo": "refresh"
    }

    refresh_token_com_sub_invalido = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    rota_refresh = usuario_autenticado.post("/usuarios/refresh", headers={"Authorization": f"Bearer {refresh_token_com_sub_invalido}"})

    assert rota_refresh.status_code == HTTPStatus.UNAUTHORIZED

def test_verifcar_refresh_token_de_usuario_inexistente(usuario_autenticado):
    dic_info = {
        "sub": str(999),
        "tipo": "refresh"
    }

    refresh_token_usuario_inexistente = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    rota_refresh = usuario_autenticado.post("/usuarios/refresh", headers={"Authorization": f"Bearer {refresh_token_usuario_inexistente}"})

    assert rota_refresh.status_code == HTTPStatus.UNAUTHORIZED