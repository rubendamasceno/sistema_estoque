import requests

url = "http://127.0.0.1:8000/usuarios/refresh"

refresh_token = "COLE_SEU_REFRESH_TOKEN_AQUI"

headers = {
    "Authorization": f"Bearer {refresh_token}"
}

resposta = requests.post(url, headers=headers)
print(resposta.status_code)
print(resposta.json().keys())