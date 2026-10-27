# Sistema de Estoque

API REST para gerenciamento de estoque, usuários e pedidos, desenvolvida com **Python, FastAPI e SQLAlchemy**.

O sistema permite cadastrar produtos, gerenciar usuários e registrar pedidos. Ao criar um pedido, a API valida a disponibilidade dos produtos e atualiza automaticamente as quantidades em estoque.

Este é meu primeiro projeto de API, desenvolvido para colocar em prática conceitos de desenvolvimento backend, bancos de dados relacionais, autenticação JWT e regras de negócio.

## Tecnologias utilizadas

- **Python** — linguagem de programação
- **FastAPI** — desenvolvimento da API REST
- **SQLAlchemy** — ORM e comunicação com o banco de dados
- **SQLite** — banco de dados relacional
- **Alembic** — controle de migrações do banco
- **Pydantic** — validação de dados
- **python-jose** — geração e validação de tokens JWT
- **Passlib e bcrypt** — hash de senhas
- **python-dotenv** — gerenciamento de variáveis de ambiente

## Funcionalidades

### Usuários e autenticação

- Cadastro de usuários e autenticação por e-mail e senha
- Armazenamento de senhas com hash bcrypt
- Autenticação JWT com access token e refresh token
- Controle de permissões entre usuários comuns e administradores
- Gerenciamento de usuários por administradores

### Produtos

- Cadastro, consulta, atualização e exclusão de produtos
- Consulta pública de produtos
- Restrição das operações de escrita a administradores
- Controle de quantidade disponível em estoque

### Pedidos

- Criação de pedidos com múltiplos produtos
- Associação automática do pedido ao usuário autenticado
- Consulta de pedidos pelo próprio usuário
- Listagem geral de pedidos por administradores
- Atualização automática do estoque após a criação do pedido

## Regras de negócio

A criação de pedidos envolve validações para manter a consistência dos dados:

1. **Identificação do cliente:** o usuário responsável pelo pedido é identificado pelo token de autenticação, não por um ID informado no corpo da requisição.
2. **Validação dos produtos:** a API verifica se os produtos solicitados existem.
3. **Verificação de estoque:** o pedido não é concluído quando a quantidade disponível é insuficiente.
4. **Produtos repetidos:** quando um produto aparece mais de uma vez, suas quantidades são consideradas em conjunto.
5. **Registro de preços:** o preço de cada item é obtido do produto no momento da criação do pedido.
6. **Transações:** a criação do pedido, o registro dos itens e a atualização do estoque acontecem em uma única transação, com rollback em caso de falha no banco.
7. **Controle de acesso:** usuários autenticados podem consultar seus próprios pedidos, enquanto administradores podem listar todos.

## Endpoints

### Usuários — `/usuarios`

| Método | Endpoint | Acesso |
|---|---|---|
| POST | `/usuarios/` | Público |
| POST | `/usuarios/login` | Público |
| POST | `/usuarios/login-form` | Público |
| POST | `/usuarios/refresh` | Refresh token |
| GET | `/usuarios/` | Administrador |
| GET | `/usuarios/{id}` | Administrador |
| PUT | `/usuarios/{id}` | Administrador |
| DELETE | `/usuarios/{id}` | Administrador |

### Produtos — `/produtos`

| Método | Endpoint | Acesso |
|---|---|---|
| GET | `/produtos/` | Público |
| GET | `/produtos/{id}` | Público |
| POST | `/produtos/` | Administrador |
| PUT | `/produtos/{id}` | Administrador |
| DELETE | `/produtos/{id}` | Administrador |

### Pedidos — `/pedidos`

| Método | Endpoint | Acesso |
|---|---|---|
| POST | `/pedidos/` | Usuário autenticado |
| GET | `/pedidos/{id}` | Usuário autenticado, proprietário do pedido |
| GET | `/pedidos/` | Administrador |

## Como executar o projeto

**Pré-requisitos:** Python e Git instalados.

### 1. Clonar o repositório

```bash
git clone https://github.com/rubendamasceno/sistema_estoque.git
cd sistema_estoque
```

### 2. Criar e ativar um ambiente virtual

```bash
python -m venv .venv
```

No Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto, utilizando o `.env.example` como referência:

```dotenv
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Para gerar uma chave secreta aleatória:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Substitua `sua_chave_secreta` pelo valor gerado.

O arquivo `.env` não deve ser enviado ao GitHub.

### 5. Aplicar as migrações do banco de dados

```bash
alembic upgrade head
```

### 6. Iniciar a API

```bash
uvicorn main:app --reload
```

A API ficará disponível localmente em:

`http://127.0.0.1:8000`

Documentação interativa (Swagger UI):

`http://127.0.0.1:8000/docs`

## Exemplo de requisição

Para criar um pedido, envie uma requisição autenticada para `POST /pedidos/` com um corpo semelhante a:

```json
{
  "itens": [
    {
      "id_produto": 1,
      "quantidade": 2
    },
    {
      "id_produto": 3,
      "quantidade": 1
    }
  ]
}
```

Os produtos precisam existir no banco e possuir estoque suficiente.

## Testando a API pelo Swagger

1. Cadastre um usuário usando `POST /usuarios/`.
2. Faça login pelo botão **Authorize**, informando o e-mail no campo `username` e a senha.
3. Utilize o token de acesso para testar os endpoints protegidos.
4. Para testar as operações administrativas, utilize um usuário com a permissão `admin`.

## Observações e limitações

Este projeto foi desenvolvido com foco no aprendizado e na execução em ambiente local.

- **Cadastro de administradores:** para facilitar os testes em ambiente local, o endpoint público de cadastro permite definir o campo `admin: true`. Essa decisão foi intencional e limitada ao contexto educacional do projeto. Em um ambiente de produção, a atribuição de permissões administrativas exigiria um mecanismo de autorização adequado, impedindo que usuários comuns elevassem seus próprios privilégios.
- **Banco de dados:** o projeto utiliza SQLite para persistência local.
- **Testes:** as funcionalidades foram verificadas manualmente pelo Swagger; ainda não existe uma suíte de testes automatizados.
- **Deploy:** a API ainda não está hospedada em um servidor público.

## Autor

Ruben Damasceno