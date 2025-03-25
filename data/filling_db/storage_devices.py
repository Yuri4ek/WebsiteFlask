import sqlite3

con = sqlite3.connect("../../db/components.db")
cur = con.cursor()
cur.execute("DELETE FROM storage_devices")
con.commit()
con.close()

storages = [
    # HDD
    ("Seagate BarraCuda 4TB", "HDD", 4000, "3.5", 80.00, "USD"),
    ("Western Digital Blue 2TB", "HDD", 2000, "3.5", 55.00, "USD"),
    ("Toshiba MG08ACA 18TB", "HDD", 18000, "3.5", 255.00, "USD"),
    ("Seagate Exos X18 16TB", "HDD", 16000, "3.5", 300.00, "USD"),
    ("Western Digital Red Pro 6TB", "HDD", 6000, "3.5", 180.00, "USD"),
    ("Seagate SkyHawk 1TB", "HDD", 1000, "3.5", 50.00, "USD"),
    ("Western Digital Purple 8TB", "HDD", 8000, "3.5", 200.00, "USD"),
    ("Toshiba N300 4TB", "HDD", 4000, "3.5", 90.00, "USD"),
    ("Seagate IronWolf 10TB", "HDD", 10000, "3.5", 230.00, "USD"),
    ("Western Digital Blue 500GB", "HDD", 500, "3.5", 35.00, "USD"),
    ("HGST Ultrastar 12TB", "HDD", 12000, "3.5", 250.00, "USD"),
    ("Seagate BarraCuda 2TB", "HDD", 2000, "2.5", 60.00, "USD"),
    ("Toshiba MQ04 1TB", "HDD", 1000, "2.5", 45.00, "USD"),
    ("Western Digital Black 6TB", "HDD", 6000, "3.5", 190.00, "USD"),
    ("Seagate FireCuda 2TB", "HDD", 2000, "2.5", 75.00, "USD"),
    # SSD (SATA)
    ("Samsung 870 EVO 1TB", "SSD", 1000, "2.5", 90.00, "USD"),
    ("Crucial BX500 2TB", "SSD", 2000, "2.5", 120.00, "USD"),
    ("Kingston A400 480GB", "SSD", 480, "2.5", 40.00, "USD"),
    ("SanDisk SSD Plus 1TB", "SSD", 1000, "2.5", 85.00, "USD"),
    ("Western Digital Green 500GB", "SSD", 500, "2.5", 50.00, "USD"),
    ("Samsung 870 QVO 4TB", "SSD", 4000, "2.5", 250.00, "USD"),
    ("Crucial MX500 250GB", "SSD", 250, "2.5", 35.00, "USD"),
    ("Kingston NV2 500GB", "SSD", 500, "2.5", 45.00, "USD"),
    ("SanDisk Ultra 3D 2TB", "SSD", 2000, "2.5", 130.00, "USD"),
    ("Western Digital Blue 1TB", "SSD", 1000, "2.5", 80.00, "USD"),
    ("ADATA SU800 256GB", "SSD", 256, "2.5", 30.00, "USD"),
    ("Samsung 860 EVO 500GB", "SSD", 500, "2.5", 60.00, "USD"),
    ("Crucial BX500 120GB", "SSD", 120, "2.5", 20.00, "USD"),
    ("Kingston A400 240GB", "SSD", 240, "2.5", 28.00, "USD"),
    ("SanDisk SSD Plus 480GB", "SSD", 480, "2.5", 45.00, "USD"),
    # NVMe
    ("Samsung 990 Pro 2TB", "NVMe", 2000, "M.2", 180.00, "USD"),
    ("WD Black SN850X 4TB", "NVMe", 4000, "M.2", 280.00, "USD"),
    ("Crucial T705 1TB", "NVMe", 1000, "M.2", 150.00, "USD"),
    ("Corsair MP600 Pro 8TB", "NVMe", 8000, "M.2", 900.00, "USD"),
    ("Lexar NM790 2TB", "NVMe", 2000, "M.2", 140.00, "USD"),
    ("Samsung 970 EVO Plus 500GB", "NVMe", 500, "M.2", 70.00, "USD"),
    ("WD Black SN770 1TB", "NVMe", 1000, "M.2", 80.00, "USD"),
    ("Crucial P3 Plus 4TB", "NVMe", 4000, "M.2", 220.00, "USD"),
    ("Kingston NV2 250GB", "NVMe", 250, "M.2", 35.00, "USD"),
    ("Sabrent Rocket 4 Plus 2TB", "NVMe", 2000, "M.2", 160.00, "USD"),
    ("Corsair MP700 1TB", "NVMe", 1000, "M.2", 130.00, "USD"),
    ("Lexar NM610 500GB", "NVMe", 500, "M.2", 50.00, "USD"),
    ("Samsung 980 250GB", "NVMe", 250, "M.2", 40.00, "USD"),
    ("WD Black SN850 500GB", "NVMe", 500, "M.2", 90.00, "USD"),
    ("Crucial P5 Plus 2TB", "NVMe", 2000, "M.2", 150.00, "USD"),
]

from data import db_session
from data.storage_devices import StorageDevices

db_session.global_init("../../db/components.db")

db_sess = db_session.create_session()
for storage in storages:
    storageDevice = StorageDevices()
    storageDevice.name = storage[0]
    storageDevice.capacity_gb = storage[2]
    storageDevice.storage_type = storage[1]
    storageDevice.price = storage[4]
    storageDevice.currency = storage[5]
    db_sess.add(storageDevice)
db_sess.commit()

db_sess = db_session.create_session()
current_storageDevices = db_sess.query(StorageDevices).all()

for current_storageDevice in current_storageDevices:
    print(current_storageDevice.name)
