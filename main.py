from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import inspect
from choose_components_methods import *
from data.forum import Forum
from data.comment import Comment

app = Flask(__name__)
db_session.global_init("db/components.db")


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
                component_type == 'processors' or component_type == 'ram_modules' or
                component_type == 'videocards'):
            return update_cookies(component_type, component_name)
        return update_cookie('configuration_data', component_type,
                             component_name)

    # если нет никаких изменений
    return render_template('main.html', selected_component=data)


@app.route('/choose_components/computer_cases')
def choose_computer_cases():
    return computer_cases()


@app.route('/choose_components/cooling_systems')
def choose_cooling_systems():
    return cooling_systems()


@app.route('/choose_components/motherboards')
def choose_motherboards():
    return motherboards()


@app.route('/choose_components/power_supplies')
def choose_power_supplies():
    return power_supplies()


@app.route('/choose_components/processors')
def choose_processors():
    return processors()


@app.route('/choose_components/ram_modules')
def choose_ram_modules():
    return ram_modules()


@app.route('/choose_components/storage_devices')
def choose_storage_devices():
    return storage_devices()


@app.route('/choose_components/videocards')
def choose_videocards():
    return videocards()


@app.route('/components/<component_type>')
def show_components_table(component_type):
    component_class = components_types[component_type]

    # все компоненты
    db_sess = db_session.create_session()
    components = db_sess.query(component_class).all()

    if (component_type == 'processors' or component_type == 'cooling_systems'
            or component_type == 'motherboards'):
        current_sockets, sockets_db = get_sockets()
        for component in components:
            component.socket_id = current_sockets[component.socket_id]
    if component_type == 'ram_modules' or component_type == 'motherboards':
        current_memory_types, memory_types_db = get_memory_types()
        for component in components:
            component.memory_type_id = current_memory_types[
                component.memory_type_id]

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


@app.get("/clear_cookies")
def clear_cookies_handler():
    return clear_cookies()


# Страница для отображения списка форумов
@app.route('/forums')
def forums_page():
    db_sess = db_session.create_session()
    forums = db_sess.query(Forum)  # Получаем все форумы из базы данных
    return render_template('forums.html', forums=forums)


# Страница форума с темой
@app.route('/forum/<int:forum_id>')
def forum_detail(forum_id):
    db_sess = db_session.create_session()
    forum = db_sess.query(Forum).get(forum_id)  # Получаем форум по ID

    if forum is None:
        return "Форум не найден", 404
    return render_template('forum_detail.html', forum=forum)


# Страница для добавления нового поста на форум
@app.route('/forum/create', methods=['GET', 'POST'])
def new_forum_post():
    db_sess = db_session.create_session()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        # Создание нового форума в базе данных
        new_forum = Forum(title=title, content=content)
        db_sess.add(new_forum)
        db_sess.commit()  # Сохраняем изменения в базе данных
        return redirect('/forums')
    return render_template('create_forum.html')

 # Обработчик для добавления комментария
@app.route('/forum/<int:forum_id>/comment', methods=['POST'])
def add_comment(forum_id):
    db_sess = db_session.create_session()
    forum = db_sess.query(Forum).get(forum_id)
    if forum is None:
        return "Форум не найден", 404
    content = request.form['content']
    new_comment = Comment(content=content, forum_id=forum_id)
    db_sess.add(new_comment)
    db_sess.commit()  # Сохраняем изменения в базе данных
    return redirect(url_for('forum_detail', forum_id=forum_id))


if __name__ == '__main__':
    app.run(debug=True)
