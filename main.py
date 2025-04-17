from flask import Flask, render_template
from sqlalchemy import inspect
from data.db_imports import *
from cookie_functions import *

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


@app.route('/', defaults={'component': None})
@app.route('/<component>')
def home(component):
    # Проверяем, есть ли cookie
    data = get_cookie('configuration_data')

    # Если нет cookie, то создаем
    if not data:
        # создаем cookie
        return set_cookies()

    # Если cookie и component есть, обновляем данные
    if component:
        component_type, component_name = component.split(':')
        if (component_type == 'cooling_systems' or component_type == 'motherboards' or
                component_type == 'processors' or component_type == 'videocards'):
            return update_cookies(component_type, component_name)
        return update_cookie('configuration_data', component_type, component_name)

    # если нет никаких изменений
    return render_template('main.html', selected_component=data)


@app.route('/choose_components/computer_cases')
def choose_computer_cases():
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


@app.route('/choose_components/cooling_systems')
def choose_cooling_systems():
    # все компоненты
    db_sess = db_session.create_session()
    components = db_sess.query(CoolingSystems).all()

    # достаем сокеты для систем охлаждения
    sockets_db = db_sess.query(Sockets).all()
    current_sockets = {}
    for socket in sockets_db:
        current_sockets[socket.id] = socket.name
    current_sockets[None] = "Неизвестно"

    displaying_components = []
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

    return render_template('search_components.html',
                           component_type='cooling_systems',
                           components=displaying_components,
                           sockets=sockets_db)


@app.route('/choose_components/motherboards')
def choose_motherboards():
    # все компоненты
    db_sess = db_session.create_session()
    components = db_sess.query(MotherBoards).all()
    # достаем сокеты для материнских плат
    sockets_db = db_sess.query(Sockets).all()
    current_sockets = {}
    for socket in sockets_db:
        current_sockets[socket.id] = socket.name
    current_sockets[None] = "Неизвестно"

    # достаем типы памяти для материнских плат
    memory_types_db = db_sess.query(MemoryTypes).all()
    current_memory_types = {}
    for memory_type in memory_types_db:
        current_memory_types[memory_type.id] = memory_type.name
    current_memory_types[None] = "Неизвестно"

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
                                      None,
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


@app.route('/choose_components/power_supplies')
def choose_power_supplies():
    # все компоненты
    db_sess = db_session.create_session()
    components = db_sess.query(PowerSupplies).all()

    displaying_components = []
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

    return render_template('search_components.html',
                           component_type='power_supplies',
                           components=displaying_components)


@app.route('/choose_components/processors')
def choose_processors():
    # все компоненты
    db_sess = db_session.create_session()
    components = db_sess.query(Processors).all()

    # достаем сокеты для процессоров
    sockets_db = db_sess.query(Sockets).all()
    current_sockets = {}
    for socket in sockets_db:
        current_sockets[socket.id] = socket.name
    current_sockets[None] = "Неизвестно"

    displaying_components = []
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

    return render_template('search_components.html',
                           component_type='processors',
                           components=displaying_components,
                           sockets=sockets_db)


@app.route('/choose_components/ram_modules')
def choose_ram_modules():
    # все компоненты
    db_sess = db_session.create_session()
    components = db_sess.query(RamModules).all()

    # достаем типы памяти для оперативной памяти
    memory_types_db = db_sess.query(MemoryTypes).all()
    current_memory_types = {}
    for memory_type in memory_types_db:
        current_memory_types[memory_type.id] = memory_type.name
    current_memory_types[None] = "Неизвестно"

    displaying_components = []
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

    return render_template('search_components.html',
                           component_type='ram_modules',
                           components=displaying_components,
                           memory_types=memory_types_db)


@app.route('/choose_components/storage_devices')
def choose_storage_devices():
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
                                      None,
                                      f'Цена: {price} $',
                                      f'Тип накопителя: {storage_type}',
                                      f'Объём: {capacity_gb} Гб'))

    return render_template('search_components.html',
                           component_type='storage_devices',
                           components=displaying_components)


@app.route('/choose_components/videocards')
def choose_videocards():
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
                                      None,
                                      f'Цена: {price} $',
                                      f'Потребление: {tdp} Ватт'))

    return render_template('search_components.html',
                           component_type='videocards',
                           components=displaying_components)


@app.route('/components/<component_type>')
def show_components_table(component_type):
    component_class = components_types[component_type]

    # все компоненты
    db_sess = db_session.create_session()
    components = db_sess.query(component_class).all()

    # название колонн
    inspector = inspect(component_class)
    columns = [column.name for column in inspector.mapper.columns]

    return render_template('components_table.html',
                           keys=columns,
                           components=components)


@app.route('/builds')
def show_builds():
    return render_template('builds.html')


@app.route('/login')
def authorization():
    return render_template('authorization.html')


@app.route('/register')
def registration():
    return render_template('registration.html')


@app.get("/delete_cookies")
def delete_cookies():
    resp = make_response("Cookie удален")
    resp.delete_cookie('configuration_data')
    resp.delete_cookie('filter_data')
    return resp


if __name__ == '__main__':
    app.run(debug=True)
