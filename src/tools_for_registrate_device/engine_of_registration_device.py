import requests

from configs.Endpoint import Endpoints



def registrate_device(uuid_code: str, device_name: str, status: bool):
	response = requests.post(
		Endpoints.registration, 
			json={'device_id': uuid_code, "device_name": device_name, "device_status": 'on' if status else 'off'}
		)
	return response.status_code