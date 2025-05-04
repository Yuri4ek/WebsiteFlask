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
        computer_cases_info = json.load(file)['components']['Корпус']
    return computer_cases_info


def filling_db(computer_cases_info):
    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM computer_cases")
    con.commit()
    con.close()

    db_session.global_init("../../db/components.db")

    db_sess = db_session.create_session()
    for computer_case_info in computer_cases_info:
        computerCase = ComputerCases()
        computerCase.name = computer_case_info[0]
        computerCase.price_in_rubles = computer_case_info[1]

        db_sess.add(computerCase)
    db_sess.commit()

    db_sess = db_session.create_session()
    computerCases = db_sess.query(ComputerCases).all()

    for computerCase in computerCases:
        print(computerCase.name)


computer_cases_info = get_info()

filling_db(computer_cases_info)
