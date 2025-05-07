import sqlite3
from data.db_imports import *
from pprint import pprint


def filling_db():
    current_memory_types = ["DDR5", "DDR4", "DDR3"]

    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM memory_types")
    con.commit()
    con.close()

    db_session.global_init("../../db/components.db")

    db_sess = db_session.create_session()
    for current_memory_type in current_memory_types:
        memory_type = MemoryTypes()
        memory_type.name = current_memory_type
        db_sess.add(memory_type)
    db_sess.commit()

    memory_types = db_sess.query(MemoryTypes).all()

    for memory_type in memory_types:
        print(memory_type.name)


filling_db() # обновлять только после анонса новых типов
