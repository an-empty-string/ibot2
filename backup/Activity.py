from Iodine import *
from string import *
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
		self.authObj = authObj
		self.url = "https://iodine.tjhsst.edu/eighth/vcp_schedule/choose/uid/" + authObj.uid + "/bids/" + self.bid
		if aid is not None: # If we got an AID...
			self.aid = aid # Set it as a class variable
			self.checkAid() # Do a sanity check, just to make sure it exists
		else:
			self.name = name
			self.getAidFromName()
	def getAidFromName(self):
		name = self.name # Fetch the name of the activity
		url = self.url # Fetch the URL
		soup = BeautifulSoup(ClientCookie.urlopen(url).read()) # Make some soup
		x = [str(i).lower() for i in soup.findAll("div")]
		matchingActs = []
		for i in x:
			if name.lower() in i:
				matchingActs.append(i)
		if len(matchingActs) is 0:
			raise IodineException("Error: no matching activities found.", "ERR_NO_ACTS")
		self.aid = matchingActs[-3].split('data-aid="')[1].split('" data-room')[0]
	def signUpFor(self):
		bid = self.bid
		query = "https://iodine.tjhsst.edu/eighth/vcp_schedule/change/uid/" + self.authObj.uid + "/bids/" + self.bid + "?aid=" + self.aid
		print ClientCookie.urlopen(query).read()
	def checkAid(self):
		"""
		Called internally.
		"""
		# Construct a query URL
		url = self.url
		eighthList = ClientCookie.urlopen(url) # Open it
		eighths = eighthList.read() # Read it
		if self.aid not in eighths: # If the activity doesn't exist
			# Complain
			raise IodineException("Error: The activity ID passed in does not exist.", "ERR_NO_ACT")
		else: # Don't complain
			return True # Return True.
		return False # This should never happen
		
		
