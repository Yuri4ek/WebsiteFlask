import json
import sqlite3
from data.db_imports import *
from pprint import pprint


def get_info():
    # Имя JSON-файла
    json_file = "data_files/components_prices.json"

    # Открываем и читаем JSON-файл
    with open(json_file, "r", encoding="utf-8") as file:
        # Загружаем JSON в словарь
        HDDs_info = json.load(file)['components']['Жёсткий диск']
    return HDDs_info


def filling_db(HDDs_info):
    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM HDDs")
    con.commit()
    con.close()

    db_session.global_init("../../db/components.db")

    db_sess = db_session.create_session()
    for HDD_info in HDDs_info:
        capacity_gb, type, *name = HDD_info[0].split()
        name = f"{capacity_gb} {' '.join(name)}"
        if capacity_gb[-2:] == "Tb":
            capacity_gb = int(capacity_gb[:-2]) * 1000
        else:
            capacity_gb = int(capacity_gb[:-2])

        HDD = HDDs()
        HDD.name = name
        HDD.capacity_gb = capacity_gb
        HDD.price_in_rubles = HDD_info[1]

        db_sess.add(HDD)
    db_sess.commit()

    db_sess = db_session.create_session()
    HDDs_ = db_sess.query(HDDs).all()

    for HDD in HDDs_:
        print(HDD.name)


HDDs_info = get_info()

filling_db(HDDs_info)
