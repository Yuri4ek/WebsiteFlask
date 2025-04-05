from flask import make_response, request, render_template
import json


# Установка cookie с JSON
def set_cookie():
    # Пример данных в формате JSON
    data = {'computer_cases': 'не выбран',
            'cooling_systems': 'не выбран',
            'memory_types': 'не выбран',
            'motherboards': 'не выбран',
            'power_supplies': 'не выбран',
            'processors': 'не выбран',
            'ram_modules': 'не выбран',
            'sockets': 'не выбран',
            'storage_devices': 'не выбран',
            'videocards': 'не выбран'}

    # Преобразуем JSON в строку
    json_data = json.dumps(data)
    resp = make_response(render_template('main.html', selected_component=data))
    resp.set_cookie('configuration_data', json_data, max_age=60 * 60)
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
        data[key] = value

        # Преобразуем обратно в строку
        updated_json = json.dumps(data)
        resp = make_response(render_template('main.html',
                             selected_component=data))
        resp.set_cookie('configuration_data', updated_json, max_age=60 * 60)
        return resp
    return "Cookie не найдено!"
