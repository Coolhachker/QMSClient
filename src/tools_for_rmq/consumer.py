import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

import json
import time
from typing import Optional

from src.tools_for_rmq.Queues import Queues
from src.tools_for_rmq.Tasks import Tasks
from src.databases.sqlite_db.engine_sqlite_db import sqlite_engine
from src.tools_for_qms_test.qms_test_engine import qms_test_engine

from configs.Exceptions import UnSuccessConnectionToRMQServer


class Consumer:
	def __init__(self, host):
		self.parameters = pika.ConnectionParameters(heartbeat=0, host=host)
		self.connection: Optional[pika.BlockingConnection] = None

		self.set_connection_to_rmq_server()

		self.channel = self.connection.channel()

		self.queue = Queues.qms_queue
		self.queue_callback = Queues.callback_queue
		self.exchange = ''

		self.declare_queue()
		self.consume()

	def declare_queue(self):
		self.channel.queue_declare(queue=self.queue, durable=True)
		self.channel.queue_declare(queue=self.queue_callback, durable=True)

	def consume(self):
		self.channel.basic_qos(prefetch_count=25)
		self.channel.basic_consume(queue=self.queue, on_message_callback=self.confirm_the_request)

		properties = pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent)

	def confirm_the_request(self, channel: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
		message = json.loads(body.decode())
		result: str = None
		device_id = sqlite_engine.get_uuid_from_db()
		try:
			assert device_id == message['device_id']
			if message['task'] == Tasks.task_net_test:
				# result = {'response': 2, 'message': 'Выполняю задачу...', 'device_id': sqlite_engine.get_uuid_from_db()}
				# channel.basic_publish(
				# 	exchange=self.exchange,
				# 	routing_key=properties.reply_to,
				# 	body=str(json.dumps(result, ensure_ascii=False)).encode(),
				# )

				test_result = qms_test_engine.start_test()

				result = {'response': 5, 'message': 'Успешно выполнил задачу.', 'data': test_result, 'device_id': sqlite_engine.get_uuid_from_db()}
				self.basic_publish(properties, channel, method, result)

			elif message['task'] == Tasks.task_check_device:
				result = {'response': 3, 'message': 'Устройство работает.', 'device_id': device_id}
				self.basic_publish(properties, channel, method, result)
		except AssertionError:
			# result = {'response': 1, 'message': 'Получил сообщение. Отправляю ответ обратно серверу.', 'device_id': device_id}
			pass

	def set_connection_to_rmq_server(self):
		try:
			self.connection = pika.BlockingConnection(self.parameters)
		except pika.exceptions.AMQPConnectionError as ex:
			print(ex)
			raise UnSuccessConnectionToRMQServer("Невозможно подключиться к RMQ серверу.")

	def basic_publish(self, properties, channel, method, result):
		print(f"DEVICE_ID: {sqlite_engine.get_uuid_from_db()} - result : {result}")
		channel.basic_publish(
			exchange=self.exchange,
			routing_key=properties.reply_to,
			body=str(json.dumps(result, ensure_ascii=False)).encode(),
		)
		channel.basic_ack(delivery_tag=method.delivery_tag)