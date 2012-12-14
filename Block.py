from BeautifulSoup import *
from Iodine import *
class Block: 
	"""
	Block is a class which defines an 8th period block.
	"""
	def __init__(self, authObject, **kwargs):
		"""
		Initialize the Block. Pass in an authObject and one of these:
		bid - as an integer. This is the block ID of a block.
		or...
		a date-block pair like this:
		date = "December 14, 2012"
		block = "A"
		"""
		# Various sanity checks to make sure the programmer isn't
		# trolling us.
		if authObject.isAuthenticated is False: # If we aren't authenticated
			authObject.login() # Authenticate
		if "date" in kwargs and "block" not in kwargs: #If we're missing an argument...
			# Complain
			raise IodineException("Error: A date was passed in, but without a block.", "ERR_NO_BLOCK")
		elif "block" in kwargs and "date" not in kwargs: #If we're missing an argument...
			# Complain
			raise IodineException("Error: A block was passed in, but without a date.", "ERR_NO_DATE")
		elif "date" not in kwargs and "block" not in kwargs and "bid" not in kwargs: #If we're missing all the args...
			# Complain
			raise IodineException("Error: No arguments were passed in.", "ERR_NO_ARGS")
		elif "bid" in kwargs: # If we get a block id...
			# Don't complain
			self.bid = str(bid)
		elif "date" in kwargs and "block" in kwargs: # If we get a date...
			# Don't go to homecoming, instead...
			# Call getBidByDate
			self.date = kwargs["date"]
			self.block = kwargs["block"]
			self.getBidByDate()
		else:
			raise IodineException("Error: unknown error", "ERR_BLOCK_UNKNOWN")
	def getBidByDate(self):
		"""
		Use vcp_attendance to find the block id of a date/block combination.
		"""
		date = self.date # Set our date
		block = self.block + " block" # Set our block
		attdc = ClientCookie.urlopen("https://iodine.tjhsst.edu/eighth/vcp_attendance").read() # Grab the block list
		soup = BeautifulSoup(attdc) # Make some soup
		line = None # Set a placeholder value
		for e in soup.findAll('tr'): # For all the blocks in the table 
			found_date = e.find('td', text=date) # Find dates that match
			found_block = e.find('td', text=block) # Find blocks that match
			if found_date is not None and found_block is not None: # If we found a date AND block that match
				line = repr(e) # Get the line where it was found
		if line is not None: # If we found a block matching...
			# Process it
			line = line.split("/activity/bid/")[1].split('">')[0]
			# Store the bid
			self.bid = line
