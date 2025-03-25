import sqlite3

con = sqlite3.connect("../../db/components.db")
cur = con.cursor()
cur.execute("DELETE FROM computer_cases")
con.commit()
con.close()

cases = [
    # Full Tower
    ("Corsair Obsidian 1000D", "Full Tower", 550.00, "USD"),
    ("Be Quiet! Dark Base Pro 901", "Full Tower", 300.00, "USD"),
    ("Phanteks Enthoo 719", "Full Tower", 200.00, "USD"),
    ("Lian Li PC-O11 Dynamic XL", "Full Tower", 220.00, "USD"),
    ("Cooler Master Cosmos C700M", "Full Tower", 450.00, "USD"),
    ("Fractal Design Define 7 XL", "Full Tower", 230.00, "USD"),
    ("Thermaltake Core X71", "Full Tower", 180.00, "USD"),
    ("InWin 909", "Full Tower", 400.00, "USD"),
    ("Corsair 7000D Airflow", "Full Tower", 250.00, "USD"),
    ("NZXT H9 Elite", "Full Tower", 240.00, "USD"),
    # Mid Tower
    ("Fractal Design Meshify 2", "Mid Tower", 110.00, "USD"),
    ("NZXT H710i", "Mid Tower", 170.00, "USD"),
    ("Corsair 4000D Airflow", "Mid Tower", 95.00, "USD"),
    ("Phanteks Eclipse P500A", "Mid Tower", 140.00, "USD"),
    ("Lian Li Lancool III", "Mid Tower", 150.00, "USD"),
    ("Cooler Master MasterBox TD500 Mesh", "Mid Tower", 120.00, "USD"),
    ("Be Quiet! Silent Base 802", "Mid Tower", 160.00, "USD"),
    ("MSI MAG Forge 100R", "Mid Tower", 80.00, "USD"),
    ("Thermaltake S500 TG", "Mid Tower", 130.00, "USD"),
    ("Zalman S4 Plus", "Mid Tower", 60.00, "USD"),
    ("Fractal Design North", "Mid Tower", 130.00, "USD"),
    ("Corsair iCUE 5000X RGB", "Mid Tower", 200.00, "USD"),
    ("Phanteks Evolv X", "Mid Tower", 190.00, "USD"),
    ("AeroCool Aero One", "Mid Tower", 55.00, "USD"),
    ("Lian Li PC-O11 Air", "Mid Tower", 140.00, "USD"),
    # Mini Tower / Mini-ITX
    ("NZXT H1 V2", "Mini-ITX", 200.00, "USD"),
    ("Fractal Design Terra", "Mini-ITX", 180.00, "USD"),
    ("Cooler Master NR200P", "Mini-ITX", 110.00, "USD"),
    ("SilverStone Sugo 16", "Mini-ITX", 120.00, "USD"),
    ("In Win A1 Plus", "Mini-ITX", 220.00, "USD"),
    ("Lian Li Q58", "Mini-ITX", 130.00, "USD"),
    ("Thermaltake Tower 100", "Mini-ITX", 100.00, "USD"),
    ("Phanteks Evolv Shift 2", "Mini-ITX", 150.00, "USD"),
    ("Jonsbo A4", "Mini-ITX", 140.00, "USD"),
    ("Fractal Design Ridge", "Mini-ITX", 130.00, "USD"),
    # Micro-ATX
    ("Fractal Design Define Nano S", "Micro-ATX", 80.00, "USD"),
    ("Corsair Crystal 280X", "Micro-ATX", 130.00, "USD"),
    ("Thermaltake Versa H18", "Micro-ATX", 50.00, "USD"),
    ("Cooler Master MasterBox Q300L", "Micro-ATX", 45.00, "USD"),
    ("SilverStone PS15", "Micro-ATX", 70.00, "USD"),
]

from data import db_session
from data.computer_cases import ComputerCases

db_session.global_init("../../db/components.db")

db_sess = db_session.create_session()
for case in cases:
    computerCase = ComputerCases()
    computerCase.name = case[0]
    computerCase.form_factor = case[1]
    computerCase.price = case[2]
    computerCase.currency = case[3]
    db_sess.add(computerCase)
db_sess.commit()

db_sess = db_session.create_session()
current_computerCases = db_sess.query(ComputerCases).all()

for current_computerCase in current_computerCases:
    print(current_computerCase.name)
