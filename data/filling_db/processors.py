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


def get_info(processors):
    processors_info = []
    for processor in processors:
        processor_for_url = processor.replace(' ', '_')
        url = f'https://www.chaynikam.info/{processor_for_url}.html'  # сюда ссылку на сайт
        response = requests.get(url)

        # Проверяем успешность запроса
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            elements = soup.find_all('td')

            i = 0
            elements_len = len(elements)
            while i < elements_len:
                if 'Год выхода' in elements[i].get_text():
                    year = int(elements[i + 1].get_text())
                    i += 1
                elif 'Socket' in elements[i].get_text():
                    socket = elements[i + 1].get_text()
                    i += 1
                elif 'Количество ядер' in elements[i].get_text():
                    try:
                        cores = int(elements[i + 1].get_text())
                    except:
                        cores = int(elements[i + 1].get_text().split()[0])
                    i += 1
                elif 'Количество потоков' in elements[i].get_text():
                    threads = int(elements[i + 1].get_text())
                    i += 1
                elif 'Базовая частота' in elements[i].get_text():
                    processor_frequency = int(elements[i + 1].get_text().split()[0])
                    i += 1
                elif 'TDP' in elements[i].get_text():
                    try:
                        tdp = int(elements[i + 1].get_text().split()[0])
                    except:
                        try:
                            tdp = int(elements[i + 1].get_text().split()[0].split('-')[1])
                        except:
                            tdp = None
                    i += 1
                elif 'Контроллер PCIe' in elements[i].get_text():
                    pcie_type = int(elements[i + 1].get_text().split()[2].split('.')[0])
                    i += 1
                elif 'Контроллер оперативной памяти' in elements[i].get_text():
                    memory = elements[i + 1].get_text().split('(')[1].split(')')[0]
                    try:
                        memory1, memory2 = memory.split(', ')
                        memory_type, memory_frequency = memory1.split('-')
                        memory_frequency = int(memory_frequency)
                        processors_info.append(
                            (processor, year, socket, cores, threads, processor_frequency,
                             tdp, memory_type, memory_frequency, pcie_type))

                        memory_type, memory_frequency = memory2.split('-')
                        memory_frequency = int(memory_frequency)
                    except:
                        try:
                            memory_type, memory_frequency = memory.split('-')
                            memory_frequency = int(memory_frequency)
                        except:
                            try:
                                memory_frequency = int(memory_frequency.split(', ')[1])
                            except:
                                memory_frequency = None
                    i += 1
                i += 1

            processors_info.append((processor, year, socket, cores, threads, processor_frequency,
                                    tdp, memory_type, memory_frequency, pcie_type))
        else:
            pass
    return processors_info


def get_prices():
    # Имя JSON-файла
    json_file = "data_files/components_prices.json"

    # Открываем и читаем JSON-файл
    with open(json_file, "r", encoding="utf-8") as file:
        # Загружаем JSON в словарь
        processors_prices = json.load(file)['components']['Процессор']
    return processors_prices


def filling_db(processors_info):
    # берем сокеты
    with open('data_files/sockets.json', "r", encoding="utf-8") as file:
        sockets = json.load(file)

    # берем типы памяти
    with open('data_files/memory_types.json', "r", encoding="utf-8") as file:
        memory_types = json.load(file)

    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM processors")
    con.commit()
    con.close()

    db_session.global_init("../../db/components.db")

    db_sess = db_session.create_session()
    for current_processor in processors_info:
        processor = Processors()
        processor.name = current_processor[0]
        processor.release_year = current_processor[1]
        try:
            processor.socket_id = sockets[current_processor[2]]
        except:
            processor.socket_id = None
        processor.cores = current_processor[3]
        processor.threads = current_processor[4]
        processor.processor_frequency = current_processor[5]
        processor.tdp = current_processor[6]
        try:
            processor.memory_type_id = memory_types[current_processor[7]]
        except:
            processor.memory_type_id = None
        processor.memory_frequency = current_processor[8]
        processor.pcie_type = current_processor[9]
        db_sess.add(processor)
    db_sess.commit()

    db_sess = db_session.create_session()
    processors = db_sess.query(Processors).all()

    for processor in processors:
        print(processor.name)


def filling_db_prices(processors_price):
    db_session.global_init("../../db/components.db")
    db_sess = db_session.create_session()

    # берем данные процессоров
    processors = db_sess.query(Processors).all()

    # удаляем старые данные
    con = sqlite3.connect("../../db/components.db")
    cur = con.cursor()
    cur.execute("DELETE FROM processors")
    con.commit()
    con.close()

    # добавляем цены
    for current_processor in processors:
        processor = Processors()
        processor.name = current_processor.name
        processor.release_year = current_processor.release_year
        processor.socket_id = current_processor.socket_id
        processor.cores = current_processor.cores
        processor.threads = current_processor.threads
        processor.processor_frequency = current_processor.processor_frequency
        processor.tdp = current_processor.tdp
        processor.memory_type_id = current_processor.memory_type_id
        processor.memory_frequency = current_processor.memory_frequency
        processor.pcie_type = current_processor.pcie_type
        price_flag = True
        for processor_price in processors_price:
            if current_processor.name.lower() in processor_price[0].lower():
                processor.price_in_rubles = processor_price[1]
                price_flag = False
                break
        if price_flag:
            processor.price_in_rubles = current_processor.price_in_rubles
        db_sess.add(processor)
    db_sess.commit()

    processors = db_sess.query(Processors).all()

    for processor in processors:
        print(processor.name)


# данные (раз в месяц обновлять)
processors_info = get_info(get_names())
filling_db(processors_info)

# цены (раз в день обновлять)
processors_price = get_prices()
filling_db_prices(processors_price)
