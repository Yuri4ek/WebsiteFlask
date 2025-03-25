import sqlite3

con = sqlite3.connect("../../db/components.db")
cur = con.cursor()
cur.execute("DELETE FROM motherboards")
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
current_memory_types = {"DDR2": 1, "DDR3": 2, "DDR4": 3, "DDR5": 4}
motherboards = [
    # AMD Socket sTR5 (серверные, премиум)
    ("ASRock WRX80 Creator", "AMD Socket sTR5", "DDR5", True, "E-ATX", 599,
     "USD"),
    ("Gigabyte WRX80 SU8", "AMD Socket sTR5", "DDR5", True, "E-ATX", 650,
     "USD"),
    ("ASUS Pro WS WRX80E-SAGE", "AMD Socket sTR5", "DDR5", True, "E-ATX", 580,
     "USD"),
    ("MSI WRX80-A Pro", "AMD Socket sTR5", "DDR5", True, "ATX", 450, "USD"),
    (
        "Supermicro H13SRD", "AMD Socket sTR5", "DDR5", True, "E-ATX", 700,
        "USD"),

    # AMD Socket TR4 (премиум для Threadripper)
    ("Gigabyte TRX40 AORUS Pro", "AMD Socket TR4", "DDR4", True, "ATX", 399,
     "USD"),
    (
        "ASUS ROG Zenith II Extreme", "AMD Socket TR4", "DDR4", True, "E-ATX",
        550,
        "USD"),
    ("MSI TRX40 PRO 10G", "AMD Socket TR4", "DDR4", True, "ATX", 350, "USD"),
    (
        "ASRock TRX40 Creator", "AMD Socket TR4", "DDR4", True, "ATX", 450,
        "USD"),
    (
        "ASUS Prime TRX40-Pro", "AMD Socket TR4", "DDR4", True, "ATX", 299,
        "USD"),

    # FCLGA1851 (новый Intel, предположительно)
    ("ASUS Z890 Maximus Hero", "FCLGA1851", "DDR5", True, "ATX", 500, "USD"),
    (
        "Gigabyte Z890 Aorus Elite", "FCLGA1851", "DDR5", True, "ATX", 400,
        "USD"),
    ("MSI MPG Z890 Edge TI", "FCLGA1851", "DDR5", True, "ATX", 450, "USD"),
    ("ASRock Z890 Steel Legend", "FCLGA1851", "DDR5", True, "ATX", 350, "USD"),
    ("EVGA Z890 Dark", "FCLGA1851", "DDR5", True, "E-ATX", 600, "USD"),

    # AMD Socket AM5 (новейшие AMD)
    ("ASRock X870E Taichi", "AMD Socket AM5", "DDR5", True, "E-ATX", 450,
     "USD"),
    ("Gigabyte B650E Aorus Master", "AMD Socket AM5", "DDR5", True, "ATX", 349,
     "USD"),
    (
        "MSI MPG X670E Carbon", "AMD Socket AM5", "DDR5", True, "ATX", 400,
        "USD"),
    ("ASUS ROG Crosshair X670E Hero", "AMD Socket AM5", "DDR5", True, "ATX",
     550, "USD"),
    ("ASRock B650M PG Riptide", "AMD Socket AM5", "DDR5", True, "Micro ATX",
     250, "USD"),

    # FCLGA1700 (Intel 12th-14th Gen)
    ("ASRock Z790 Taichi Lite", "FCLGA1700", "DDR5", True, "ATX", 350, "USD"),
    ("Gigabyte Z790 Aorus Elite AX", "FCLGA1700", "DDR5", True, "ATX", 300,
     "USD"),
    ("MSI MAG B760M Mortar", "FCLGA1700", "DDR5", True, "Micro ATX", 190,
     "USD"),
    ("ASUS PRIME Z690-P", "FCLGA1700", "DDR5", True, "ATX", 250, "USD"),
    ("ASUS ROG Maximus Z790 Apex", "FCLGA1700", "DDR5", True, "E-ATX", 500,
     "USD"),

    # AMD Socket AM4 (популярный)
    (
        "ASUS ROG Strix B550-F Gaming", "AMD Socket AM4", "DDR4", True, "ATX",
        180,
        "USD"),
    ("MSI B450 Tomahawk Max", "AMD Socket AM4", "DDR4", True, "ATX", 120,
     "USD"),
    ("Gigabyte X570 Aorus Elite", "AMD Socket AM4", "DDR4", True, "ATX", 200,
     "USD"),
    ("ASRock B550 Steel Legend", "AMD Socket AM4", "DDR4", True, "ATX", 150,
     "USD"),
    (
        "ASUS ROG Crosshair VIII Hero", "AMD Socket AM4", "DDR4", True, "ATX",
        350,
        "USD"),

    # FCLGA2066 (Intel High-End Desktop)
    ("ASUS ROG Strix X299-E", "FCLGA2066", "DDR4", True, "ATX", 250, "USD"),
    ("Gigabyte X299 UD4 Pro", "FCLGA2066", "DDR4", True, "ATX", 200, "USD"),
    ("MSI X299 Raider", "FCLGA2066", "DDR4", True, "ATX", 180, "USD"),
    ("ASRock X299 Taichi", "FCLGA2066", "DDR4", True, "ATX", 300, "USD"),
    ("EVGA X299 Dark", "FCLGA2066", "DDR4", True, "E-ATX", 400, "USD"),

    # AMD Socket SP3r2 (серверные)
    ("Supermicro H11DSi-NT", "AMD Socket SP3r2", "DDR4", True, "E-ATX", 600,
     "USD"),
    ("ASRock Rack EPYCD8-2T", "AMD Socket SP3r2", "DDR4", True, "ATX", 450,
     "USD"),
    ("Gigabyte MZ32-AR0", "AMD Socket SP3r2", "DDR4", True, "E-ATX", 550,
     "USD"),
    ("Tyan S8253GM2NE", "AMD Socket SP3r2", "DDR4", True, "ATX", 500, "USD"),
    ("ASUS KRPA-U16", "AMD Socket SP3r2", "DDR4", True, "E-ATX", 650, "USD"),

    # FCLGA1200 (Intel 10th-11th Gen)
    ("MSI B460M-A PRO", "FCLGA1200", "DDR4", True, "Micro ATX", 100, "USD"),
    ("ASUS PRIME H410M-E", "FCLGA1200", "DDR4", False, "Micro ATX", 80, "USD"),
    ("Gigabyte H470 AORUS Pro", "FCLGA1200", "DDR4", True, "ATX", 150, "USD"),
    ("ASRock Z490 Steel Legend", "FCLGA1200", "DDR4", True, "ATX", 200, "USD"),
    ("ASUS ROG Strix Z590-E", "FCLGA1200", "DDR4", True, "ATX", 300, "USD"),

    # FCBGA1787 (мобильные, условно)
    ("ASUS VivoBook X712", "FCBGA1787", "DDR4", False, "Embedded", 150, "USD"),
    ("MSI Modern 14", "FCBGA1787", "DDR4", False, "Embedded", 200, "USD"),
    ("Lenovo IdeaPad 5", "FCBGA1787", "DDR4", False, "Embedded", 180, "USD"),
    ("HP Pavilion 15", "FCBGA1787", "DDR4", False, "Embedded", 250, "USD"),
    ("Dell Inspiron 14", "FCBGA1787", "DDR4", False, "Embedded", 300, "USD"),

    # AMD Socket FP7 (мобильные, условно)
    (
        "ASUS ZenBook 14", "AMD Socket FP7", "DDR4", True, "Embedded", 200,
        "USD"),
    ("Lenovo ThinkPad E14", "AMD Socket FP7", "DDR4", True, "Embedded", 250,
     "USD"),
    ("HP EliteBook 835", "AMD Socket FP7", "DDR4", True, "Embedded", 300,
     "USD"),
    ("Acer Swift 3", "AMD Socket FP7", "DDR4", True, "Embedded", 180, "USD"),
    ("Dell Latitude 5420", "AMD Socket FP7", "DDR4", True, "Embedded", 350,
     "USD"),

    # FCLGA1151 (Intel 6th-9th Gen)
    ("ASRock Z390 Taichi", "FCLGA1151", "DDR4", True, "ATX", 200, "USD"),
    ("Gigabyte Z370 AORUS Gaming 3", "FCLGA1151", "DDR4", True, "ATX", 150,
     "USD"),
    ("MSI Z390-A PRO", "FCLGA1151", "DDR4", True, "ATX", 130, "USD"),
    ("ASUS PRIME H370M-Plus", "FCLGA1151", "DDR4", True, "Micro ATX", 100,
     "USD"),
    ("ASUS ROG Maximus XI Hero", "FCLGA1151", "DDR4", True, "ATX", 300, "USD"),

    # FCLGA2011 (Intel High-End Desktop/Server)
    ("ASUS ROG Rampage V Extreme", "FCLGA2011", "DDR4", True, "E-ATX", 350,
     "USD"),
    ("Gigabyte X99-UD4", "FCLGA2011", "DDR4", True, "ATX", 250, "USD"),
    ("MSI X99A Raider", "FCLGA2011", "DDR4", True, "ATX", 200, "USD"),
    ("ASRock X99 Extreme4", "FCLGA2011", "DDR4", True, "ATX", 280, "USD"),
    ("EVGA X99 Classified", "FCLGA2011", "DDR4", True, "E-ATX", 400, "USD"),

    # AMD Socket FP6 (мобильные, условно)
    ("ASUS ROG Flow X13", "AMD Socket FP6", "DDR4", True, "Embedded", 250,
     "USD"),
    ("Lenovo Yoga Slim 7", "AMD Socket FP6", "DDR4", True, "Embedded", 300,
     "USD"),
    ("HP ProBook 445", "AMD Socket FP6", "DDR4", True, "Embedded", 200, "USD"),
    ("Acer Nitro 5", "AMD Socket FP6", "DDR4", True, "Embedded", 350, "USD"),
    ("Dell G5 15 SE", "AMD Socket FP6", "DDR4", True, "Embedded", 280, "USD"),

    # FCBGA1440 (мобильные, условно)
    ("ASRock NUC-5005U", "FCBGA1440", "DDR4", False, "Mini-ITX", 150, "USD"),
    ("Intel NUC 10 Frost Canyon", "FCBGA1440", "DDR4", False, "Mini-ITX", 200,
     "USD"),
    ("Gigabyte BRIX GB-BXi5", "FCBGA1440", "DDR4", False, "Mini-ITX", 180,
     "USD"),
    ("ASUS PN50", "FCBGA1440", "DDR4", False, "Mini-ITX", 220, "USD"),
    ("MSI Cubi 5", "FCBGA1440", "DDR4", False, "Mini-ITX", 250, "USD"),

    # AMD Socket AM3+ (старые AMD)
    ("ASRock 970 Pro3", "AMD Socket AM3+", "DDR3", False, "ATX", 90, "USD"),
    ("MSI 970A-G46", "AMD Socket AM3+", "DDR3", False, "ATX", 80, "USD"),
    ("ASUS M5A97 R2.0", "AMD Socket AM3+", "DDR3", False, "ATX", 100, "USD"),
    ("Gigabyte GA-990FXA-UD3", "AMD Socket AM3+", "DDR3", True, "ATX", 120,
     "USD"),
    ("Biostar TA970XE", "AMD Socket AM3+", "DDR3", False, "ATX", 70, "USD"),

    # AMD Socket FP5 (мобильные, условно)
    ("ASUS TUF Gaming A15", "AMD Socket FP5", "DDR4", True, "Embedded", 200,
     "USD"),
    (
        "Lenovo Legion 5", "AMD Socket FP5", "DDR4", True, "Embedded", 250,
        "USD"),
    ("HP Omen 15", "AMD Socket FP5", "DDR4", True, "Embedded", 300, "USD"),
    ("Acer Predator Helios 300", "AMD Socket FP5", "DDR4", True, "Embedded",
     350, "USD"),
    ("Dell G3 15", "AMD Socket FP5", "DDR4", True, "Embedded", 180, "USD"),

    # FCLGA1150 (Intel 4th Gen)
    ("ASUS Z97-A", "FCLGA1150", "DDR3", True, "ATX", 150, "USD"),
    ("Gigabyte GA-Z97X-UD3H", "FCLGA1150", "DDR3", True, "ATX", 130, "USD"),
    ("MSI Z97 PC Mate", "FCLGA1150", "DDR3", True, "ATX", 100, "USD"),
    ("ASRock Z97 Extreme4", "FCLGA1150", "DDR3", True, "ATX", 180, "USD"),
    ("ASUS MAXIMUS VII Hero", "FCLGA1150", "DDR3", True, "ATX", 220, "USD"),

    # FCBGA1364 (мобильные, условно)
    ("ASUS VivoBook S14", "FCBGA1364", "DDR3", False, "Embedded", 150, "USD"),
    ("Lenovo ThinkPad T440", "FCBGA1364", "DDR3", False, "Embedded", 180,
     "USD"),
    ("HP EliteBook 840", "FCBGA1364", "DDR3", False, "Embedded", 200, "USD"),
    (
        "Dell Latitude E7440", "FCBGA1364", "DDR3", False, "Embedded", 220,
        "USD"),
    ("Acer TravelMate P645", "FCBGA1364", "DDR3", False, "Embedded", 250,
     "USD"),

    # FCLGA1366 (Intel старые)
    ("ASUS P6T Deluxe", "FCLGA1366", "DDR3", False, "ATX", 150, "USD"),
    ("Gigabyte GA-EX58-UD5", "FCLGA1366", "DDR3", False, "ATX", 120, "USD"),
    ("MSI X58 Pro-E", "FCLGA1366", "DDR3", False, "ATX", 100, "USD"),
    ("ASRock X58 Extreme", "FCLGA1366", "DDR3", False, "ATX", 180, "USD"),
    ("EVGA X58 Classified", "FCLGA1366", "DDR3", False, "E-ATX", 250, "USD"),

    # FCLGA1155 (Intel 2nd-3rd Gen)
    ("ASUS P8Z77-V", "FCLGA1155", "DDR3", True, "ATX", 140, "USD"),
    ("Gigabyte GA-Z77X-UD3H", "FCLGA1155", "DDR3", True, "ATX", 120, "USD"),
    ("MSI Z77A-G45", "FCLGA1155", "DDR3", True, "ATX", 100, "USD"),
    ("ASRock Z77 Extreme4", "FCLGA1155", "DDR3", True, "ATX", 160, "USD"),
    ("ASUS Sabertooth Z77", "FCLGA1155", "DDR3", True, "ATX", 200, "USD"),

    # AMD Socket AM3 (старые AMD)
    ("ASUS M4A87TD EVO", "AMD Socket AM3", "DDR3", False, "ATX", 80, "USD"),
    ("Gigabyte GA-MA785GM-US2H", "AMD Socket AM3", "DDR2", False, "Micro ATX",
     60, "USD"),
    ("MSI 760GM-P23", "AMD Socket AM3", "DDR3", False, "Micro ATX", 70, "USD"),
    ("ASRock M3A770DE", "AMD Socket AM3", "DDR3", False, "ATX", 90, "USD"),
    ("Biostar A770E3", "AMD Socket AM3", "DDR3", False, "ATX", 100, "USD"),

    # BGA1338 (мобильные, условно)
    ("ASUS Chromebook CX9", "BGA1338", "DDR4", False, "Embedded", 150, "USD"),
    ("Lenovo Chromebook Flex 5", "BGA1338", "DDR4", False, "Embedded", 180,
     "USD"),
    ("HP Chromebook x360", "BGA1338", "DDR4", False, "Embedded", 200, "USD"),
    ("Acer Chromebook Spin 713", "BGA1338", "DDR4", False, "Embedded", 250,
     "USD"),
    ("Dell Chromebook 13", "BGA1338", "DDR4", False, "Embedded", 300, "USD"),

    # AMD Socket FM2+ (старые AMD APU)
    ("ASRock FM2A88X-ITX+", "AMD Socket FM2+", "DDR3", True, "Mini-ITX", 90,
     "USD"),
    ("MSI A88XM-E45", "AMD Socket FM2+", "DDR3", True, "Micro ATX", 80, "USD"),
    ("Gigabyte GA-F2A88XM-D3H", "AMD Socket FM2+", "DDR3", True, "Micro ATX",
     100, "USD"),
    ("ASUS A88XM-A", "AMD Socket FM2+", "DDR3", True, "Micro ATX", 70, "USD"),
    ("Biostar Hi-Fi A88W 3D", "AMD Socket FM2+", "DDR3", True, "ATX", 120,
     "USD"),

    # AMD Socket FM1 (старые AMD APU)
    ("ASUS F1A55-M LE", "AMD Socket FM1", "DDR3", False, "Micro ATX", 60,
     "USD"),
    ("Gigabyte GA-A55M-DS2", "AMD Socket FM1", "DDR3", False, "Micro ATX", 70,
     "USD"),
    ("MSI A55M-P33", "AMD Socket FM1", "DDR3", False, "Micro ATX", 50, "USD"),
    ("ASRock A55M-HVS", "AMD Socket FM1", "DDR3", False, "Micro ATX", 80,
     "USD"),
    ("Biostar TA55A", "AMD Socket FM1", "DDR3", False, "ATX", 90, "USD"),

    # FCLGA1156 (Intel 1st Gen)
    ("ASUS P7P55D-E Pro", "FCLGA1156", "DDR3", False, "ATX", 130, "USD"),
    ("Gigabyte GA-P55-UD3", "FCLGA1156", "DDR3", False, "ATX", 110, "USD"),
    ("MSI P55-GD65", "FCLGA1156", "DDR3", False, "ATX", 100, "USD"),
    ("ASRock P55 Extreme", "FCLGA1156", "DDR3", False, "ATX", 150, "USD"),
    ("Intel DP55WG", "FCLGA1156", "DDR3", False, "ATX", 170, "USD"),

    # FCBGA1090 (мобильные, условно)
    ("ASUS Eee PC 1015PEM", "FCBGA1090", "DDR2", False, "Embedded", 80, "USD"),
    (
        "Acer Aspire One D255", "FCBGA1090", "DDR2", False, "Embedded", 90,
        "USD"),
    ("Lenovo IdeaPad S10-3", "FCBGA1090", "DDR2", False, "Embedded", 100,
     "USD"),
    ("HP Mini 210", "FCBGA1090", "DDR2", False, "Embedded", 120, "USD"),
    ("Dell Mini 10", "FCBGA1090", "DDR2", False, "Embedded", 150, "USD"),

    # FCBGA1296 (мобильные, условно)
    ("ASUS Transformer Book T100", "FCBGA1296", "DDR3", False, "Embedded", 100,
     "USD"),
    ("Lenovo Miix 2", "FCBGA1296", "DDR3", False, "Embedded", 120, "USD"),
    ("HP Stream 7", "FCBGA1296", "DDR3", False, "Embedded", 140, "USD"),
    ("Acer Iconia W4", "FCBGA1296", "DDR3", False, "Embedded", 160, "USD"),
    ("Dell Venue 8 Pro", "FCBGA1296", "DDR3", False, "Embedded", 180, "USD"),

    # BGA1493 (мобильные, условно)
    ("ASUS ROG Phone 5", "BGA1493", "DDR5", True, "Embedded", 300, "USD"),
    ("Lenovo Legion Phone Duel", "BGA1493", "DDR5", True, "Embedded", 350,
     "USD"),
    ("Xiaomi Black Shark 4", "BGA1493", "DDR5", True, "Embedded", 400, "USD"),
    ("Samsung Galaxy Tab S8", "BGA1493", "DDR5", True, "Embedded", 450, "USD"),
    ("OnePlus Pad", "BGA1493", "DDR5", True, "Embedded", 500, "USD"),

    # AMD Socket AM1 (бюджетные APU)
    (
        "ASRock AM1H-ITX", "AMD Socket AM1", "DDR3", False, "Mini-ITX", 50,
        "USD"),
    ("MSI AM1I", "AMD Socket AM1", "DDR3", False, "Mini-ITX", 45, "USD"),
    ("Gigabyte GA-AM1M-S2H", "AMD Socket AM1", "DDR3", False, "Micro ATX", 60,
     "USD"),
    ("ASUS AM1M-A", "AMD Socket AM1", "DDR3", False, "Micro ATX", 55, "USD"),
    ("Biostar AM1ML", "AMD Socket AM1", "DDR3", False, "Micro ATX", 40, "USD"),

    # FCBGA1170 (мобильные, условно)
    (
        "ASUS VivoTab Note 8", "FCBGA1170", "DDR3", False, "Embedded", 100,
        "USD"),
    ("Lenovo ThinkPad 8", "FCBGA1170", "DDR3", False, "Embedded", 120, "USD"),
    ("HP Elite x2 1011", "FCBGA1170", "DDR3", False, "Embedded", 140, "USD"),
    ("Acer Aspire Switch 10", "FCBGA1170", "DDR3", False, "Embedded", 160,
     "USD"),
    ("Dell Venue 11 Pro", "FCBGA1170", "DDR3", False, "Embedded", 180, "USD"),

    # LGA775 (Intel старые)
    ("ASUS P5Q Deluxe", "LGA775", "DDR2", False, "ATX", 90, "USD"),
    ("Gigabyte GA-EP45-UD3P", "LGA775", "DDR2", False, "ATX", 80, "USD"),
    ("MSI G41M-P33 Combo", "LGA775", "DDR3", False, "Micro ATX", 70, "USD"),
    ("ASRock G31M-S", "LGA775", "DDR2", False, "Micro ATX", 60, "USD"),
    ("Intel DQ45CB", "LGA775", "DDR2", False, "Micro ATX", 100, "USD"),

    # FT1 BGA 413-Ball (мобильные, условно)
    ("ASUS Eee PC X101", "FT1 BGA 413-Ball", "DDR3", False, "Embedded", 50,
     "USD"),
    ("Acer Aspire One 522", "FT1 BGA 413-Ball", "DDR3", False, "Embedded", 60,
     "USD"),
    ("Lenovo S205", "FT1 BGA 413-Ball", "DDR3", False, "Embedded", 70, "USD"),
    ("HP dm1z", "FT1 BGA 413-Ball", "DDR3", False, "Embedded", 80, "USD"),
    (
        "Samsung NC110", "FT1 BGA 413-Ball", "DDR3", False, "Embedded", 90,
        "USD"),
]

from data import db_session
from data.motherboards import MotherBoards

db_session.global_init("../../db/components.db")

db_sess = db_session.create_session()
for current_motherboard in motherboards:
    motherboard = MotherBoards()
    motherboard.name = current_motherboard[0]
    try:
        motherboard.socket_id = current_sockets[current_motherboard[1]]
    except:
        motherboard.socket_id = None
    motherboard.memory_type_id = current_memory_types[current_motherboard[2]]
    motherboard.m2_support = current_motherboard[3]
    motherboard.form_factor = current_motherboard[4]
    motherboard.price = current_motherboard[5]
    motherboard.currency = current_motherboard[6]
    db_sess.add(motherboard)
db_sess.commit()

db_sess = db_session.create_session()
current_motherboards = db_sess.query(MotherBoards).all()

for current_motherboard in current_motherboards:
    print(current_motherboard.name)
