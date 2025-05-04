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
        PSUs_info = json.load(file)['components']['Блок питания']
    return PSUs_info


def filling_db(PSUs_info):
    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM power_supplies")
    con.commit()
    con.close()

    db_session.global_init("../../db/components.db")

    db_sess = db_session.create_session()
    for PSU_info in PSUs_info:
        power, *other = PSU_info[0].split()
        power = int(power[:-1])

        PSU = PowerSupplies()
        PSU.name = PSU_info[0]
        PSU.power = power
        PSU.price_in_rubles = PSU_info[1]

        db_sess.add(PSU)
    db_sess.commit()

    db_sess = db_session.create_session()
    PSUs = db_sess.query(PowerSupplies).all()

    for PSU in PSUs:
        print(PSU.name)


PSUs_info = get_info()

filling_db(PSUs_info)
