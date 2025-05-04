import json
import sqlite3
from data.db_imports import *
from pprint import pprint


def get_info():
    # Имя JSON-файла
    json_file = "components_prices.json"

    # Открываем и читаем JSON-файл
    with open(json_file, "r", encoding="utf-8") as file:
        # Загружаем JSON в словарь
        SSDs_info = json.load(file)['components']['Накопитель SSD']

    M2_SSDs_info = []
    for SSD in SSDs_info:
        if 'M.2' in SSD[0]:
            M2_SSDs_info.append(SSD)
    return SSDs_info, M2_SSDs_info


def filling_db(SSDs_info, M2_SSDs_info):
    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM SSDs")
    con.commit()
    con.close()

    db_session.global_init("../../db/components.db")

    db_sess = db_session.create_session()
    for SSD_info in M2_SSDs_info:
        capacity_gb, type, *name = SSD_info[0].split()
        name = f"{capacity_gb} {' '.join(name)}"
        if capacity_gb[-2:] == "Tb":
            capacity_gb = int(float(capacity_gb[:-2]) * 1000)
        else:
            capacity_gb = int(capacity_gb[:-2])

        SSD = SSDs()
        SSD.name = name
        SSD.m2 = True
        SSD.capacity_gb = capacity_gb
        SSD.price_in_rubles = SSD_info[1]

        db_sess.add(SSD)
    for SSD_info in SSDs_info:
        capacity_gb, type, *name = SSD_info[0].split()
        name = f"{capacity_gb} {' '.join(name)}"
        if capacity_gb[-2:] == "Tb":
            capacity_gb = int(float(capacity_gb[:-2]) * 1000)
        else:
            capacity_gb = int(capacity_gb[:-2])

        SSD = SSDs()
        SSD.name = name
        SSD.m2 = False
        SSD.capacity_gb = capacity_gb
        SSD.price_in_rubles = SSD_info[1]

        db_sess.add(SSD)
    db_sess.commit()

    db_sess = db_session.create_session()
    SSDs_ = db_sess.query(SSDs).all()

    for SSD in SSDs_:
        print(SSD.name)


SSDs_info, M2_SSDs_info = get_info()

filling_db(SSDs_info, M2_SSDs_info)
