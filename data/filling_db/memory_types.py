import sqlite3

con = sqlite3.connect("../../db/components.db")
cur = con.cursor()
cur.execute("DELETE FROM memory_types")
con.commit()
con.close()

current_memory_types = ["DDR2", "DDR3", "DDR4", "DDR5"]

from data import db_session
from data.memory_types import MemoryTypes

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
