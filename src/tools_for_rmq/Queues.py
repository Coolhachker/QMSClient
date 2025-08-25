from dataclasses import dataclass


@dataclass
class Queues:
	qms_queue: str = 'qms_queue'
	callback_queue: str = 'qms_callback_queue'
	ping_pong_queue: str = 'ping_pong_queue'