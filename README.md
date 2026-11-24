# Sistema de Estoque — API REST

API REST desenvolvida com Python e FastAPI para gerenciamento de usuários, produtos e pedidos. O projeto utiliza autenticação JWT, controle de acesso por níveis de permissão, banco de dados SQLite e testes automatizados com Pytest.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- Pydantic
- JWT (python-jose)
- Passlib e bcrypt
- python-dotenv
- Pytest

## Funcionalidades

### Produtos

- Cadastrar produtos.
- Listar produtos.
- Consultar produto por ID.
- Atualizar produtos.
- Excluir produtos.
- Validar preço e quantidade em estoque.
- Restringir operações de escrita a administradores.

### Usuários

- Cadastrar usuários.
- Autenticar usuários.
- Gerar access tokens e refresh tokens.
- Renovar access tokens.
- Listar, consultar, atualizar e excluir usuários.
- Restringir operações administrativas a administradores.
- Impedir que usuários comuns definam ou alterem o próprio nível de administrador pela API.

### Pedidos

- Criar pedidos para o usuário autenticado.
- Consultar um pedido específico.
- Listar todos os pedidos, operação restrita a administradores.
- Validar disponibilidade de estoque.
- Registrar os produtos, quantidades e preços dos itens do pedido.

## Endpoints

### Produtos — `/produtos`

| Método | Endpoint | Descrição | Permissão |
|---|---|---|---|
| GET | `/produtos/` | Lista os produtos | Público |
| POST | `/produtos/` | Cadastra um produto | Administrador |
| GET | `/produtos/{id}` | Busca um produto pelo ID | Público |
| DELETE | `/produtos/{id}` | Exclui um produto | Administrador |
| PUT | `/produtos/{id}` | Atualiza um produto | Administrador |

### Usuários — `/usuarios`

| Método | Endpoint | Descrição | Permissão |
|---|---|---|---|
| POST | `/usuarios/login` | Autentica um usuário usando JSON | Público |
| POST | `/usuarios/login-form` | Autentica usando formulário OAuth2 | Público |
| GET | `/usuarios/` | Lista os usuários | Administrador |
| POST | `/usuarios/` | Cadastra um usuário | Público |
| GET | `/usuarios/{id}` | Busca um usuário pelo ID | Administrador |
| DELETE | `/usuarios/{id}` | Exclui um usuário | Administrador |
| PUT | `/usuarios/{id}` | Atualiza um usuário | Administrador |
| POST | `/usuarios/refresh` | Gera um novo access token | Refresh token |

### Pedidos — `/pedidos`

| Método | Endpoint | Descrição | Permissão |
|---|---|---|---|
| GET | `/pedidos/` | Lista todos os pedidos | Administrador |
| POST | `/pedidos/` | Cria um pedido para o usuário autenticado | Usuário autenticado |
| GET | `/pedidos/{id}` | Consulta um pedido específico | Usuário autenticado, respeitando a propriedade do pedido |

## Autenticação

A API utiliza JWT (JSON Web Token) para autenticar usuários e controlar o acesso aos endpoints protegidos.

O processo funciona da seguinte maneira:

1. O usuário realiza o login informando suas credenciais.
2. A API verifica o e-mail e a senha.
3. Se as credenciais forem válidas, são gerados um access token e um refresh token.
4. O access token é utilizado para acessar endpoints protegidos.
5. Quando necessário, o refresh token pode ser enviado para `/usuarios/refresh` para obter um novo access token.

O token deve ser enviado no cabeçalho da requisição:

```text
Authorization: Bearer SEU_TOKEN
```

As permissões são verificadas de acordo com o tipo de usuário e o endpoint solicitado.

## Regras de negócio

- O e-mail dos usuários deve ser único.
- As senhas são armazenadas utilizando hash.
- Usuários comuns não podem acessar endpoints administrativos.
- Usuários não podem se promover a administradores por meio do cadastro ou da atualização pública.
- Produtos não podem possuir preço ou estoque negativo.
- A quantidade de itens em um pedido deve ser maior ou igual a 1.
- Um pedido só pode ser criado quando existe estoque suficiente.
- O preço unitário dos itens é registrado no momento da criação do pedido.
- Usuários autenticados só podem consultar os próprios pedidos.

## Como executar o projeto

### Pré-requisitos

Antes de começar, é necessário ter instalado:

- Git
- Python 3.14
- Windows com PowerShell (os comandos abaixo foram preparados para esse ambiente)

Para verificar se o Python está instalado:

```powershell
py -3.14 --version
```

### 1. Clonar o repositório

```powershell
git clone https://github.com/rubendamasceno/sistema_estoque.git
```

### 2. Entrar na pasta do projeto

```powershell
cd sistema_estoque
```

### 3. Criar um ambiente virtual

```powershell
py -3.14 -m venv .venv
```

### 4. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a execução do script, permita a execução somente na sessão atual do terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Em seguida, execute novamente o comando de ativação do ambiente virtual.

### 5. Instalar as dependências

Com o ambiente virtual ativado:

```powershell
python -m pip install -r requirements.txt
```

### 6. Configurar as variáveis de ambiente

Copie o arquivo de exemplo para criar seu arquivo local:

```powershell
Copy-Item .env.example .env
```

Abra o arquivo `.env` e configure as variáveis:

```env
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

- `SECRET_KEY`: chave secreta utilizada para assinar e validar os tokens JWT. Gere uma chave própria e forte.
- `ALGORITHM`: algoritmo utilizado na assinatura dos tokens. O valor utilizado pelo projeto é `HS256`.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: tempo de validade do access token em minutos. O exemplo utiliza `30`.

Não compartilhe sua chave secreta e não envie o arquivo `.env` para o Git. O arquivo `.env.example` serve apenas como modelo, sem conter sua chave privada.

### 7. Executar as migrações do banco de dados

```powershell
python -m alembic upgrade head
```

O projeto utiliza SQLite. As migrações do Alembic criam e atualizam a estrutura do banco de dados local.

### 8. Iniciar a API

```powershell
python -m uvicorn main:app --reload
```

A documentação interativa estará disponível em:

- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Administrador

O cadastro público cria usuários comuns. Por segurança, não é permitido que uma pessoa escolha ou altere o próprio nível de administrador pelas rotas públicas da API.

Para realizar testes locais com uma conta administradora, primeiro crie um usuário normalmente pela API. Depois, com a API parada, execute no PowerShell, na pasta raiz do projeto e com o ambiente virtual ativado, o comando abaixo. Substitua o e-mail pelo endereço da conta que deseja promover:

```powershell
python -c "import sqlite3; c=sqlite3.connect('db.sqlite'); cur=c.execute('UPDATE usuarios SET admin = 1 WHERE email = ?', ('seu-email@email.com',)); c.commit(); print('Usuarios atualizados:', cur.rowcount); c.close()"
```

Se o resultado for `Usuarios atualizados: 1`, a conta foi promovida a administradora no banco local. Se retornar `0`, confira se o e-mail informado corresponde a um usuário cadastrado.

Depois, inicie a API novamente, faça login com essa conta e utilize o token para testar os endpoints administrativos.

**Atenção:** essa alteração é destinada apenas ao ambiente local de desenvolvimento e testes. Não conceda privilégios administrativos a usuários sem autorização em um ambiente real.

## Testes

O projeto utiliza Pytest para executar testes automatizados das rotas, validações, autenticação e permissões.

Executar os testes:

```powershell
python -m pytest -v
```

Executar os testes com relatório de cobertura:

```powershell
python -m pytest --cov --cov-report=term-missing
```

## Autor

Ruben Damasceno

GitHub: https://github.com/RubenDamasceno