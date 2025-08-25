from dataclasses import dataclass

from configs.Hosts import Hosts

from src.databases.sqlite_db.engine_sqlite_db import sqlite_engine


@dataclass
class Endpoints:
	registration: str = 'http://'+sqlite_engine.get_ip_of_web_server()+"/registrate_device"
	download_endpoint: str = "https://spb.qms.ru:20000/download.php?ckSize=25"
	upload_endpoint: str = "https://spb.qms.ru:20000/upload.php"