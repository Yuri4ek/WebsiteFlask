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
