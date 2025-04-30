import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from data.db_imports import *
from pprint import pprint


def get_names():
    processors = []
    for i in range(1, 19):
        url = f'https://technical.city/en/cpu/rating?&pg={i}'  # сюда ссылку на сайт
        response = requests.get(url)

        # Проверяем успешность запроса
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Найдем таблицу с рейтингом процессоров
            table = soup.find('table')

            # Извлекаем заголовки таблицы
            headers = [header.text for header in table.find_all('th')]
            # Извлекаем строки таблицы
            for row in table.find_all('tr')[1:]:  # Пропускаем заголовок
                cols = row.find_all('td')
                data = [col.text.strip() for col in cols]
                try:
                    if int(data[5]) > 2018 and data[2] == 'desktop':
                        processors.append(data[1])
                except:
                    pass
        else:
            print(f'Ошибка при загрузке страницы: {response.status_code}')
    return processors


def get_memory_types(processors):
    memory_types = []
    for processor in processors:
        processor_for_url = processor.replace(' ', '_')
        url = f'https://www.chaynikam.info/{processor_for_url}.html'  # сюда ссылку на сайт
        response = requests.get(url)

        # Проверяем успешность запроса
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            elements = soup.find_all('td', {'class': 'tdc2'})
            try:
                memory_type, memory_frequency = (
                    elements[17].get_text().split('(')[1].split(')'))[0].split('-')
            except:
                try:
                    memory_type, memory_frequency = (
                        elements[18].get_text().split('(')[1].split(')'))[0].split('-')
                except:
                    try:
                        memory_type, memory_frequency = (
                            elements[19].get_text().split('(')[1].split(')'))[0].split('-')
                    except:
                        pass
            if memory_type not in memory_types:
                memory_types.append(memory_type)
        else:
            pass
    return memory_types


def make_json(memory_types):
    memory_types_json = {}

    i = 1
    for memory_type in memory_types:
        memory_types_json[memory_type] = i
        i += 1

    # Преобразование словаря в JSON
    json_data = json.dumps(memory_types_json, indent=4, ensure_ascii=False)

    # Запись JSON в файл
    with open("memory_types.json", "w", encoding="utf-8") as file:
        file.write(json_data)


def filling_db(current_memory_types):
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


memory_types = get_memory_types(get_names())

filling_db(memory_types)
make_json(memory_types)
