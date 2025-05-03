from flask import Flask, render_template, request, redirect, url_for, abort
from sqlalchemy import inspect
from choose_components_methods import *
from forms.forum_form import ForumForm
from flask_login import (LoginManager, login_user, login_required, logout_user,
                         current_user)
from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'configuration_site_secret_key'
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
    '''if component:
        component_type, component_name = component.split(':')
        if (component_type == 'cooling_systems' or component_type == 'motherboards' or
                component_type == 'processors' or component_type == 'ram_modules' or
                component_type == 'videocards'):
            return update_cookies(component_type, component_name)
        return update_cookie('configuration_data', component_type,
                             component_name)'''

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


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', form=form,
                                   message="Пользователь с такой почтой уже существует")
        user = User(
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
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def authorization():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter((User.nickname == form.nickname_email.data) |
                                          (User.email == form.nickname_email.data)).first()
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
    db_sess = db_session.create_session()
    forums = db_sess.query(Forum).all()
    return render_template('forums.html', forums=forums, user=current_user if current_user.is_authenticated else None)

# Просмотр конкретного форума
@app.route('/forum/<int:forum_id>')
def forum_detail(forum_id):
    db_sess = db_session.create_session()
    forum = db_sess.query(Forum).get(forum_id)
    if not forum:
        abort(404)
    return render_template('forum_detail.html', forum=forum, user=forum.user)


# Страница для добавления нового поста на форум
@app.route('/forum/new_forum_post', methods=['GET', 'POST'])
def new_forum_post():
    db_sess = db_session.create_session()
    form = ForumForm()
    if current_user.is_authenticated:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            # Создание нового форума в базе данных
            forum = Forum(
                title=form.title.data,
                content=form.content.data
            )
            current_user.forums.append(forum)  # Предполагается, что связь установлена
            db_sess.merge(current_user)
            db_sess.commit()  # Сохраняем изменения в базе данных
            return redirect('/forums')
    return render_template('create_forum.html')



""" # Обработчик для добавления комментария
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
    return redirect(url_for('forum_detail', forum_id=forum_id))"""


@app.get("/clear_cookies")
def clear_cookies_handler():
    return clear_cookies()


if __name__ == '__main__':
    app.run(debug=True)
