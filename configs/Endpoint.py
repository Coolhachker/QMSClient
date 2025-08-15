from dataclasses import dataclass

from configs.Hosts import Hosts


@dataclass
class Endpoints:
	registration: str = 'http://'+Hosts.domain+"/registrate_device"
	download_endpoint: str = "https://spb.qms.ru:20000/download.php?ckSize=25"
	upload_endpoint: str = "https://spb.qms.ru:20000/upload.php"