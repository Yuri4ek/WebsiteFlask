import requests
from bs4 import BeautifulSoup


def parse_cpu_info(processor, url):
    # Send HTTP request and get page content
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Dictionary to store results
    specs = {}

    # Find ranking
    a = soup.find_all('em')
    rating = int(a[1].get_text())
    cores = int(a[21].get_text().split()[0])
    threads = int(a[23].get_text())
    clock_speed = float(a[25].get_text().split()[0])
    socket = a[47].get_text()
    tdp = int(a[49].get_text().split()[0])
    memory_type = a[59].get_text()
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
    else:
        print(f'Ошибка при загрузке страницы: {response.status_code}')

for processor in processors:
    url = f"https://technical.city/en/cpu/{processor.replace(' ', '-')}"
    parse_cpu_info(processor, url)
