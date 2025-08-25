import sqlite3
import uuid

from logging import getLogger

connection = sqlite3.connect('data/db/db.sqlite')


class SQLiteDB:
	def __init__(self):
		self.cursor = connection.cursor()
		self.make_tables()

	def make_tables(self):
		self.cursor.execute("CREATE TABLE IF NOT EXISTS uuid_of_device(uuid_code VARCHAR(10) PRIMARY KEY)")
		self.cursor.execute("CREATE TABLE IF NOT EXISTS configs(ip_of_web_server VARCHAR(25) NOT NULL DEFAULT '127.0.0.1:8080', ip_of_rabbitmq_server VARCHAR(15) NOT NULL DEFAULT '127.0.0.1')")

		self.cursor.execute("SELECT COUNT(*) FROM configs")
		if self.cursor.fetchone()[0] == 0:
			self.cursor.execute("INSERT INTO configs DEFAULT VALUES")
		connection.commit()

	def create_a_new_uuid(self, uuid_code: str):
		try:
			self.cursor.execute("INSERT INTO uuid_of_device ('uuid_code') VALUES (?)", (uuid_code, ))
			connection.commit()
		except sqlite3.IntegrityError:
			pass

	def get_uuid_from_db(self) -> None | str:
		self.cursor.execute("SELECT uuid_code FROM uuid_of_device")
		result = self.cursor.fetchone()

		if result is None:
			return None

		return result[0]

	def get_ip_of_web_server(self):
		self.cursor.execute("SELECT ip_of_web_server FROM configs")
		return self.cursor.fetchone()[0]

	def get_ip_of_rmq_sever(self):
		self.cursor.execute("SELECT ip_of_rabbitmq_server FROM configs")
		return self.cursor.fetchone()[0]


sqlite_engine = SQLiteDB()