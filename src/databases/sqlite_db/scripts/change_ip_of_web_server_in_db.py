import re
from src.databases.sqlite_db.engine_sqlite_db import sqlite_engine


while:
	ip: str = input("Введите новый ip адрес вашего rmq сервера > ")

	if re.search(r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(:([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5]))?$", ip):
		sqlite_engine.update_ip_of_rmq_server(ip)
		break
	else:
		print("Неправильный ip адрес.")