import requests

from configs.Endpoint import Endpoints
from configs.Exceptions import UnSuccessRegestration



def registrate_device(uuid_code: str, device_name: str, status: bool):
	try:
		response = requests.post(
			Endpoints.registration, 
				json={'device_id': uuid_code, "device_name": device_name, "device_status": 'on' if status else 'off'}
			)
	except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout):
		raise UnSuccessRegestration('Невозможно подключиться к сервису регистрации.')
	return response.status_code