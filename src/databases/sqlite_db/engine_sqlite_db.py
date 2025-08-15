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


sqlite_engine = SQLiteDB()