import sqlite3

con = sqlite3.connect("../../db/components.db")
cur = con.cursor()
cur.execute("DELETE FROM configurations")
con.commit()
con.close()

configurations = [('Yes', {'1': 1, "2": 2}, 1)]

from data import db_session
from data.configurations import Configurations

db_session.global_init("../../db/components.db")

db_sess = db_session.create_session()
for configuration in configurations:
    class_configuration = Configurations()
    class_configuration.title = configuration[0]
    class_configuration.components = configuration[1]
    class_configuration.user_id = configuration[2]
    db_sess.add(class_configuration)
db_sess.commit()

db_sess = db_session.create_session()
current_configurations = db_sess.query(Configurations).all()

for current_configuration in current_configurations:
    print(current_configuration.components)
