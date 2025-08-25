class UnSuccessRegestration(Exception):
	def __init__(self, message):
		super().__init__(message)

class UnSuccessConnectionToRMQServer(Exception):
	def __init__(self, message):
		super().__init__(message)