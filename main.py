from flask import Flask, render_template
from sqlalchemy import inspect
from data import (db_session, computer_cases, cooling_systems, memory_types,
                  motherboards, power_supplies, processors, ram_modules,
                  sockets, storage_devices, videocards)

app = Flask(__name__)
db_session.global_init("db/components.db")

# надо бд сделать и удалить
# Имитация данных пользователя (в реальном приложении это будет из базы данных)
# Для теста можно менять значения
user = {
    "is_logged_in": False,
    # Измените на True, чтобы протестировать авторизованного пользователя
    "username": "User123"
}


@app.route('/')
def home():
    return render_template('main.html', user=user)


components_types = {'computer_cases': computer_cases.ComputerCases,
                    'cooling_systems': cooling_systems.CoolingSystems,
                    'memory_types': memory_types.MemoryTypes,
                    'motherboards': motherboards.MotherBoards,
                    'power_supplies': power_supplies.PowerSupplies,
                    'processors': processors.Processors,
                    'ram_modules': ram_modules.RamModules,
                    'sockets': sockets.Sockets,
                    'storage_devices': storage_devices.StorageDevices,
                    'videocards': videocards.Videocards}


@app.route('/choose_components/<component_type>')
def choose_components(component_type):
    component_class = components_types[component_type]

    # все компоненты
    db_sess = db_session.create_session()
    components = db_sess.query(component_class).all()

    displaying_components = []
    if component_type == 'processors':
        # достаем сокеты для процессоров
        sockets_db = db_sess.query(sockets.Sockets).all()
        current_sockets = {}
        for socket in sockets_db:
            current_sockets[socket.id] = socket.name
        current_sockets[None] = "Неизвестно"

        # делаем процессоры читабельнее
        for component in components:
            name = component.name
            price = component.price
            socket = current_sockets[component.socket_id]
            cores, threads = component.cores_threads.split(' / ')
            tdp = component.tdp

            displaying_components.append((name,
                                          None,
                                          f'Цена: {price} $',
                                          f'Сокет: {socket}',
                                          f'Ядра: {cores}',
                                          f'Потоки: {threads}',
                                          f'Потребление: {tdp} Ватт'))
    if component_type == 'videocards':
        # делаем видеокарты читабельнее
        for component in components:
            name = component.name
            price = component.price
            tdp = component.tdp

            displaying_components.append((name,
                                          None,
                                          f'Цена: {price} $',
                                          f'Потребление: {tdp} Ватт'))
    if component_type == 'motherboards':
        # достаем сокеты для материнских плат
        sockets_db = db_sess.query(sockets.Sockets).all()
        current_sockets = {}
        for socket in sockets_db:
            current_sockets[socket.id] = socket.name
        current_sockets[None] = "Неизвестно"

        # достаем типы памяти для материнских плат
        memory_types_db = db_sess.query(memory_types.MemoryTypes).all()
        current_memory_types = {}
        for memory_type in memory_types_db:
            current_memory_types[memory_type.id] = memory_type.name
        current_memory_types[None] = "Неизвестно"

        # делаем материнские платы читабельнее
        for component in components:
            name = component.name
            price = component.price
            socket = current_sockets[component.socket_id]
            memory_type = current_memory_types[component.memory_type_id]
            m2_support = component.m2_support
            form_factor = component.form_factor

            displaying_components.append((name,
                                          None,
                                          f'Цена: {price} $',
                                          f'Сокет: {socket}',
                                          f'Тип памяти: {memory_type}',
                                          f'Поддержка m2 ssd: '
                                          f'{"Есть" if m2_support else "Нет"}',
                                          f'Форм-фактор: {form_factor}'))
    if component_type == 'ram_modules':
        # достаем типы памяти для оперативной памяти
        memory_types_db = db_sess.query(memory_types.MemoryTypes).all()
        current_memory_types = {}
        for memory_type in memory_types_db:
            current_memory_types[memory_type.id] = memory_type.name
        current_memory_types[None] = "Неизвестно"

        # делаем оперативную память читабельнее
        for component in components:
            name = component.name
            price = component.price
            memory_type = current_memory_types[component.memory_type_id]
            capacity_gb = component.capacity_gb

            displaying_components.append((name,
                                          None,
                                          f'Цена: {price} $',
                                          f'Тип памяти: {memory_type}',
                                          f'Объём памяти: {capacity_gb}'))
    if component_type == 'cooling_systems':
        # достаем сокеты для систем охлаждения
        sockets_db = db_sess.query(sockets.Sockets).all()
        current_sockets = {}
        for socket in sockets_db:
            current_sockets[socket.id] = socket.name
        current_sockets[None] = "Неизвестно"

        # делаем системы охлаждения читабельнее
        for component in components:
            name = component.name
            price = component.price
            socket = current_sockets[component.socket_id]
            type = component.type
            tdp = component.tdp

            displaying_components.append((name,
                                          None,
                                          f'Цена: {price} $',
                                          f'Сокет: {socket}',
                                          f'Тип системы охлаждения: '
                                          f'{"Воздушное" if type == "Air" else "Водяное"}',
                                          f'Отвод тепла: {tdp} Ватт'))
    if component_type == 'storage_devices':
        # делаем накопители читабельнее
        for component in components:
            name = component.name
            price = component.price
            storage_type = component.storage_type
            capacity_gb = component.capacity_gb

            displaying_components.append((name,
                                          None,
                                          f'Цена: {price} $',
                                          f'Тип накопителя: {storage_type}',
                                          f'Объём: {capacity_gb} Гб'))
    if component_type == 'power_supplies':
        # делаем БП читабельнее
        for component in components:
            name = component.name
            price = component.price
            form_factor = component.form_factor
            power = component.power

            displaying_components.append((name,
                                          None,
                                          f'Цена: {price} $',
                                          f'Форм-фактор: {form_factor}',
                                          f'Мощность: {power} Ватт'))
    if component_type == 'computer_cases':
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
                           user=user,
                           component_type=component_type,
                           components=displaying_components)


@app.route('/builds')
def show_builds():
    return render_template('builds.html', user=user)


@app.route('/login')
def authorization():
    return render_template('authorization.html', user=user)


@app.route('/register')
def registration():
    return render_template('registration.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
