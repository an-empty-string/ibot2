from Iodine import *
from BeautifulSoup import *
class Activity:
	"""
	Activity defines an 8th period activity. It does this by taking a Block
	as well as either an Activity ID or the name of an activity. Using the
	activity ID will result in faster load times, however, the name will always
	find the correct activity ID.
	"""
	def __init__(self, authObj, block, aid = None, name = None):
		"""
		Initialize the Activity. Pass in an Authenticator, Block, and either an
		activity ID or an activity name.
		"""
		if aid is None and name is None: # If we don't get one of the arguments...
			# Complain.
			raise IodineException("Error: Not enough information was passed in to get the AID.", "ERR_NO_ARGS")
		if not authObj.isAuthenticated: # If we aren't authenticated...
			# Complain.
			raise IodineException("Error: There is no usable Authenticator.", "ERR_NOT_AUTHED")
		self.bid = block.bid # Get the Block's bid
		if aid is not None: # If we got an AID...
			self.aid = aid # Set it as a class variable
			self.checkAid() # Do a sanity check, just to make sure it exists
	def checkAid(self):
		"""
		Called internally.
		"""
		url = "https://iodine.tjhsst.edu/eighth/vcp_schedule/choose/uid/" + authObj.uid + "/bids/" + self.bid  # Construct a query URL
		eighthList = ClientCookie.urlopen(url) # Open it
		eighths = eighthList.read() # Read it
		if self.aid not in eighths: # If the activity doesn't exist
			# Complain
			raise IodineException("Error: The activity ID passed in does not exist.", "ERR_NO_ACT")
		else: # Don't complain
			return True # Return True.
		return False # This should never happen
		
		
