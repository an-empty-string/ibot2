class IodineException(Exception):
	"""
	IodineException is a default error class for the Iodine API. It should
	be raised for all errors in the API.
	"""
	def __init__(self, message, info = ""):
		"""
		Initialize an IodineException.
		"""
		Exception.__init__(self, message) # Call Exception's init
		self.info = info # Set self.info to what was passed in
