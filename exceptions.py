class UsuarioException(Exception):
    ...

class UsuarioNotFoundError(UsuarioException):
    def __init__(self):
        self.status_code = 404
        self.detail = "USUARIO_NAO_ENCONTRADO"


class UsuarioAlreadyExistError(UsuarioException):
    def __init__(self):
        self.status_code = 409
        self.detail = "EMAIL_DUPLICADO"

class CompraException(Exception):
    ...

class CompraNotFoundError(CompraException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Compra_NAO_ENCONTRADO"
class ProdutoException(Exception):
    ...

class ProdutoNotFoundError(ProdutoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Produto_NAO_ENCONTRADO"