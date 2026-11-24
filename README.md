# Sistema de Estoque — API REST

API REST desenvolvida com **Python e FastAPI** para gerenciamento de usuários, produtos e pedidos. O projeto utiliza autenticação JWT, controle de acesso por níveis de permissão, banco de dados SQLite e testes automatizados com Pytest.

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

As rotas abaixo estão organizadas conforme a ordem de declaração nos arquivos do projeto.

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

`Authorization: Bearer SEU_TOKEN`

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

### 1. Clonar o repositório

```bash
git clone https://github.com/RubenDamasceno/sistema_estoque.git
```

### 2. Entrar na pasta do projeto

```bash
cd sistema_estoque
```

### 3. Criar um ambiente virtual

```bash
python -m venv .venv
```

Ativar no Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Utilize uma chave secreta própria e mantenha o arquivo `.env` fora do controle de versão.

### 6. Executar as migrações

```bash
alembic upgrade head
```

### 7. Iniciar a API

```bash
uvicorn main:app --reload
```

A documentação interativa estará disponível em:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Administrador

O cadastro público cria usuários comuns. Para configurar um administrador no ambiente local, é necessário alterar o campo `admin` diretamente no banco SQLite.

Exemplo:

```sql
UPDATE usuarios
SET admin = 1
WHERE email = 'seu-email@email.com';
```

Substitua o e-mail pelo cadastro desejado. Essa alteração deve ser feita diretamente no banco, não por uma rota pública da API.

## Testes

O projeto utiliza Pytest para executar testes automatizados das rotas, validações, autenticação e permissões.

Executar os testes:

```bash
python -m pytest -v
```

Executar os testes com relatório de cobertura:

```bash
python -m pytest --cov --cov-report=term-missing
```

## Autor

**Ruben Damasceno**

GitHub: [github.com/RubenDamasceno](https://github.com/RubenDamasceno)