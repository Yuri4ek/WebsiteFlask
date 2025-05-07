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
        rams_info = json.load(file)['components']['Оперативная память']
    return rams_info


def filling_db(rams_info):
    # берем типы памяти
    with open('data_files/memory_types.json', "r", encoding="utf-8") as file:
        memory_types = json.load(file)

    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM ram_modules")
    con.commit()
    con.close()

    db_session.global_init("../../db/components.db")

    db_sess = db_session.create_session()
    for ram_info in rams_info:
        capacity_gb, memory_type, frequency, *other = ram_info[0].split()
        capacity_gb = int(capacity_gb[:-2])
        if memory_type == 'DDR-II':
            continue
        elif memory_type == 'DDR-III':
            memory_type = 'DDR3'
        memory_type_id = memory_types[memory_type]
        frequency = int(frequency[:-3])

        ramModule = RamModules()
        ramModule.name = ram_info[0]
        ramModule.capacity_gb = capacity_gb
        ramModule.frequency = frequency
        ramModule.memory_type_id = memory_type_id
        ramModule.price_in_rubles = ram_info[1]

        db_sess.add(ramModule)
    db_sess.commit()

    db_sess = db_session.create_session()
    ramModules = db_sess.query(RamModules).all()

    for ramModule in ramModules:
        print(ramModule.name)


rams_info = get_info()

filling_db(rams_info)
