from flask import make_response, request, render_template
import json
from data.db_imports import *

# данные для конфигурации
configuration_data = {'computer_cases': ['не выбран'],
                      'cooling_systems': ['не выбран'],
                      'motherboards': ['не выбран'],
                      'power_supplies': ['не выбран'],
                      'processors': ['не выбран'],
                      'ram_modules': ['не выбран'],
                      'storage_devices': ['не выбран'],
                      'videocards': ['не выбран']}


# Установка cookie с JSON
def set_cookie():
    # Преобразуем JSON в строку
    json_configuration_data = json.dumps(configuration_data)

    resp = make_response(
        render_template('main.html', selected_component=configuration_data))
    resp.set_cookie('configuration_data', json_configuration_data,
                    max_age=60 * 60)
    return resp


def clear_cookie():
    # Преобразуем JSON в строку
    json_configuration_data = json.dumps(configuration_data)

    resp = make_response(
        render_template('main.html', selected_component=configuration_data))

    # добавляем удаленные cookie
    resp.set_cookie('configuration_data', json_configuration_data,
                    max_age=60 * 60)
    return resp


# Чтение и вывод JSON из cookie
def get_cookie():
    json_data = request.cookies.get('configuration_data')
    if json_data:
        # Преобразуем строку обратно в JSON
        data = json.loads(json_data)
        return data
    return None


# Изменение JSON в cookie
def update_cookie(key, value):
    data = get_cookie()
    if data:
        # Изменяем данные
        if isinstance(value[0], list):
            new_value = []
            for i in range(len(value[0])):
                if value[0][i] == value[1][i]:
                    new_value.append(value[0][i])
                else:
                    new_value.append((value[0][i], value[1][i]))
            data[key] = new_value
        else:
            data[key] = value

        # Преобразуем обратно в строку
        updated_json = json.dumps(data)
        resp = make_response(render_template('main.html',
                                             selected_component=data))
        resp.set_cookie('configuration_data', updated_json, max_age=60 * 60)
        return resp
    return "Cookie не найдено!"
