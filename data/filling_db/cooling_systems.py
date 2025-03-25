import sqlite3

con = sqlite3.connect("../../db/components.db")
cur = con.cursor()
cur.execute("DELETE FROM processors")
con.commit()
con.close()

current_sockets = {'AMD Socket sTR5': 1, 'AMD Socket TR4': 2, 'FCLGA1851': 3,
                   'AMD Socket AM5': 4, 'FCLGA1700': 5, 'AMD Socket AM4': 6,
                   'FCLGA2066': 7, 'AMD Socket SP3r2': 8, 'FCLGA1200': 9,
                   'FCBGA1787': 10, 'AMD Socket FP7': 11, 'FCLGA1151': 12,
                   'FCLGA2011': 13, 'AMD Socket FP6': 14, 'FCBGA1440': 15,
                   'AMD Socket AM3+': 16, 'AMD Socket FP5': 17,
                   'FCLGA1150': 18, 'FCBGA1364': 19, 'FCLGA1366': 20,
                   'FCLGA1155': 21, 'AMD Socket AM3': 22, 'BGA1338': 23,
                   'AMD Socket FM2+': 24, 'AMD Socket FM1': 25,
                   'FCLGA1156': 26, 'FCBGA1090': 27, 'FCBGA1296': 28,
                   'BGA1493': 29, 'AMD Socket AM1': 30, 'FCBGA1170': 31,
                   'LGA775': 32, 'FT1 BGA 413-Ball': 33}
coolers = [
    # AMD Socket sTR5
    {"id": 1, "name": "Noctua NH-D9 TR5-SP6", "socket": "AMD Socket sTR5",
     "tdp": 200, "type": "Air", "price": 119.90, "currency": "USD"},
    {"id": 2, "name": "Corsair H150i Elite", "socket": "AMD Socket sTR5",
     "tdp": 350, "type": "Water", "price": 189.99, "currency": "USD"},

    # AMD Socket TR4
    {"id": 3, "name": "Noctua NH-U14S TR4-SP3", "socket": "AMD Socket TR4",
     "tdp": 250, "type": "Air", "price": 89.95, "currency": "USD"},
    {"id": 4, "name": "NZXT Kraken X63", "socket": "AMD Socket TR4",
     "tdp": 300, "type": "Water", "price": 149.99, "currency": "USD"},

    # FCLGA1851
    {"id": 5, "name": "Cooler Master Hyper 212 Evo", "socket": "FCLGA1851",
     "tdp": 150, "type": "Air", "price": 39.99, "currency": "USD"},

    # AMD Socket AM5
    {"id": 6, "name": "Thermalright Peerless Assassin",
     "socket": "AMD Socket AM5", "tdp": 200, "type": "Air", "price": 49.90,
     "currency": "USD"},
    {"id": 7, "name": "Noctua NH-D15", "socket": "AMD Socket AM5", "tdp": 250,
     "type": "Air", "price": 109.95, "currency": "USD"},
    {"id": 8, "name": "EK-AIO 360 D-RGB", "socket": "AMD Socket AM5",
     "tdp": 300, "type": "Water", "price": 154.99, "currency": "USD"},

    # FCLGA1700
    {"id": 9, "name": "Corsair iCUE H100i", "socket": "FCLGA1700", "tdp": 250,
     "type": "Water", "price": 139.99, "currency": "USD"},
    {"id": 10, "name": "be quiet! Pure Rock 2", "socket": "FCLGA1700",
     "tdp": 150, "type": "Air", "price": 44.90, "currency": "USD"},

    # AMD Socket AM4
    {"id": 11, "name": "Noctua NH-U12S", "socket": "AMD Socket AM4",
     "tdp": 140, "type": "Air", "price": 69.95, "currency": "USD"},
    {"id": 12, "name": "Cooler Master MasterLiquid ML240L",
     "socket": "AMD Socket AM4", "tdp": 200, "type": "Water", "price": 79.99,
     "currency": "USD"},

    # FCLGA2066
    {"id": 13, "name": "Deepcool Assassin III", "socket": "FCLGA2066",
     "tdp": 250, "type": "Air", "price": 89.99, "currency": "USD"},

    # AMD Socket SP3r2
    {"id": 14, "name": "Dynatron R14", "socket": "AMD Socket SP3r2",
     "tdp": 180, "type": "Air", "price": 49.99, "currency": "USD"},

    # FCLGA1200
    {"id": 15, "name": "Arctic Freezer 34 eSports", "socket": "FCLGA1200",
     "tdp": 150, "type": "Air", "price": 39.99, "currency": "USD"},

    # FCBGA1787
    {"id": 16, "name": "Generic OEM Cooler", "socket": "FCBGA1787", "tdp": 65,
     "type": "Air", "price": None, "currency": "USD"},

    # AMD Socket FP7
    {"id": 17, "name": "Scythe Mugen 5", "socket": "AMD Socket FP7",
     "tdp": 120, "type": "Air", "price": 59.99, "currency": "USD"},

    # FCLGA1151
    {"id": 18, "name": "Cooler Master Hyper 212 Black", "socket": "FCLGA1151",
     "tdp": 130, "type": "Air", "price": 39.99, "currency": "USD"},
    {"id": 19, "name": "NZXT Kraken M22", "socket": "FCLGA1151", "tdp": 150,
     "type": "Water", "price": 79.99, "currency": "USD"},

    # FCLGA2011
    {"id": 20, "name": "Noctua NH-D15S", "socket": "FCLGA2011", "tdp": 250,
     "type": "Air", "price": 99.95, "currency": "USD"},

    # AMD Socket FP6
    {"id": 21, "name": "Arctic Freezer 7 X", "socket": "AMD Socket FP6",
     "tdp": 100, "type": "Air", "price": 24.99, "currency": "USD"},

    # FCBGA1440
    {"id": 22, "name": "Generic Mobile Cooler", "socket": "FCBGA1440",
     "tdp": 45, "type": "Air", "price": None, "currency": "USD"},

    # AMD Socket AM3+
    {"id": 23, "name": "Cooler Master Hyper TX3", "socket": "AMD Socket AM3+",
     "tdp": 130, "type": "Air", "price": 24.99, "currency": "USD"},

    # AMD Socket FP5
    {"id": 24, "name": "Thermalright AXP-90", "socket": "AMD Socket FP5",
     "tdp": 95, "type": "Air", "price": 29.90, "currency": "USD"},

    # FCLGA1150
    {"id": 25, "name": "be quiet! Shadow Rock 2", "socket": "FCLGA1150",
     "tdp": 160, "type": "Air", "price": 49.90, "currency": "USD"},

    # FCBGA1364
    {"id": 26, "name": "OEM Laptop Cooler", "socket": "FCBGA1364", "tdp": 55,
     "type": "Air", "price": None, "currency": "USD"},

    # FCLGA1366
    {"id": 27, "name": "Noctua NH-U12P SE2", "socket": "FCLGA1366", "tdp": 130,
     "type": "Air", "price": 59.95, "currency": "USD"},

    # FCLGA1155
    {"id": 28, "name": "Cooler Master Hyper 103", "socket": "FCLGA1155",
     "tdp": 130, "type": "Air", "price": 29.99, "currency": "USD"},

    # AMD Socket AM3
    {"id": 29, "name": "Arctic Freezer 13", "socket": "AMD Socket AM3",
     "tdp": 140, "type": "Air", "price": 29.99, "currency": "USD"},

    # BGA1338
    {"id": 30, "name": "Generic BGA Cooler", "socket": "BGA1338", "tdp": 35,
     "type": "Air", "price": None, "currency": "USD"},

    # AMD Socket FM2+
    {"id": 31, "name": "Scythe Katana 4", "socket": "AMD Socket FM2+",
     "tdp": 130, "type": "Air", "price": 34.99, "currency": "USD"},

    # AMD Socket FM1
    {"id": 32, "name": "Cooler Master GeminII M4", "socket": "AMD Socket FM1",
     "tdp": 100, "type": "Air", "price": 34.99, "currency": "USD"},

    # FCLGA1156
    {"id": 33, "name": "Zalman CNPS10X", "socket": "FCLGA1156", "tdp": 130,
     "type": "Air", "price": 39.99, "currency": "USD"},

    # FCBGA1090
    {"id": 34, "name": "Mobile OEM Cooler", "socket": "FCBGA1090", "tdp": 45,
     "type": "Air", "price": None, "currency": "USD"},

    # FCBGA1296
    {"id": 35, "name": "Generic Laptop Cooler", "socket": "FCBGA1296",
     "tdp": 55, "type": "Air", "price": None, "currency": "USD"},

    # BGA1493
    {"id": 36, "name": "BGA OEM Cooler", "socket": "BGA1493", "tdp": 65,
     "type": "Air", "price": None, "currency": "USD"},

    # AMD Socket AM1
    {"id": 37, "name": "Arctic Alpine AM1", "socket": "AMD Socket AM1",
     "tdp": 85, "type": "Air", "price": 14.99, "currency": "USD"},

    # FCBGA1170
    {"id": 38, "name": "Laptop Generic Cooler", "socket": "FCBGA1170",
     "tdp": 45, "type": "Air", "price": None, "currency": "USD"},

    # LGA775
    {"id": 39, "name": "Cooler Master Hyper N520", "socket": "LGA775",
     "tdp": 130, "type": "Air", "price": 39.99, "currency": "USD"},
    {"id": 40, "name": "Zalman CNPS9500", "socket": "LGA775", "tdp": 125,
     "type": "Air", "price": 49.99, "currency": "USD"},

    # FT1 BGA 413-Ball
    {"id": 41, "name": "FT1 OEM Cooler", "socket": "FT1 BGA 413-Ball",
     "tdp": 25, "type": "Air", "price": None, "currency": "USD"}
]

from data import db_session
from data.cooling_systems import CoolingSystems

db_session.global_init("../../db/components.db")

db_sess = db_session.create_session()
for current_cooler in coolers:
    cooler = CoolingSystems()
    cooler.name = current_cooler["name"]
    try:
        cooler.socket_id = current_sockets[current_cooler["socket"]]
    except:
        cooler.socket_id = None
    cooler.tdp = current_cooler["tdp"]
    cooler.type = current_cooler["type"]
    cooler.price = current_cooler["price"]
    cooler.currency = current_cooler["currency"]
    db_sess.add(cooler)
db_sess.commit()

db_sess = db_session.create_session()
current_coolers = db_sess.query(CoolingSystems).all()

for current_cooler in current_coolers:
    print(current_cooler.name)
