from db_methods import *
from cookie_functions import *


def computer_cases():
    # все компоненты
    db_sess = db_session.create_session()
    components = db_sess.query(ComputerCases).all()

    displaying_components = []
    # делаем корпуса читабельнее
    for component in components:
        name = component.name
        image_path = component.image_path
        price = component.price
        form_factor = component.form_factor

        displaying_components.append((name,
                                      image_path,
                                      f'Цена: {price} $',
                                      f'Форм-фактор: {form_factor}'))

    return render_template('search_components.html',
                           component_type='computer_cases',
                           components=displaying_components)


def cooling_systems():
    db_sess = db_session.create_session()

    filter_data = get_cookie('filter_data')
    if filter_data['socket'] or filter_data['processor_tdp']:
        components = db_sess.query(CoolingSystems).filter(
            CoolingSystems.socket_id == filter_data['socket'],
            CoolingSystems.tdp >= filter_data['processor_tdp']).all()
    else:
        # все компоненты
        components = db_sess.query(CoolingSystems).all()

    # достаем сокеты для систем охлаждения
    current_sockets, sockets_db = get_sockets()

    displaying_components = []
    # делаем системы охлаждения читабельнее
    for component in components:
        name = component.name
        price = component.price
        socket = current_sockets[component.socket_id]
        type = component.type
        tdp = component.tdp

        displaying_components.append((name,
                                      '/static/images/coolers/air_cooler.webp'
                                      if type == "Air" else
                                      '/static/images/coolers/water_cooler.webp',
                                      f'Цена: {price} $',
                                      f'Сокет: {socket}',
                                      f'Тип системы охлаждения: '
                                      f'{"Воздушное" if type == "Air" else "Водяное"}',
                                      f'Отвод тепла: {tdp} Ватт'))

    return render_template('search_components.html',
                           component_type='cooling_systems',
                           components=displaying_components,
                           sockets=sockets_db)


def motherboards():
    db_sess = db_session.create_session()

    filter_data = get_cookie('filter_data')
    if filter_data['socket']:
        components = db_sess.query(MotherBoards).filter(
            MotherBoards.socket_id == filter_data['socket']).all()
    elif filter_data['memory_type']:
        components = db_sess.query(MotherBoards).filter(
            MotherBoards.memory_type_id == filter_data['memory_type']).all()
    elif filter_data['m2_support']:
        components = db_sess.query(MotherBoards).filter(
            MotherBoards.m2_support == filter_data['m2_support']).all()
    else:
        # все компоненты
        components = db_sess.query(MotherBoards).all()

    # достаем сокеты для материнских плат
    current_sockets, sockets_db = get_sockets()

    # достаем типы памяти для материнских плат
    current_memory_types, memory_types_db = get_memory_types()

    displaying_components = []
    # делаем материнские платы читабельнее
    for component in components:
        name = component.name
        price = component.price
        socket = current_sockets[component.socket_id]
        memory_type = current_memory_types[component.memory_type_id]
        m2_support = component.m2_support
        form_factor = component.form_factor

        displaying_components.append((name,
                                      '/static/images/motherboards/motherboard.webp',
                                      f'Цена: {price} $',
                                      f'Сокет: {socket}',
                                      f'Тип памяти: {memory_type}',
                                      f'Поддержка m2 ssd: '
                                      f'{"Есть" if m2_support else "Нет"}',
                                      f'Форм-фактор: {form_factor}'))

    return render_template('search_components.html',
                           component_type='motherboards',
                           components=displaying_components,
                           sockets=sockets_db,
                           memory_types=memory_types_db)


def power_supplies():
    db_sess = db_session.create_session()

    filter_data = get_cookie('filter_data')
    if filter_data['processor_tdp'] or filter_data['videocard_tdp']:
        total_tdp = (filter_data['processor_tdp'] + filter_data[
            'videocard_tdp']) * 1.3
        components = db_sess.query(PowerSupplies).filter(
            PowerSupplies.power >= total_tdp).all()
    else:
        # все компоненты
        components = db_sess.query(PowerSupplies).all()

    displaying_components = []
    # делаем БП читабельнее
    for component in components:
        name = component.name
        price = component.price
        form_factor = component.form_factor
        power = component.power

        displaying_components.append((name,
                                      '/static/images/power_supplies/power_supplie.webp',
                                      f'Цена: {price} $',
                                      f'Форм-фактор: {form_factor}',
                                      f'Мощность: {power} Ватт'))

    return render_template('search_components.html',
                           component_type='power_supplies',
                           components=displaying_components)


def processors():
    db_sess = db_session.create_session()

    filter_data = get_cookie('filter_data')
    if filter_data['socket'] or filter_data['processor_tdp']:
        components = db_sess.query(Processors).filter(
            Processors.socket_id == filter_data['socket'],
            Processors.tdp <= filter_data['processor_tdp']).all()
    else:
        # все компоненты
        components = db_sess.query(Processors).all()

    # достаем сокеты для процессоров
    current_sockets, sockets_db = get_sockets()

    displaying_components = []
    # делаем процессоры читабельнее
    for component in components:
        name = component.name
        price = component.price
        socket = current_sockets[component.socket_id]
        cores, threads = component.cores_threads.split(' / ')
        tdp = component.tdp

        displaying_components.append((name,
                                      '/static/images/processors/processor.webp',
                                      f'Цена: {price} $',
                                      f'Сокет: {socket}',
                                      f'Ядра: {cores}',
                                      f'Потоки: {threads}',
                                      f'Потребление: {tdp} Ватт'))

    return render_template('search_components.html',
                           component_type='processors',
                           components=displaying_components,
                           sockets=sockets_db)


def ram_modules():
    db_sess = db_session.create_session()

    filter_data = get_cookie('filter_data')
    if filter_data['memory_type']:
        components = db_sess.query(RamModules).filter(
            RamModules.memory_type_id == filter_data['memory_type']).all()
    else:
        # все компоненты
        components = db_sess.query(RamModules).all()

    # достаем типы памяти для оперативной памяти
    current_memory_types, memory_types_db = get_memory_types()

    displaying_components = []
    # делаем оперативную память читабельнее
    for component in components:
        name = component.name
        price = component.price
        memory_type = current_memory_types[component.memory_type_id]
        capacity_gb = component.capacity_gb

        displaying_components.append((name,
                                      '/static/images/ram_modules/ram_module.webp',
                                      f'Цена: {price} $',
                                      f'Тип памяти: {memory_type}',
                                      f'Объём памяти: {capacity_gb}'))

    return render_template('search_components.html',
                           component_type='ram_modules',
                           components=displaying_components,
                           memory_types=memory_types_db)


def storage_devices():
    # все компоненты
    db_sess = db_session.create_session()
    components = db_sess.query(StorageDevices).all()

    displaying_components = []
    # делаем накопители читабельнее
    for component in components:
        name = component.name
        price = component.price
        storage_type = component.storage_type
        capacity_gb = component.capacity_gb

        displaying_components.append((name,
                                      '/static/images/storage_devices/storage_device.webp',
                                      f'Цена: {price} $',
                                      f'Тип накопителя: {storage_type}',
                                      f'Объём: {capacity_gb} Гб'))

    return render_template('search_components.html',
                           component_type='storage_devices',
                           components=displaying_components)


def videocards():
    # все компоненты
    db_sess = db_session.create_session()
    components = db_sess.query(Videocards).all()

    displaying_components = []
    # делаем видеокарты читабельнее
    for component in components:
        name = component.name
        price = component.price
        tdp = component.tdp

        displaying_components.append((name,
                                      '/static/images/videocards/videocard.webp',
                                      f'Цена: {price} $',
                                      f'Потребление: {tdp} Ватт'))

    return render_template('search_components.html',
                           component_type='videocards',
                           components=displaying_components)
