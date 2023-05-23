from sqlalchemy.orm import Session
from exceptions import UsuarioAlreadyExistError, UsuarioNotFoundError, ProdutoNotFoundError, CompraNotFoundError
import bcrypt, models, schemas

# usuário
def check_usuario(db: Session, usuario: schemas.UsuarioLoginSchema):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if db_usuario is None:
        return False
    return bcrypt.checkpw(usuario.senha.encode('utf8'), db_usuario.senha.encode('utf8'))

def get_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = db.query(models.Usuario).get(usuario_id)
    if db_usuario is None:
        raise UsuarioNotFoundError
    return db_usuario

def get_all_usuarios(db: Session, offset: int, limit: int):
    return db.query(models.Usuario).offset(offset).limit(limit).all()

def get_usuario_by_email(db: Session, usuario_email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == usuario_email).first()

def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    db_usuario = get_usuario_by_email(db, usuario.email)
    # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
    usuario.senha = bcrypt.hashpw(usuario.senha.encode('utf8'), bcrypt.gensalt())
    if db_usuario is not None:
        raise UsuarioAlreadyExistError
    db_usuario = models.Usuario(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def update_usuario(db: Session, usuario_id: int, usuario: schemas.UsuarioCreate):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db_usuario.nome = usuario.nome
    db_usuario.email = usuario.email
    if usuario.senha != "":
        # O parâmetro rounds do gensalt determina a complexidade. O padrão é 12.
        db_usuario.senha = bcrypt.hashpw(usuario.senha.encode('utf8'), bcrypt.gensalt())
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete_usuario_by_id(db: Session, usuario_id: int):
    db_usuario = get_usuario_by_id(db, usuario_id)
    db.delete(db_usuario)
    db.commit()
    return


# produto
def get_produto_by_id(db: Session, produto_id: int):
    db_produto = db.query(models.Produto).get(produto_id)
    if db_produto is None:
        raise ProdutoNotFoundError
    return db_produto

def get_all_produtos(db: Session, offset: int, limit: int):
    return db.query(models.Produto).offset(offset).limit(limit).all()

def create_produto(db: Session, produto: schemas.ProdutoCreate):
    db_produto = models.Produto(**produto.dict())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

def update_produto(db: Session, produto_id: int, produto: schemas.ProdutoCreate):
    db_produto = get_produto_by_id(db, produto_id)
    db_produto.titulo = produto.titulo
    db_produto.resumo = produto.resumo
    db.commit()
    db.refresh(db_produto)
    return db_produto

def delete_produto_by_id(db: Session, produto_id: int):
    db_produto = get_produto_by_id(db, produto_id)
    db.delete(db_produto)
    db.commit()
    return

# compra
def create_compra(db: Session, compra: schemas.CompraCreate):
    get_usuario_by_id(db, compra.id_usuario)
    db_compra = models.compra(id_usuario=compra.id_usuario, status=compra.status, data_retirada=compra.data_retirada)
    if (produtos := db.query(models.Produto).filter(models.Produto.id.in_(compra.produto_ids))).count() == len(compra.produto_ids):
        db_compra.produtos.extend(produtos)
    else:
        raise ProdutoNotFoundError

    db.add(db_compra)
    db.commit()
    db.refresh(db_compra)
    return db_compra

def get_compra_by_id(db: Session, compra_id: int):
    db_compra = db.query(models.Compra).get(compra_id)
    if db_compra is None:
        raise CompraNotFoundError
    return db_compra

def get_all_compras(db: Session, offset: int, limit: int):
    return db.query(models.Compra).offset(offset).limit(limit).all()

def update_compra(db: Session, compra_id: int, compra: schemas.CompraUpdate):
    db_compra = get_compra_by_id(db, compra_id)
    db_compra.status = compra.status
    db.commit()
    db.refresh(db_compra)
    return db_compra