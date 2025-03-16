import sqlite3

con = sqlite3.connect("../../db/components.db")
cur = con.cursor()
cur.execute("DELETE FROM sockets")
con.commit()
con.close()

current_sockets = [
    "AMD Socket sTR5",
    "AMD Socket TR4",
    "FCLGA1851",
    "AMD Socket AM5",
    "FCLGA1700",
    "AMD Socket AM4",
    "FCLGA2066",
    "AMD Socket SP3r2",
    "FCLGA1200",
    "FCBGA1787",
    "AMD Socket FP7",
    "FCLGA1151",
    "FCLGA2011",
    "AMD Socket FP6",
    "FCBGA1440",
    "AMD Socket AM3+",
    "AMD Socket FP5",
    "FCLGA1150",
    "FCBGA1364",
    "FCLGA1366",
    "FCLGA1155",
    "AMD Socket AM3",
    "BGA1338",
    "AMD Socket FM2+",
    "AMD Socket FM1",
    "FCLGA1156",
    "FCBGA1090",
    "FCBGA1296",
    "BGA1493",
    "AMD Socket AM1",
    "FCBGA1170",
    "LGA775",
    "FT1 BGA 413-Ball"
]

from data import db_session
from data.sockets import Sockets

db_session.global_init("../../db/components.db")

db_sess = db_session.create_session()
for current_socket in current_sockets:
    socket = Sockets()
    socket.name = current_socket
    db_sess.add(socket)
db_sess.commit()

sockets = db_sess.query(Sockets).all()

for socket in sockets:
    print(socket.name)
