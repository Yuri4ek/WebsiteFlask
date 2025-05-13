import json


def get_sockets():
    # берем сокеты
    with open('data/filling_db/data_files/sockets.json', "r", encoding="utf-8") as file:
        sockets = json.load(file)
    sockets = list(sockets.keys())

    return sockets


def get_memory_types():
    # берем типы памяти
    with open('data/filling_db/data_files/memory_types.json', "r", encoding="utf-8") as file:
        memory_types = json.load(file)
    memory_types = list(memory_types.keys())

    return memory_types


def get_memory_slots(RAM_name):
    print(RAM_name)
    if "KIT" in RAM_name:
        try:
            return int(RAM_name.split('(')[-1].split('x')[0])
        except:
            return int(RAM_name.split('(')[-2].split('x')[0])
    return 1


def get_processor_line(processor_name):
    if "Ryzen" in processor_name and "Threadripper" not in processor_name:
        processor_line = int(processor_name.split()[1])
    elif "Core Ultra" in processor_name:
        processor_line = int(processor_name.split()[2])
    elif "Core" in processor_name:
        processor_line = int(processor_name.split()[1][1])
    else:
        processor_line = None
    return processor_line


def get_price_limit(filters):
    filters_list = filters.split(',')
    if "price_from" in filters and "price_to" in filters:
        price_from = int(filters_list[0].split(':')[1])
        price_to = int(filters_list[1].split(':')[1])
    elif "price_from" in filters:
        price_from = int(filters_list[0].split(':')[1])
        price_to = 1000000
    elif "price_to" in filters:
        price_from = 0
        price_to = int(filters_list[0].split(':')[1])
    else:
        price_from = 0
        price_to = 1000000
    return price_from, price_to
