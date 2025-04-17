from flask import make_response, request, render_template
import json
from data.db_imports import *


# Установка cookie с JSON
def set_cookies():
    # данные для конфигурации
    configuration_data = {'computer_cases': 'не выбран',
                          'cooling_systems': 'не выбран',
                          'memory_types': 'не выбран',
                          'motherboards': 'не выбран',
                          'power_supplies': 'не выбран',
                          'processors': 'не выбран',
                          'ram_modules': 'не выбран',
                          'sockets': 'не выбран',
                          'storage_devices': 'не выбран',
                          'videocards': 'не выбран'}

    # данные для фильтров
    filter_data = {'socket': None,
                   'memory_type': None,
                   'm2_support': None,
                   'processor_tdp': None,
                   'videocard_tdp': None}

    # Преобразуем JSON в строку
    json_configuration_data = json.dumps(configuration_data)
    json_filter_data = json.dumps(filter_data)

    resp = make_response(render_template('main.html', selected_component=configuration_data))
    resp.set_cookie('configuration_data', json_configuration_data, max_age=60 * 60)
    resp.set_cookie('filter_data', json_filter_data, max_age=60 * 60)
    return resp


# Чтение и вывод JSON из cookie
def get_cookie(cookie_name):
    json_data = request.cookies.get(cookie_name)
    if json_data:
        # Преобразуем строку обратно в JSON
        data = json.loads(json_data)
        return data
    return None


# Изменение JSON в cookie
def update_cookie(cookie_name, key, value):
    data = get_cookie(cookie_name)
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


db_session.global_init("db/components.db")


def update_cookies(component_type, component_name):
    configuration_data = get_cookie('configuration_data')
    filter_data = get_cookie('filter_data')

    db_sess = db_session.create_session()
    component = db_sess.query(components_types[component_type]).filter(
        components_types[component_type].name == component_name).first()

    configuration_data[component_type] = component_name
    if component_type == 'cooling_systems' or component_type == 'processors':
        filter_data['socket'] = component.socket_id
        filter_data['processor_tdp'] = component.tdp
    elif component_type == 'motherboards':
        filter_data['socket'] = component.socket_id
        filter_data['memory_type'] = component.memory_type_id
        filter_data['m2_support'] = component.m2_support
    elif component_type == 'videocards':
        filter_data['videocard_tdp'] = component.tdp

    updated_configuration_json = json.dumps(configuration_data)
    updated_filter_json = json.dumps(filter_data)
    resp = make_response(render_template('main.html',
                                         selected_component=updated_configuration_json))
    resp.set_cookie('configuration_data', updated_configuration_json, max_age=60 * 60)
    resp.set_cookie('filter_data', updated_filter_json, max_age=60 * 60)
    return resp
