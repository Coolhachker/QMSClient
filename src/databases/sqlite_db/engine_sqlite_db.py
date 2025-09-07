import sqlite3
import uuid

from logging import getLogger

from dataclasses import dataclass


@dataclass
class ConnectionAndCursor:
	connection: sqlite3.Connection
	cursor: sqlite3.Cursor


def get_connection_to_db(func):
	def wrapped_function(*args, **kwargs):
		if "connection_object" not in kwargs:
			with sqlite3.connect('data/db/db.sqlite') as connection:
				cursor = connection.cursor()
				connection_object = ConnectionAndCursor(connection, cursor)
				kwargs['connection_object'] = connection_object
				return func(*args, **kwargs)
		else:
			return func(*args **kwargs)
	return wrapped_function


class SQLiteDB:
	def __init__(self):
		self.make_tables()

	@get_connection_to_db
	def make_tables(self, connection_object: ConnectionAndCursor = None):
		connection_object.cursor.execute("CREATE TABLE IF NOT EXISTS uuid_of_device(uuid_code VARCHAR(10) PRIMARY KEY)")
		connection_object.cursor.execute("CREATE TABLE IF NOT EXISTS configs(ip_of_web_server VARCHAR(25) NOT NULL DEFAULT '127.0.0.1:8080', ip_of_rabbitmq_server VARCHAR(15) NOT NULL DEFAULT '127.0.0.1', device_name VARCHAR(20) NOT NULL DEFAULT 'NONE_NAME_DEVICE', duration TINYINT NOT NULL DEFAULT 15)")
		connection_object.cursor.execute("CREATE TABLE IF NOT EXISTS status_connection_to_rmq_server(status BOOL NOT NULL DEFAULT FALSE)")

		connection_object.cursor.execute("SELECT COUNT(*) FROM configs")
		if connection_object.cursor.fetchone()[0] == 0:
			connection_object.cursor.execute("INSERT INTO configs DEFAULT VALUES")
		connection_object.cursor.execute("SELECT COUNT(*) FROM status_connection_to_rmq_server")
		if connection_object.cursor.fetchone()[0] == 0:
			connection_object.cursor.execute("INSERT INTO configs DEFAULT VALUES")
		connection_object.connection.commit()

	@get_connection_to_db
	def create_a_new_uuid(self, uuid_code: str, connection_object: ConnectionAndCursor = None):
		try:
			connection_object.cursor.execute("INSERT INTO uuid_of_device ('uuid_code') VALUES (?)", (uuid_code, ))
			connection_object.connection.commit()
		except sqlite3.IntegrityError:
			pass

	@get_connection_to_db
	def get_uuid_from_db(self, connection_object: ConnectionAndCursor = None) -> None | str:
		connection_object.cursor.execute("SELECT uuid_code FROM uuid_of_device")
		result = connection_object.cursor.fetchone()

		if result is None:
			return None

		return result[0]

	@get_connection_to_db
	def get_ip_of_web_server(self, connection_object: ConnectionAndCursor = None):
		connection_object.cursor.execute("SELECT ip_of_web_server FROM configs")
		return connection_object.cursor.fetchone()[0]

	@get_connection_to_db
	def get_ip_of_rmq_sever(self, connection_object: ConnectionAndCursor = None):
		connection_object.cursor.execute("SELECT ip_of_rabbitmq_server FROM configs")
		return connection_object.cursor.fetchone()[0]

	@get_connection_to_db
	def update_ip_of_web_server(self, ip: str, connection_object: ConnectionAndCursor = None):
		connection_object.cursor.execute("UPDATE configs SET ip_of_web_server=?", (ip, ))
		connection_object.connection.commit()

	@get_connection_to_db
	def update_ip_of_rmq_server(self, ip: str, connection_object: ConnectionAndCursor = None):
		connection_object.cursor.execute("UPDATE configs SET ip_of_rabbitmq_server=?", (ip, ))
		connection_object.connection.commit()

	@get_connection_to_db
	def update_device_name(self, device_name: str, connection_object: ConnectionAndCursor = None):
		connection_object.cursor.execute("UPDATE configs SET device_name = ?", (device_name, ))
		connection_object.connection.commit()

	@get_connection_to_db
	def get_device_name(self, connection_object: ConnectionAndCursor = None):
		connection_object.cursor.execute("SELECT device_name FROM configs")
		return connection_object.cursor.fetchone()[0]

	@get_connection_to_db
	def get_duration(self, connection_object: ConnectionAndCursor = None):
		connection_object.cursor.execute("SELECT duration FROM configs")
		return connection_object.cursor.fetchone()[0]

	@get_connection_to_db
	def get_status_of_connection_to_rmq_server(self, connection_object: ConnectionAndCursor = None):
		connection_object.cursor.execute("SELECT status FROM status_connection_to_rmq_server")
		return connection_object.cursor.fetchone()[0]

	@get_connection_to_db
	def update_status_of_connection_to_rmq_server(self, status: bool, connection_object: ConnectionAndCursor = None):
		connection_object.cursor.execute("UPDATE status_connection_to_rmq_server SET status = ?", (status, ))
		connection_object.connection.commit()

sqlite_engine = SQLiteDB()