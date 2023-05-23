from sqlalchemy import Column, Integer, String, SmallInteger, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    email = Column(String(150), unique=True, index=True)
    senha = Column(String(255))
    Compras = relationship("Compra", back_populates="usuario")

class Compra(Base):
    __tablename__ = 'Compras'
    
    id = Column(Integer, primary_key=True, index=True)
    data_compra = Column(Date)
    status = Column(SmallInteger)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="Compras")
    Produtos = relationship("Produto", secondary="itens_Compra", back_populates='Compras')

class Produto(Base):
    __tablename__ = 'Produtos'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150))
    valor = Column(String(1000))
    Compras = relationship("Compra", secondary="itens_Compra", back_populates='Produtos')

itens_Compra = Table('itens_Compra', Base.metadata,
    Column('id_Produto', ForeignKey('Produtos.id'), primary_key=True),
    Column('id_Compra', ForeignKey('Compras.id'), primary_key=True)
)