from flask import render_template

import data.configuration
import data.db_session
import cookie_functions
import data.forum
import data.user
import db_methods
from data.computer_cases import ComputerCases
from data.air_coolers import AirCoolers
from data.water_coolers import WaterCoolers
from data.motherboards import MotherBoards
from data.power_supplies import PowerSupplies
from data.processors import Processors
from data.ram_modules import RamModules
from data.HDDs import HDDs
from data.SSDs import SSDs
from data.videocards import Videocards
from sqlalchemy import and_, or_


def computer_cases(price_from, price_to, people_request):
    # все компоненты
    db_sess = data.db_session.create_session()
    components = db_sess.query(ComputerCases).filter(
        ComputerCases.price_in_rubles >= price_from,
        ComputerCases.price_in_rubles <= price_to).all()

    displaying_components = []
    # делаем корпуса читабельнее
    for component in components:
        id, name, price_in_rubles = component.get()

        if people_request:
            if set(people_request.lower()) - set(name.lower()) == set():
                displaying_components.append((name,
                                              f'Цена: {price_in_rubles} Рублей'))
        else:
            displaying_components.append((name,
                                          f'Цена: {price_in_rubles} Рублей'))

    return render_template('search_components.html',
                           component_type='computer_cases', components=displaying_components,
                           component_image='/static/images/computer_case.webp')


def air_coolers(price_from, price_to, people_request):
    current_configuration_data = cookie_functions.get_cookie()
    # все компоненты
    db_sess = data.db_session.create_session()
    if current_configuration_data['processors'] != ['не выбран']:
        tdp = current_configuration_data['processors'][6]
        components = db_sess.query(AirCoolers).filter(AirCoolers.tdp >= tdp,
                                                      AirCoolers.price_in_rubles >= price_from,
                                                      AirCoolers.price_in_rubles <= price_to).all()
    else:
        components = db_sess.query(AirCoolers).filter(
            AirCoolers.price_in_rubles >= price_from,
            AirCoolers.price_in_rubles <= price_to).all()

    displaying_components = []
    # делаем системы охлаждения читабельнее
    for component in components:
        id, name, tdp, price_in_rubles = component.get()

        if people_request:
            if set(people_request.lower()) - set(name.lower()) == set():
                displaying_components.append((name,
                                              f'Цена: {price_in_rubles} Рублей',
                                              f'Отвод тепла: {tdp} Ватт'))
        else:
            displaying_components.append((name,
                                          f'Цена: {price_in_rubles} Рублей',
                                          f'Отвод тепла: {tdp} Ватт'))

    return render_template('search_components.html',
                           component_type='air_coolers', components=displaying_components,
                           component_image='/static/images/air_cooler.webp')


def water_coolers(price_from, price_to, people_request):
    current_configuration_data = cookie_functions.get_cookie()
    # все компоненты
    db_sess = data.db_session.create_session()
    if current_configuration_data['processors'] != ['не выбран']:
        tdp = current_configuration_data['processors'][6]
        components = db_sess.query(WaterCoolers).filter(WaterCoolers.tdp >= tdp,
                                                        WaterCoolers.price_in_rubles >= price_from,
                                                        WaterCoolers.price_in_rubles <= price_to).all()
    else:
        components = db_sess.query(WaterCoolers).filter(
            WaterCoolers.price_in_rubles >= price_from,
            WaterCoolers.price_in_rubles <= price_to).all()

    displaying_components = []
    # делаем системы охлаждения читабельнее
    for component in components:
        id, name, tdp, price_in_rubles = component.get()

        if people_request:
            if set(people_request.lower()) - set(name.lower()) == set():
                displaying_components.append((name,
                                              f'Цена: {price_in_rubles} Рублей',
                                              f'Отвод тепла: {tdp} Ватт'))
        else:
            displaying_components.append((name,
                                          f'Цена: {price_in_rubles} Рублей',
                                          f'Отвод тепла: {tdp} Ватт'))

    return render_template('search_components.html',
                           component_type='water_coolers', components=displaying_components,
                           component_image='/static/images/water_cooler.webp')


def motherboards(price_from, price_to, people_request):
    # достаем сокеты для материнских плат
    current_sockets = db_methods.get_sockets()

    # достаем типы памяти для материнских плат
    current_memory_types = db_methods.get_memory_types()

    current_configuration_data = cookie_functions.get_cookie()
    # все компоненты
    db_sess = data.db_session.create_session()
    if current_configuration_data['processors'] != ['не выбран']:
        socket_id = current_configuration_data['processors'][2]
        memory_type_id = current_configuration_data['processors'][7]
        if isinstance(memory_type_id, list):
            components = db_sess.query(MotherBoards).filter(
                and_(
                    or_(MotherBoards.memory_type_id == memory_type_id[0],
                        MotherBoards.memory_type_id == memory_type_id[1]),
                    MotherBoards.socket_id == socket_id,
                    MotherBoards.price_in_rubles != 0,
                    MotherBoards.price_in_rubles >= price_from,
                    MotherBoards.price_in_rubles <= price_to
                )
            ).all()

            if len(components) == 0:
                components = db_sess.query(MotherBoards).filter(
                    and_(
                        or_(MotherBoards.memory_type_id == memory_type_id[0],
                            MotherBoards.memory_type_id == memory_type_id[1]),
                        MotherBoards.socket_id == socket_id
                    )
                ).all()
        else:
            components = db_sess.query(MotherBoards).filter(
                MotherBoards.socket_id == socket_id,
                MotherBoards.memory_type_id == memory_type_id,
                MotherBoards.price_in_rubles != 0,
                MotherBoards.price_in_rubles >= price_from,
                MotherBoards.price_in_rubles <= price_to
            ).all()

            if len(components) == 0:
                components = db_sess.query(MotherBoards).filter(
                    MotherBoards.socket_id == socket_id,
                    MotherBoards.memory_type_id == memory_type_id
                ).all()
    elif current_configuration_data['ram_modules'] != ['не выбран']:
        RAM_name = current_configuration_data['ram_modules'][0]
        memory_slots = db_methods.get_memory_slots(RAM_name)
        memory_type_id = current_configuration_data['ram_modules'][3]
        components = db_sess.query(MotherBoards).filter(
            MotherBoards.memory_type_id == memory_type_id,
            MotherBoards.memory_slots >= memory_slots,
            MotherBoards.price_in_rubles != 0,
            MotherBoards.price_in_rubles >= price_from,
            MotherBoards.price_in_rubles <= price_to).all()

        if len(components) == 0:
            components = db_sess.query(MotherBoards).filter(
                MotherBoards.memory_type_id == memory_type_id,
                MotherBoards.memory_slots >= memory_slots).all()
    else:
        components = db_sess.query(MotherBoards).filter(MotherBoards.price_in_rubles != 0,
                                                        MotherBoards.price_in_rubles >= price_from,
                                                        MotherBoards.price_in_rubles <= price_to).all()

    displaying_components = []
    # делаем материнские платы читабельнее
    for component in components:
        id, name, socket_id, chipset, memory_type_id, \
            memory_slots, memory_max, m2_quantity, pcie_type, \
            form_factor, price_in_rubles = component.get()
        socket = current_sockets[socket_id - 1] if socket_id else 'Неизвестно'
        memory_type = current_memory_types[memory_type_id - 1] if memory_type_id else 'Неизвестно'

        if people_request:
            if set(people_request.lower()) - set(name.lower()) == set():
                displaying_components.append((name,
                                              f'Цена: {price_in_rubles} Рублей' if price_in_rubles
                                              else 'Цена неизвестна',
                                              f'Сокет: {socket}',
                                              f'Тип памяти: {memory_type}',
                                              f'Кол-во слотов для ОЗУ: {memory_slots}',
                                              f'Максимальный объём памяти: {memory_max} Гигабайт',
                                              f'Кол-во слотов m2: {m2_quantity}',
                                              f'Тип pcie: {pcie_type}',
                                              f'Форм-фактор: {form_factor}'))
        else:
            displaying_components.append((name,
                                          f'Цена: {price_in_rubles} Рублей' if price_in_rubles
                                          else 'Цена неизвестна',
                                          f'Сокет: {socket}',
                                          f'Тип памяти: {memory_type}',
                                          f'Кол-во слотов для ОЗУ: {memory_slots}',
                                          f'Максимальный объём памяти: {memory_max} Гигабайт',
                                          f'Кол-во слотов m2: {m2_quantity}',
                                          f'Тип pcie: {pcie_type}',
                                          f'Форм-фактор: {form_factor}'))

    return render_template('search_components.html',
                           component_type='motherboards',
                           components=displaying_components,
                           component_image='/static/images/motherboard.webp',
                           sockets=current_sockets, memory_types=current_memory_types)


def motherboards_with_filter(price_from, price_to, filter_type, filter_value):
    # достаем сокеты для материнских плат
    current_sockets = db_methods.get_sockets()

    # достаем типы памяти для материнских плат
    current_memory_types = db_methods.get_memory_types()

    # все компоненты
    db_sess = data.db_session.create_session()
    if filter_type == "socket":
        socket_id = current_sockets.index(filter_value) + 1
        components = db_sess.query(MotherBoards).filter(
            MotherBoards.socket_id == socket_id,
            MotherBoards.price_in_rubles != 0,
            MotherBoards.price_in_rubles >= price_from,
            MotherBoards.price_in_rubles <= price_to
        ).all()

        if len(components) == 0:
            components = db_sess.query(MotherBoards).filter(
                MotherBoards.socket_id == socket_id,
            ).all()
    elif filter_type == "memory_type":
        memory_type_id = current_memory_types.index(filter_value) + 1
        components = db_sess.query(MotherBoards).filter(
            MotherBoards.memory_type_id == memory_type_id,
            MotherBoards.price_in_rubles != 0,
            MotherBoards.price_in_rubles >= price_from,
            MotherBoards.price_in_rubles <= price_to).all()

        if len(components) == 0:
            components = db_sess.query(MotherBoards).filter(
                MotherBoards.memory_type_id == memory_type_id).all()
    elif filter_type == "m2_support":
        if filter_value == "True":
            components = db_sess.query(MotherBoards).filter(
                MotherBoards.m2_quantity > 0,
                MotherBoards.price_in_rubles != 0,
                MotherBoards.price_in_rubles >= price_from,
                MotherBoards.price_in_rubles <= price_to).all()

            if len(components) == 0:
                components = db_sess.query(MotherBoards).filter(
                    MotherBoards.m2_quantity > 0).all()
        else:
            components = db_sess.query(MotherBoards).filter(
                MotherBoards.m2_quantity == 0,
                MotherBoards.price_in_rubles != 0,
                MotherBoards.price_in_rubles >= price_from,
                MotherBoards.price_in_rubles <= price_to).all()

            if len(components) == 0:
                components = db_sess.query(MotherBoards).filter(
                    MotherBoards.m2_quantity == 0).all()

    displaying_components = []
    # делаем материнские платы читабельнее
    for component in components:
        id, name, socket_id, chipset, memory_type_id, \
            memory_slots, memory_max, m2_quantity, pcie_type, \
            form_factor, price_in_rubles = component.get()
        socket = current_sockets[socket_id - 1] if socket_id else 'Неизвестно'
        memory_type = current_memory_types[memory_type_id - 1] if memory_type_id else 'Неизвестно'

        displaying_components.append((name,
                                      f'Цена: {price_in_rubles} Рублей' if price_in_rubles
                                      else 'Цена неизвестна',
                                      f'Сокет: {socket}',
                                      f'Тип памяти: {memory_type}',
                                      f'Кол-во слотов для ОЗУ: {memory_slots}',
                                      f'Максимальный объём памяти: {memory_max} Гигабайт',
                                      f'Кол-во слотов m2: {m2_quantity}',
                                      f'Тип pcie: {pcie_type}',
                                      f'Форм-фактор: {form_factor}'))

    return render_template('search_components.html',
                           component_type='motherboards',
                           components=displaying_components,
                           component_image='/static/images/motherboard.webp',
                           sockets=current_sockets, memory_types=current_memory_types)


def power_supplies(price_from, price_to, people_request):
    current_configuration_data = cookie_functions.get_cookie()
    # все компоненты
    db_sess = data.db_session.create_session()
    tdp = 0
    if current_configuration_data['videocards'] != ['не выбран']:
        tdp += current_configuration_data['videocards'][1] * 1.6
    elif current_configuration_data['processors'] != ['не выбран']:
        tdp += current_configuration_data['processors'][6] * 2
    tdp += 40
    components = db_sess.query(PowerSupplies).filter(PowerSupplies.power >= tdp,
                                                     PowerSupplies.price_in_rubles >= price_from,
                                                     PowerSupplies.price_in_rubles <= price_to).all()

    if len(components) == 0:
        components = db_sess.query(PowerSupplies).filter(PowerSupplies.power >= tdp).all()

    displaying_components = []
    # делаем БП читабельнее
    for component in components:
        id, name, power, price_in_rubles = component.get()

        if people_request:
            if set(people_request.lower()) - set(name.lower()) == set():
                displaying_components.append((name,
                                              f'Цена: {price_in_rubles} Рублей',
                                              f'Мощность: {power} Ватт'))
        else:
            displaying_components.append((name,
                                          f'Цена: {price_in_rubles} Рублей',
                                          f'Мощность: {power} Ватт'))

    return render_template('search_components.html',
                           component_type='power_supplies', components=displaying_components,
                           component_image='/static/images/power_supplie.webp')


def processors(price_from, price_to, people_request):
    # достаем сокеты для процессоров
    current_sockets = db_methods.get_sockets()

    # достаем типы памяти для процессоров
    current_memory_types = db_methods.get_memory_types()

    current_configuration_data = cookie_functions.get_cookie()
    # все компоненты
    db_sess = data.db_session.create_session()
    if current_configuration_data['motherboards'] != ['не выбран']:
        socket_id = current_configuration_data['motherboards'][1]
        memory_type_id = current_configuration_data['motherboards'][3]
        components = db_sess.query(Processors).filter(
            Processors.socket_id == socket_id,
            Processors.memory_type_id == memory_type_id,
            Processors.price_in_rubles != 0,
            Processors.price_in_rubles >= price_from,
            Processors.price_in_rubles <= price_to
        ).all()

        if len(components) == 0:
            components = db_sess.query(Processors).filter(
                Processors.socket_id == socket_id,
                Processors.memory_type_id == memory_type_id
            ).all()
    elif current_configuration_data['ram_modules'] != ['не выбран']:
        memory_type_id = current_configuration_data['ram_modules'][3]
        components = db_sess.query(Processors).filter(
            Processors.memory_type_id == memory_type_id, Processors.price_in_rubles != 0,
            Processors.price_in_rubles >= price_from,
            Processors.price_in_rubles <= price_to).all()

        if len(components) == 0:
            components = db_sess.query(Processors).filter(
                Processors.memory_type_id == memory_type_id).all()
    elif current_configuration_data['cooling_systems'] != ['не выбран']:
        tdp = current_configuration_data['cooling_systems'][1]
        components = db_sess.query(Processors).filter(
            Processors.tdp <= tdp,
            Processors.price_in_rubles != 0
        ).all()

        if len(components) == 0:
            components = db_sess.query(Processors).filter(
                Processors.tdp <= tdp
            ).all()
    elif current_configuration_data['power_supplies'] != ['не выбран']:
        power = current_configuration_data['power_supplies'][1]
        max_processor_tdp = power // 2.5
        components = db_sess.query(Processors).filter(
            Processors.tdp <= max_processor_tdp,
            Processors.price_in_rubles != 0,
            Processors.price_in_rubles >= price_from,
            Processors.price_in_rubles <= price_to
        ).all()

        if len(components) == 0:
            components = db_sess.query(Processors).filter(
                Processors.tdp <= max_processor_tdp
            ).all()
    else:
        components = db_sess.query(Processors).filter(Processors.price_in_rubles != 0,
                                                      Processors.price_in_rubles >= price_from,
                                                      Processors.price_in_rubles <= price_to).all()

    displaying_components = []
    # делаем процессоры читабельнее
    for component in components:
        id, name, release_year, socket_id, cores, threads, processor_frequency, tdp, \
            memory_type_id, memory_frequency, pcie_type, price_in_rubles = component.get()
        socket = current_sockets[int(socket_id) - 1] if socket_id else 'Неизвестно'
        memory_type = current_memory_types[
            int(memory_type_id) - 1] if memory_type_id else 'Неизвестно'

        if people_request:
            if set(people_request.lower()) - set(name.lower()) == set():
                displaying_components.append((name,
                                              f'Цена: {price_in_rubles} Рублей' if price_in_rubles
                                              else 'Цена неизвестна',
                                              f'Год выпуска: {release_year}',
                                              f'Сокет: {socket}',
                                              f'Ядра / Потоки: {cores} / {threads}',
                                              f'Частота процессора: {processor_frequency} Мегагерц',
                                              f'Тип памяти: {memory_type}',
                                              f'Максимальная частота памяти: {memory_frequency} Мегагерц',
                                              f'Тип pcie: {pcie_type}',
                                              f'Потребление: {tdp} Ватт'))
        else:
            displaying_components.append((name,
                                          f'Цена: {price_in_rubles} Рублей' if price_in_rubles
                                          else 'Цена неизвестна',
                                          f'Год выпуска: {release_year}',
                                          f'Сокет: {socket}',
                                          f'Ядра / Потоки: {cores} / {threads}',
                                          f'Частота процессора: {processor_frequency} Мегагерц',
                                          f'Тип памяти: {memory_type}',
                                          f'Максимальная частота памяти: {memory_frequency} Мегагерц',
                                          f'Тип pcie: {pcie_type}',
                                          f'Потребление: {tdp} Ватт'))

    return render_template('search_components.html',
                           component_type='processors', components=displaying_components,
                           component_image='/static/images/processor.webp',
                           sockets=current_sockets, memory_types=current_memory_types)


def processors_with_filter(price_from, price_to, filter_type, filter_value):
    # достаем сокеты для процессоров
    current_sockets = db_methods.get_sockets()

    # достаем типы памяти для процессоров
    current_memory_types = db_methods.get_memory_types()

    # все компоненты
    db_sess = data.db_session.create_session()
    if filter_type == "socket":
        socket_id = current_sockets.index(filter_value) + 1
        components = db_sess.query(Processors).filter(
            Processors.socket_id == socket_id,
            Processors.price_in_rubles != 0,
            Processors.price_in_rubles >= price_from,
            Processors.price_in_rubles <= price_to
        ).all()

        if len(components) == 0:
            components = db_sess.query(Processors).filter(
                Processors.socket_id == socket_id,
            ).all()
    elif filter_type == "memory_type":
        memory_type_id = current_memory_types.index(filter_value) + 1
        components = db_sess.query(Processors).filter(
            Processors.memory_type_id == memory_type_id,
            Processors.price_in_rubles != 0,
            Processors.price_in_rubles >= price_from,
            Processors.price_in_rubles <= price_to).all()

        if len(components) == 0:
            components = db_sess.query(Processors).filter(
                Processors.memory_type_id == memory_type_id).all()

    displaying_components = []
    # делаем процессоры читабельнее
    for component in components:
        id, name, release_year, socket_id, cores, threads, processor_frequency, tdp, \
            memory_type_id, memory_frequency, pcie_type, price_in_rubles = component.get()
        socket = current_sockets[int(socket_id) - 1] if socket_id else 'Неизвестно'
        memory_type = current_memory_types[
            int(memory_type_id) - 1] if memory_type_id else 'Неизвестно'

        displaying_components.append((name,
                                      f'Цена: {price_in_rubles} Рублей' if price_in_rubles
                                      else 'Цена неизвестна',
                                      f'Год выпуска: {release_year}',
                                      f'Сокет: {socket}',
                                      f'Ядра / Потоки: {cores} / {threads}',
                                      f'Частота процессора: {processor_frequency} Мегагерц',
                                      f'Тип памяти: {memory_type}',
                                      f'Максимальная частота памяти: {memory_frequency} Мегагерц',
                                      f'Тип pcie: {pcie_type}',
                                      f'Потребление: {tdp} Ватт'))

    return render_template('search_components.html',
                           component_type='processors', components=displaying_components,
                           component_image='/static/images/processor.webp',
                           sockets=current_sockets, memory_types=current_memory_types)


def ram_modules(price_from, price_to, people_request):
    # флаг для проверки кол-во модулей памяти
    memory_slots_flag = False

    # достаем типы памяти для оперативной памяти
    current_memory_types = db_methods.get_memory_types()

    current_configuration_data = cookie_functions.get_cookie()
    # все компоненты
    db_sess = data.db_session.create_session()
    if current_configuration_data['motherboards'] != ['не выбран']:
        memory_slots_flag = True

        memory_type_id = current_configuration_data['motherboards'][3]
        components = db_sess.query(RamModules).filter(
            RamModules.memory_type_id == memory_type_id,
            RamModules.price_in_rubles != 0,
            RamModules.price_in_rubles >= price_from,
            RamModules.price_in_rubles <= price_to
        ).all()

        if len(components) == 0:
            components = db_sess.query(RamModules).filter(
                RamModules.memory_type_id == memory_type_id
            ).all()
    elif current_configuration_data['processors'] != ['не выбран']:
        memory_type_id = current_configuration_data['processors'][7]
        components = db_sess.query(RamModules).filter(
            RamModules.memory_type_id == memory_type_id,
            RamModules.price_in_rubles != 0,
            RamModules.price_in_rubles >= price_from,
            RamModules.price_in_rubles <= price_to
        ).all()

        if len(components) == 0:
            components = db_sess.query(RamModules).filter(
                RamModules.memory_type_id == memory_type_id
            ).all()
    else:
        components = db_sess.query(RamModules).filter(
            RamModules.price_in_rubles >= price_from,
            RamModules.price_in_rubles <= price_to).all()

    displaying_components = []
    # делаем оперативную память читабельнее
    for component in components:
        id, name, capacity_gb, frequency, memory_type_id, price_in_rubles = component.get()
        memory_type = current_memory_types[
            int(memory_type_id) - 1] if memory_type_id else 'Неизвестно'
        if memory_slots_flag:
            memory_slots = db_methods.get_memory_slots(name)
            if memory_slots > current_configuration_data['motherboards'][4]:
                continue

        if people_request:
            if set(people_request.lower()) - set(name.lower()) == set():
                displaying_components.append((name,
                                              f'Цена: {price_in_rubles} Рублей',
                                              f'Тип памяти: {memory_type}',
                                              f'Объём памяти: {capacity_gb} Гигабайт',
                                              f'Частота памяти: {frequency} Мегагерц'))
        else:
            displaying_components.append((name,
                                          f'Цена: {price_in_rubles} Рублей',
                                          f'Тип памяти: {memory_type}',
                                          f'Объём памяти: {capacity_gb} Гигабайт',
                                          f'Частота памяти: {frequency} Мегагерц'))

    return render_template('search_components.html',
                           component_type='ram_modules', components=displaying_components,
                           component_image='/static/images/ram_module.webp',
                           memory_types=current_memory_types)


def ram_modules_with_filter(price_from, price_to, filter_type, filter_value):
    # флаг для проверки кол-во модулей памяти
    memory_slots_flag = False

    # достаем типы памяти для оперативной памяти
    current_memory_types = db_methods.get_memory_types()

    current_configuration_data = cookie_functions.get_cookie()
    # все компоненты
    db_sess = data.db_session.create_session()
    if filter_type == "memory_type":
        memory_type_id = current_memory_types.index(filter_value) + 1
        components = db_sess.query(RamModules).filter(
            RamModules.memory_type_id == memory_type_id,
            RamModules.price_in_rubles != 0,
            RamModules.price_in_rubles >= price_from,
            RamModules.price_in_rubles <= price_to).all()

        if len(components) == 0:
            components = db_sess.query(RamModules).filter(
                RamModules.memory_type_id == memory_type_id).all()

    displaying_components = []
    # делаем оперативную память читабельнее
    for component in components:
        id, name, capacity_gb, frequency, memory_type_id, price_in_rubles = component.get()
        memory_type = current_memory_types[
            int(memory_type_id) - 1] if memory_type_id else 'Неизвестно'
        if memory_slots_flag:
            memory_slots = db_methods.get_memory_slots(name)
            if memory_slots > current_configuration_data['motherboards'][4]:
                continue

        displaying_components.append((name,
                                      f'Цена: {price_in_rubles} Рублей',
                                      f'Тип памяти: {memory_type}',
                                      f'Объём памяти: {capacity_gb} Гигабайт',
                                      f'Частота памяти: {frequency} Мегагерц'))

    return render_template('search_components.html',
                           component_type='ram_modules', components=displaying_components,
                           component_image='/static/images/ram_module.webp',
                           memory_types=current_memory_types)


def ssds(price_from, price_to, people_request):
    # все компоненты
    db_sess = data.db_session.create_session()
    components = db_sess.query(SSDs).filter(
        SSDs.price_in_rubles >= price_from,
        SSDs.price_in_rubles <= price_to).all()

    displaying_components = []
    # делаем накопители читабельнее
    for component in components:
        id, name, m2, capacity_gb, price_in_rubles = component.get()

        if people_request:
            if set(people_request.lower()) - set(name.lower()) == set():
                displaying_components.append((name,
                                              f'Цена: {price_in_rubles} Рублей',
                                              f'Тип: {"m2" if m2 else "Неизвестно"}',
                                              f'Объём: {capacity_gb} Гигабайт'))
        else:
            displaying_components.append((name,
                                          f'Цена: {price_in_rubles} Рублей',
                                          f'Тип: {"m2" if m2 else "Неизвестно"}',
                                          f'Объём: {capacity_gb} Гигабайт'))

    return render_template('search_components.html',
                           component_type='SSDs', components=displaying_components,
                           component_image='/static/images/SSD.webp')


def hdds(price_from, price_to, people_request):
    # все компоненты
    db_sess = data.db_session.create_session()
    components = db_sess.query(HDDs).filter(
        HDDs.price_in_rubles >= price_from,
        HDDs.price_in_rubles <= price_to).all()

    displaying_components = []
    # делаем накопители читабельнее
    for component in components:
        id, name, capacity_gb, price_in_rubles = component.get()

        if people_request:
            if set(people_request.lower()) - set(name.lower()) == set():
                displaying_components.append((name,
                                              f'Цена: {price_in_rubles} Рублей',
                                              f'Объём: {capacity_gb} Гигабайт'))
        else:
            displaying_components.append((name,
                                          f'Цена: {price_in_rubles} Рублей',
                                          f'Объём: {capacity_gb} Гигабайт'))

    return render_template('search_components.html',
                           component_type='HDDs', components=displaying_components,
                           component_image='/static/images/HDD.webp')


def videocards(price_from, price_to, people_request):
    current_configuration_data = cookie_functions.get_cookie()
    # все компоненты
    db_sess = data.db_session.create_session()
    if current_configuration_data['power_supplies'] != ['не выбран']:
        power = current_configuration_data['power_supplies'][1]
        if power >= 900:
            max_videocard_tdp = power // 1.7
        else:
            max_videocard_tdp = power // 2
        components = db_sess.query(Videocards).filter(
            Videocards.tdp <= max_videocard_tdp,
            Videocards.price_in_rubles != 0,
            Videocards.price_in_rubles >= price_from,
            Videocards.price_in_rubles <= price_to
        ).all()

        if len(components) == 0:
            components = db_sess.query(Videocards).filter(
                Videocards.tdp <= max_videocard_tdp
            ).all()
    else:
        components = db_sess.query(Videocards).filter(Videocards.price_in_rubles != 0,
                                                      Videocards.price_in_rubles >= price_from,
                                                      Videocards.price_in_rubles <= price_to).all()

    displaying_components = []
    # делаем видеокарты читабельнее
    for component in components:
        id, name, tdp, release_year, memory_capacity, pcie_type, price_in_rubles = component.get()

        if people_request:
            if set(people_request.lower()) - set(name.lower()) == set():
                displaying_components.append((name,
                                              f'Цена: {price_in_rubles} Рублей' if price_in_rubles
                                              else 'Цена неизвестна',
                                              f'Год выпуска: {release_year}',
                                              f'Объём видеопамяти: {memory_capacity} Гигабайт',
                                              f'Тип pcie: {pcie_type}',
                                              f'Потребление: {tdp} Ватт'))
        else:
            displaying_components.append((name,
                                          f'Цена: {price_in_rubles} Рублей' if price_in_rubles
                                          else 'Цена неизвестна',
                                          f'Год выпуска: {release_year}',
                                          f'Объём видеопамяти: {memory_capacity} Гигабайт',
                                          f'Тип pcie: {pcie_type}',
                                          f'Потребление: {tdp} Ватт'))

    return render_template('search_components.html',
                           component_type='videocards', components=displaying_components,
                           component_image='/static/images/videocard.webp')
