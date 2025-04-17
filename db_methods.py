from data.db_imports import *

db_session.global_init("db/components.db")


def get_sockets():
    db_sess = db_session.create_session()

    sockets_db = db_sess.query(Sockets).all()
    current_sockets = {}
    for socket in sockets_db:
        current_sockets[socket.id] = socket.name
    current_sockets[None] = "Неизвестно"

    return current_sockets, sockets_db


def get_memory_types():
    db_sess = db_session.create_session()

    memory_types_db = db_sess.query(MemoryTypes).all()
    current_memory_types = {}
    for memory_type in memory_types_db:
        current_memory_types[memory_type.id] = memory_type.name
    current_memory_types[None] = "Неизвестно"

    return current_memory_types, memory_types_db
