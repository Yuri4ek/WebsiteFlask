from flask import Flask, render_template, request, redirect, abort
from sqlalchemy import inspect
import os
import choose_components_methods
import data.configuration
import data.db_session
import cookie_functions
import data.forum
import data.user
import db_methods
from forms.forum_form import ForumForm
from flask_login import (LoginManager, login_user, login_required, logout_user,
                         current_user)
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.profile import EditProfileForm
from data.computer_cases import ComputerCases
from data.air_coolers import AirCoolers
from data.water_coolers import WaterCoolers
from data.memory_types import MemoryTypes
from data.motherboards import MotherBoards
from data.power_supplies import PowerSupplies
from data.processors import Processors
from data.ram_modules import RamModules
from data.sockets import Sockets
from data.HDDs import HDDs
from data.SSDs import SSDs
from data.videocards import Videocards

components_types = {'computer_cases': ComputerCases,
                    'air_coolers': AirCoolers,
                    'water_coolers': WaterCoolers,
                    'memory_types': MemoryTypes,
                    'motherboards': MotherBoards,
                    'power_supplies': PowerSupplies,
                    'processors': Processors,
                    'ram_modules': RamModules,
                    'sockets': Sockets,
                    'HDDs': HDDs,
                    'SSDs': SSDs,
                    'videocards': Videocards}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'configuration_site_secret_key'

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'components.db')
data.db_session.global_init(DB_PATH)
db_sess = data.db_session.create_session()


@app.route('/', defaults={'component': None})
@app.route('/<component>')
def home(component):
    # Проверяем, есть ли cookie
    data = cookie_functions.get_cookie()

    # Если нет cookie, то создаем
    if not data:
        # создаем cookie
        return cookie_functions.set_cookie()

    # Если cookie и component есть, обновляем данные
    if component:
        try:
            component_type, component_name = component.split(':')

            component_class = components_types[component_type]
            # данные компонента
            component_info = db_sess.query(component_class).filter(
                component_class.name == component_name).all()
            if len(component_info) > 1:
                component_info = [component.get()[1:] for component in
                                  component_info]
            else:
                component_info = component_info[0].get()[1:]

            if component_type == "air_coolers" or component_type == "water_coolers":
                component_type = "cooling_systems"
            elif component_type == "SSDs" or component_type == "HDDs":
                component_type = "storage_devices"
            return cookie_functions.update_cookie(component_type, component_info)
        except:
            pass

    # если нет никаких изменений
    return render_template('main.html', selected_component=data)


@app.route('/build')
def build():
    data = cookie_functions.get_cookie()

    # первый - Регард, второй - ДНС, третий - Авито
    displaying_data = [dict(), dict(), dict()]
    for component_type in data.keys():
        name = data[component_type][0]
        if name == "не выбран":
            return render_template('main.html', selected_component=data)
        if component_type == "ram_modules":
            name = ' '.join(name.split()[:4])
        elif component_type == "computer_cases" or component_type == "power_supplies":
            name = ' '.join(name.split()[:3])
        price_in_rubles = data[component_type][-1]

        displaying_data[0][component_type] = [name, price_in_rubles]
        displaying_data[1][component_type] = [name, price_in_rubles]
        displaying_data[2][component_type] = db_methods.avito_price(name,
                                                                    component_type,
                                                                    price_in_rubles,
                                                                    data[component_type])

    return render_template('build.html', data=displaying_data)


@app.route('/builds')
def show_builds():
    db_sess = data.db_session.create_session()

    # пользователи
    users = db_sess.query(data.user.User).all()

    users_names = []
    users_id = []
    for user in users:
        users_names.append(user.nickname)
        users_id.append(user.id)

    # конфигурации
    configurations = db_sess.query(data.configuration.Configuration).all()

    displaying_configurations = []
    for configuration in configurations:
        user_name = "Неизвестный"
        for user_id in users_id:
            if configuration.user_id == user_id:
                user_name = users_names[users_id.index(user_id)]
        title = configuration.title
        price = 0
        components = configuration.components
        for component_type in components.keys():
            price += components[component_type][-1]
        image_path = configuration.image_path

        displaying_configurations.append(
            (user_name, title, price, components, image_path))

    return render_template('builds.html',
                           configurations=displaying_configurations)


@app.route('/publish_configuration')
def publish_configuration():
    configuration_name = request.args.get('name', None)
    configutarion_data = cookie_functions.get_cookie()

    if current_user.is_authenticated:
        db_sess = data.db_session.create_session()
        configuration = data.configuration.Configuration()
        configuration.title = configuration_name
        configuration.image_path = "static/images/computer_case.webp"
        configuration.components = configutarion_data
        configuration.user_id = current_user.id
        db_sess.add(configuration)
        db_sess.commit()
        return redirect("/builds")

    return render_template('main.html', selected_component=configutarion_data)


@app.route('/choose_components/computer_cases')
def choose_computer_cases():
    price_from = 0
    price_to = 1000000
    people_request = None

    # Получаем фильтры (параметр filters из query string)
    filters = request.args.get('filters', None)
    if filters:
        price_from, price_to = db_methods.get_price_limit(filters)
        if "search" in filters:
            search, people_request = filters.split(':')

    return choose_components_methods.computer_cases(price_from, price_to, people_request)


@app.route('/choose_components/air_coolers')
def choose_air_coolers():
    price_from = 0
    price_to = 1000000
    people_request = None

    # Получаем фильтры (параметр filters из query string)
    filters = request.args.get('filters', None)
    if filters:
        price_from, price_to = db_methods.get_price_limit(filters)
        if "search" in filters:
            search, people_request = filters.split(':')

    return choose_components_methods.air_coolers(price_from, price_to, people_request)


@app.route('/choose_components/water_coolers')
def choose_water_coolers():
    price_from = 0
    price_to = 1000000
    people_request = None

    # Получаем фильтры (параметр filters из query string)
    filters = request.args.get('filters', None)
    if filters:
        price_from, price_to = db_methods.get_price_limit(filters)
        if "search" in filters:
            search, people_request = filters.split(':')

    return choose_components_methods.water_coolers(price_from, price_to, people_request)


@app.route('/choose_components/motherboards')
def choose_motherboards():
    price_from = 0
    price_to = 1000000
    people_request = None

    # Получаем фильтры (параметр filters из query string)
    filters = request.args.get('filters', None)
    if filters:
        price_from, price_to = db_methods.get_price_limit(filters)
        if "socket" in filters or "memory_type" in filters or "m2_support" in filters:
            if len(filters.split(',')) >= 3:
                filter_type, filter_value = filters.split(',')[-1].split(':')
            else:
                filter_type, filter_value = filters.split(':')
            return choose_components_methods.motherboards_with_filter(price_from, price_to,
                                                                      filter_type,
                                                                      filter_value)
        if "search" in filters:
            search, people_request = filters.split(':')

    return choose_components_methods.motherboards(price_from, price_to, people_request)


@app.route('/choose_components/power_supplies')
def choose_power_supplies():
    price_from = 0
    price_to = 1000000
    people_request = None

    # Получаем фильтры (параметр filters из query string)
    filters = request.args.get('filters', None)
    if filters:
        price_from, price_to = db_methods.get_price_limit(filters)
        if "search" in filters:
            search, people_request = filters.split(':')

    return choose_components_methods.power_supplies(price_from, price_to, people_request)


@app.route('/choose_components/processors/')
def choose_processors():
    price_from = 0
    price_to = 1000000
    people_request = None

    # Получаем фильтры (параметр filters из query string)
    filters = request.args.get('filters', None)
    if filters:
        price_from, price_to = db_methods.get_price_limit(filters)
        if "socket" in filters or "memory_type" in filters:
            if len(filters.split(',')) >= 3:
                filter_type, filter_value = filters.split(',')[-1].split(':')
            else:
                filter_type, filter_value = filters.split(':')
            return choose_components_methods.processors_with_filter(price_from, price_to,
                                                                    filter_type,
                                                                    filter_value)
        if "search" in filters:
            search, people_request = filters.split(':')

    return choose_components_methods.processors(price_from, price_to, people_request)


@app.route('/choose_components/ram_modules')
def choose_ram_modules():
    price_from = 0
    price_to = 1000000
    people_request = None

    # Получаем фильтры (параметр filters из query string)
    filters = request.args.get('filters', None)
    if filters:
        price_from, price_to = db_methods.get_price_limit(filters)
        if "memory_type" in filters:
            if len(filters.split(',')) >= 3:
                filter_type, filter_value = filters.split(',')[-1].split(':')
            else:
                filter_type, filter_value = filters.split(':')
            return choose_components_methods.ram_modules_with_filter(price_from, price_to,
                                                                     filter_type,
                                                                     filter_value)
        if "search" in filters:
            search, people_request = filters.split(':')

    return choose_components_methods.ram_modules(price_from, price_to, people_request)


@app.route('/choose_components/SSDs')
def choose_SSDs():
    price_from = 0
    price_to = 1000000
    people_request = None

    # Получаем фильтры (параметр filters из query string)
    filters = request.args.get('filters', None)
    if filters:
        price_from, price_to = db_methods.get_price_limit(filters)
        if "search" in filters:
            search, people_request = filters.split(':')

    return choose_components_methods.ssds(price_from, price_to, people_request)


@app.route('/choose_components/HDDs')
def choose_HDDs():
    price_from = 0
    price_to = 1000000
    people_request = None

    # Получаем фильтры (параметр filters из query string)
    filters = request.args.get('filters', None)
    if filters:
        price_from, price_to = db_methods.get_price_limit(filters)
        if "search" in filters:
            search, people_request = filters.split(':')

    return choose_components_methods.hdds(price_from, price_to, people_request)


@app.route('/choose_components/videocards')
def choose_videocards():
    price_from = 0
    price_to = 1000000
    people_request = None

    # Получаем фильтры (параметр filters из query string)
    filters = request.args.get('filters', None)
    if filters:
        price_from, price_to = db_methods.get_price_limit(filters)
        if "search" in filters:
            search, people_request = filters.split(':')

    return choose_components_methods.videocards(price_from, price_to, people_request)


@app.route('/components/<component_type>')
def show_components_table(component_type):
    component_class = components_types[component_type]

    # название колонн
    inspector = inspect(component_class)
    columns = [column.name for column in inspector.mapper.columns]

    # все компоненты
    components = [el.get() for el in db_sess.query(component_class).all()]

    if component_type == 'processors' or component_type == 'motherboards':
        current_sockets = db_methods.get_sockets()
        i = columns.index("socket_id")
        for component in components:
            component[i] = current_sockets[int(component[i]) - 1] if component[
                i] else None
    if component_type == 'ram_modules' or component_type == 'motherboards' or component_type == 'processors':
        i = columns.index("memory_type_id")
        current_memory_types = db_methods.get_memory_types()
        for component in components:
            component[i] = current_memory_types[int(component[i]) - 1] if \
                component[i] else None

    return render_template('components_table.html',
                           keys=columns,
                           components=components)


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()

    if form.validate_on_submit():
        db_sess = data.db_session.create_session()
        if db_sess.query(data.user.User).filter(data.user.User.email == form.email.data).first():
            return render_template('registration.html', form=form,
                                   message="Пользователь с такой почтой уже существует")
        user = data.user.User(
            nickname=form.nickname.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')
    return render_template('registration.html', form=form)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = data.db_session.create_session()
    return db_sess.query(data.user.User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def authorization():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = data.db_session.create_session()
        user = db_sess.query(data.user.User).filter(
            (data.user.User.nickname == form.nickname_email.data) | (
                    data.user.User.email == form.nickname_email.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/")
        return render_template('authorization.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('authorization.html', form=form)


# Отображение списка форумов
@app.route('/forums')
def forums_page():
    db_sess = data.db_session.create_session()
    forums = db_sess.query(data.forum.Forum).all()
    if current_user.is_authenticated:
        return render_template('forums.html', forums=forums,
                               user=current_user)
    else:
        return render_template('notauth.html', forums=forums)


# Просмотр конкретного форума
@app.route('/forum/<int:forum_id>')
def forum_detail(forum_id):
    db_sess = data.db_session.create_session()
    forum = db_sess.query(data.forum.Forum).get(forum_id)
    if not forum:
        abort(404)
    return render_template('forum_detail.html', forum=forum, user=forum.user)


# Страница для добавления нового поста на форум
@app.route('/forum/new_forum_post', methods=['GET', 'POST'])
def new_forum_post():
    db_sess = data.db_session.create_session()
    form = ForumForm()
    if current_user.is_authenticated:
        if request.method == 'POST':
            # Создание нового форума в базе данных
            forum = data.forum.Forum(
                title=form.title.data,
                content=form.content.data
            )
            current_user.forums.append(
                forum)  # Предполагается, что связь установлена
            db_sess.merge(current_user)
            db_sess.commit()  # Сохраняем изменения в базе данных
            return redirect('/forums')
    return render_template('create_forum.html')


# пробная версия профиля
@app.route('/profile')
def profile():
    db_sess = data.db_session.create_session()
    user = db_sess.query(data.user.User).filter(data.user.User.id == current_user.id).one()
    return render_template('profile.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    db_sess = data.db_session.create_session()
    user = db_sess.query(data.user.User).filter(data.user.User.id == current_user.id).one()
    if request.method == 'POST':
        # Обработка отправленной формы
        print(user.nickname, 'vfdbdsgs')
        user.nickname = form.nickname.data
        user.email = form.email.data
        user.password = form.password.data
        db_sess.commit()
        return redirect('/profile')  # Перенаправление на страницу профиля

    return render_template('edit_profile.html', user=user)


@app.get("/print_cookie")
def print_cookie():
    return cookie_functions.get_cookie()


@app.get("/clear_cookie")
def clear_cookie_handler():
    return cookie_functions.clear_cookie()


if __name__ == '__main__':
    app.run(debug=True)
