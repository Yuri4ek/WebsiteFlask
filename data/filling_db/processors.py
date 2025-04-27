import requests
from bs4 import BeautifulSoup
from pprint import pprint


def parse_cpu_info(processor, url):
    # Send HTTP request and get page content
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)

    # берем html
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find ranking
    a = soup.find_all('em')
    print(a)
    try:
        rating = int(a[0].get_text())
    except:
        rating = int(a[1].get_text())
    try:
        cores = int(a[20].get_text().split()[0])
    except:
        cores = int(a[21].get_text().split()[0])
    try:
        threads = int(a[22].get_text())
    except:
        threads = int(a[23].get_text())
    try:
        clock_speed = float(a[24].get_text().split()[0])
    except:
        clock_speed = float(a[25].get_text().split()[0])
    try:
        socket = a[44].get_text()
    except:
        socket = a[47].get_text()
    try:
        tdp = int(a[46].get_text().split()[0])
    except:
        tdp = int(a[49].get_text().split()[0])
    try:
        memory_type = a[56].get_text()
    except:
        memory_type = a[59].get_text()
    try:
        pcie_type = float(a[60].get_text())
    except:
        pcie_type = float(a[63].get_text())

    print(processor, rating, cores, threads, clock_speed, socket, tdp, memory_type, pcie_type)


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
                if int(data[5]) > 2018 or data[2] == 'desktop':
                    processors.append(data[1])
            except:
                pass
        break
    else:
        print(f'Ошибка при загрузке страницы: {response.status_code}')

for processor in processors:
    print(processor)
    print(f"https://technical.city/en/cpu/{processor.replace(' ', '-')}")
    url = f"https://technical.city/en/cpu/{processor.replace(' ', '-')}"
    parse_cpu_info(processor, url)
