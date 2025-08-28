from src.databases.sqlite_db.engine_sqlite_db import sqlite_engine


while True:
	device_name: str = input("Введите имя устройства > ")
	sqlite_engine.update_device_name(device_name)
	break