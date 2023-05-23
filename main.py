from fastapi import FastAPI, Depends, HTTPException, Body
from auth.auth_handler import signJWT
from auth.auth_bearer import JWTBearer
from sqlalchemy.orm import Session
from exceptions import UsuarioException, ProdutoException, CompraException
from database import get_db, engine
import crud, models, schemas

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# usuário
@app.get("/api/usuarios/{usuario_id}", response_model=schemas.Usuario, dependencies=[Depends(JWTBearer())])
def get_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_usuario_by_id(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/usuarios", response_model=schemas.PaginatedUsuario, dependencies=[Depends(JWTBearer())])
def get_all_usuarios(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_usuarios = crud.get_all_usuarios(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_usuarios}
    return response

@app.post("/api/usuarios", response_model=schemas.Usuario, dependencies=[Depends(JWTBearer())])
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_usuario(db, usuario)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/usuarios/{usuario_id}", response_model=schemas.Usuario, dependencies=[Depends(JWTBearer())])
def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.update_usuario(db, usuario_id, usuario)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/usuarios/{usuario_id}", dependencies=[Depends(JWTBearer())])
def delete_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_usuario_by_id(db, usuario_id)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

# produto
@app.get("/api/produtos/{produto_id}", response_model=schemas.Produto, dependencies=[Depends(JWTBearer())])
def get_produto_by_id(produto_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_produto_by_id(db, produto_id)
    except ProdutoException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/produtos", response_model=schemas.PaginatedProduto, dependencies=[Depends(JWTBearer())])
def get_all_produtos(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_produtos = crud.get_all_produtos(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_produtos}
    return response

@app.post("/api/produtos", response_model=schemas.Produto, dependencies=[Depends(JWTBearer())])
def create_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_produto(db, produto)
    except ProdutoException as cie:
        raise HTTPException(**cie.__dict__)

@app.put("/api/produtos/{produto_id}", response_model=schemas.Produto, dependencies=[Depends(JWTBearer())])
def update_produto(produto_id: int, produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    try:
        return crud.update_produto(db, produto_id, produto)
    except ProdutoException as cie:
        raise HTTPException(**cie.__dict__)

@app.delete("/api/produtos/{produto_id}")
def delete_produto_by_id(produto_id: int, db: Session = Depends(get_db), dependencies=[Depends(JWTBearer())]):
    try:
        return crud.delete_produto_by_id(db, produto_id)
    except ProdutoException as cie:
        raise HTTPException(**cie.__dict__)


# empréstimo
@app.post("/api/compras", response_model=schemas.Compra, dependencies=[Depends(JWTBearer())])
def create_compra(compra: schemas.CompraCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_compra(db, compra)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/compras/{compra_id}", response_model=schemas.Compra, dependencies=[Depends(JWTBearer())])
def get_compra_by_id(compra_id: int, db: Session = Depends(get_db)):
    try:
        return crud.get_compra_by_id(db, compra_id)
    except CompraException as cie:
        raise HTTPException(**cie.__dict__)

@app.get("/api/compras", response_model=schemas.PaginatedCompra, dependencies=[Depends(JWTBearer())])
def get_all_compras(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    db_compras = crud.get_all_compras(db, offset, limit)
    response = {"limit": limit, "offset": offset, "data": db_compras}
    return response

@app.put("/api/compras/{compra_id}", response_model=schemas.Compra, dependencies=[Depends(JWTBearer())])
def update_compra(compra_id: int, compra: schemas.CompraUpdate, db: Session = Depends(get_db)):
    return crud.update_compra(db, compra_id, compra)

# login
@app.post("/api/signup", tags=["usuario"])
async def create_usuario_signup(usuario: schemas.UsuarioCreate = Body(...), db: Session
= Depends(get_db)):
    try:
        crud.create_usuario(db, usuario)
        return signJWT(usuario.email)
    except UsuarioException as cie:
        raise HTTPException(**cie.__dict__)

# login
@app.post("/api/login", tags=["usuario"])
async def user_login(usuario: schemas.UsuarioLoginSchema = Body(...), db: Session = 
Depends(get_db)):
    if crud.check_usuario(db, usuario):
        return signJWT(usuario.email)
    return {
        "error": "E-mail ou senha incorretos!"
    }
