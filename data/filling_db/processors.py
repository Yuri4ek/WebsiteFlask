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

            elements = soup.find_all('td', {'class': 'tdc2'})
            try:
                year = int(elements[0].get_text())
                socket = elements[2].get_text()
                cores = int(elements[4].get_text())
                threads = int(elements[5].get_text())
                processor_frequency = int(elements[6].get_text().split()[0])
                tdp = int(elements[11].get_text().split()[0])
                if tdp > 1000:
                    tdp = int(elements[12].get_text().split()[0])
                pcie_type = ' '.join(elements[19].get_text().split()[2:])
            except:
                try:
                    year = int(elements[0].get_text())
                    socket = elements[2].get_text()
                    cores = int(elements[3].get_text())
                    threads = int(elements[4].get_text())
                    processor_frequency = int(elements[5].get_text().split()[0])
                    tdp = int(elements[10].get_text().split()[0])
                    if tdp > 1000:
                        tdp = int(elements[11].get_text().split()[0])
                    pcie_type = ' '.join(elements[18].get_text().split()[2:])
                except:
                    try:
                        year = int(elements[0].get_text())
                        socket = elements[2].get_text()
                        cores = int(elements[3].get_text().split()[0])
                        threads = int(elements[4].get_text())
                        processor_frequency = int(elements[5].get_text().split()[0])
                        tdp = int(elements[11].get_text().split()[0])
                        if tdp > 1000:
                            tdp = int(elements[12].get_text().split()[0])
                        pcie_type = ' '.join(elements[19].get_text().split()[2:])
                    except:
                        try:
                            year = int(elements[0].get_text())
                            socket = elements[2].get_text()
                            cores = int(elements[4].get_text().split()[0])
                            threads = int(elements[5].get_text())
                            processor_frequency = int(elements[6].get_text().split()[0])
                            tdp = int(elements[11].get_text().split()[0])
                            if tdp > 1000:
                                tdp = int(elements[12].get_text().split()[0])
                            pcie_type = int(elements[20].get_text().split()[2])
                        except:
                            pass
            # тип памяти частота памяти
            try:
                memory = elements[17].get_text().split('(')[1].split(')')[0]
                if 'DDR' not in memory:
                    raise
            except:
                try:
                    memory = elements[18].get_text().split('(')[1].split(')')[0]
                    if 'DDR' not in memory:
                        raise
                except:
                    memory = elements[19].get_text().split('(')[1].split(')')[0]
            try:
                memory_type, memory_frequency = memory.split('-')
                memory_frequency = int(memory_frequency.split(', ')[1])
            except:
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
                        memory_type, memory_frequency = None, None

            processors_info.append((processor, year, socket, cores, threads, processor_frequency,
                                    tdp, memory_type, memory_frequency, pcie_type))
        else:
            pass
    return processors_info


def get_prices():
    # Имя JSON-файла
    json_file = "components_prices.json"

    # Открываем и читаем JSON-файл
    with open(json_file, "r", encoding="utf-8") as file:
        # Загружаем JSON в словарь
        processors_prices = json.load(file)['components']['Процессор']
    return processors_prices


def filling_db(processors_info, processors_prices):
    # берем сокеты
    with open('sockets.json', "r", encoding="utf-8") as file:
        sockets = json.load(file)

    # берем типы памяти
    with open('memory_types.json', "r", encoding="utf-8") as file:
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
        for processors_price in processors_prices:
            if current_processor[0] == processors_price[0]:
                processor.price_in_rubles = processors_price[1]
                break
        db_sess.add(processor)
    db_sess.commit()

    db_sess = db_session.create_session()
    processors = db_sess.query(Processors).all()

    for processor in processors:
        print(processor.name)


processors_info = get_info(get_names())
processors_prices = get_prices()

filling_db(processors_info, processors_prices)