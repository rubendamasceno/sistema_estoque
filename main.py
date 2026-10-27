from fastapi import FastAPI


app = FastAPI()

from routes.produtos import produtos_router
from routes.usuario import usuario_router
from routes.pedido import pedido_router

app.include_router(produtos_router)
app.include_router(usuario_router)
app.include_router(pedido_router)