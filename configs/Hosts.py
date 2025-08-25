from dataclasses import dataclass


@dataclass
class Hosts:
	domain: str = '127.0.0.1:8080'
	rmq_server: str = '127.0.0.1'
