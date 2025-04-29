import requests
from bs4 import BeautifulSoup
from pprint import pprint


def get_processors_name():
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


def get_processors_info(processors):
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
                memory_type, memory_frequency = (
                    elements[18].get_text().split('(')[1].split(')'))[0].split('-')
                memory_frequency = int(memory_frequency)
                pcie_type = ' '.join(elements[19].get_text().split()[2:])
            except:
                try:
                    year = int(elements[0].get_text())
                    socket = elements[2].get_text()
                    cores = int(elements[3].get_text())
                    threads = int(elements[4].get_text())
                    processor_frequency = int(elements[5].get_text().split()[0])
                    tdp = int(elements[10].get_text().split()[0])
                    memory_type, memory_frequency = (
                        elements[17].get_text().split('(')[1].split(')'))[0].split('-')
                    memory_frequency = int(memory_frequency)
                    pcie_type = ' '.join(elements[18].get_text().split()[2:])
                except:
                    try:
                        year = int(elements[0].get_text())
                        socket = elements[2].get_text()
                        cores = int(elements[3].get_text().split()[0])
                        threads = int(elements[4].get_text())
                        processor_frequency = int(elements[5].get_text().split()[0])
                        tdp = int(elements[11].get_text().split()[0])
                        memory_type, memory_frequency = (
                            elements[18].get_text().split('(')[1].split(')'))[0].split('-')
                        memory_frequency = int(memory_frequency)
                        pcie_type = ' '.join(elements[19].get_text().split()[2:])
                    except:
                        try:
                            year = int(elements[0].get_text())
                            socket = elements[2].get_text()
                            cores = int(elements[4].get_text().split()[0])
                            threads = int(elements[5].get_text())
                            processor_frequency = int(elements[6].get_text().split()[0])
                            tdp = int(elements[11].get_text().split()[0])
                            memory_type, memory_frequency = (
                                elements[19].get_text().split('(')[1].split(')'))[0].split('-')
                            memory_frequency = int(memory_frequency)
                            pcie_type = int(elements[20].get_text().split()[2])
                        except:
                            pass
            processors_info.append((processor, year, socket, cores, threads, processor_frequency,
                                    tdp, memory_type, memory_frequency, pcie_type))
        else:
            pass
    return processors_info


processors_info = get_processors_info(get_processors_name())
print(processors_info)
