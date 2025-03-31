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


@app.route('/choose_components/<components_type>')
def choose_components(components_type):
    return render_template('search_components.html',
                           user=user,
                           component=components_type)


if __name__ == '__main__':
    app.run(debug=True)
