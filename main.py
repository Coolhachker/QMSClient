from system_info import sysinfo
import uuid

from src.tools_for_registrate_device.engine_of_registration_device import registrate_device
from src.databases.sqlite_db.engine_sqlite_db import sqlite_engine

from src.tools_for_rmq.consumer import Consumer

from configs.Hosts import Hosts


def main():
	model: str = sysinfo.sysInfo['Model']
	model = 'NONE_MODEL_NAME_DEVICE' if model is None else model

	uuid_code: str = sqlite_engine.get_uuid_from_db()
	uuid_code = str(uuid.uuid4())[:10] if uuid_code is None else uuid_code

	state: bool = False

	response = registrate_device(uuid_code, model, state)
	if response == 200:
		sqlite_engine.create_a_new_uuid(uuid_code)

	consumer = Consumer(Hosts.rmq_server)




if __name__ == '__main__':
	main()