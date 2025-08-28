from system_info import sysinfo
import uuid

from src.tools_for_registrate_device.engine_of_registration_device import registrate_device
from src.databases.sqlite_db.engine_sqlite_db import sqlite_engine

from src.tools_for_rmq.consumer import Consumer
from src.Mobile_App.engine_of_mobile_app import ConfigApp


def main():
	model: str = sqlite_engine.get_device_name()

	uuid_code: str = sqlite_engine.get_uuid_from_db()
	uuid_code = str(uuid.uuid4())[:10] if uuid_code is None else uuid_code

	state: bool = False

	response = registrate_device(uuid_code, model, state)
	if response == 200:
		sqlite_engine.create_a_new_uuid(uuid_code)

	consumer = Consumer(sqlite_engine.get_ip_of_rmq_sever())




if __name__ == '__main__':
	ConfigApp(main).run()