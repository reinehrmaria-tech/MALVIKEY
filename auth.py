"""Regras de autenticação."""

from database import buscar_usuario


def autenticar(usuario: str, senha: str):
    """
    Valida credenciais.
    Retorna um dicionário com os dados do usuário ou None.
    """
    usuario = (usuario or "").strip()
    senha = (senha or "").strip()

    if not usuario or not senha:
        return None

    return buscar_usuario(usuario, senha)