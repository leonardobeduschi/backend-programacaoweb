from datetime import date
from typing import List  
from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nome: str
    email: str
class UsuarioCreate(UsuarioBase):
    senha: str
class Usuario(UsuarioBase):
    id: int
    class Config:
        orm_mode = True
class UsuarioLoginSchema(BaseModel):
    email: str
    senha: str
    class Config:
        schema_extra = {
            "example": {
                "email": "x@x.com",
                "senha": "pass"
            }
        }
class PaginatedUsuario(BaseModel):
    limit: int
    offset: int
    data: List[Usuario]

class ProdutoBase(BaseModel):
    titulo: str
    resumo: str
class ProdutoCreate(ProdutoBase):
    pass
class Produto(ProdutoBase):
    id: int
    class Config:
        orm_mode = True
class PaginatedProduto(BaseModel):
    limit: int
    offset: int
    data: List[Produto]

class CompraBase(BaseModel):
    id_usuario: int
    status: int
    data_retirada: date
class CompraUpdate(BaseModel):
    status: int
class CompraCreate(CompraBase):
    Produto_ids: List[int] = []
    pass
class Compra(CompraBase):
    id: int
    usuario: Usuario = {}
    Produtos: List[Produto] = []
    class Config:
        orm_mode = True
class PaginatedCompra(BaseModel):
    limit: int
    offset: int
    data: List[Compra]