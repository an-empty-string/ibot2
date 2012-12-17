import ClientCookie
import urllib
import urllib2
from Iodine import *
class Authenticator:
	"""
	Authenticator is a class which interfaces with the Iodine authentication
	system. It submits an HTTPS POST request containing a username and
	password. Iodine then returns a PHP session ID cookie, which the
	ClientCookie module stores and passes to other components of the Iodine
	API. Methods contained in this class are the __init__ method and the 
	login method.
	"""
	def __init__(self, username, password):
		"""
		Initialize the Authenticator. Takes a username and password, which
		are stored as class variables. This method does not actually log in
		the username in question.
		"""
		self.username = username # Defines the username that the login method will use
		self.password = password # Defines the password that the login method will use
		self.isAuthenticated = False # Are we authenticated yet?
	def login(self):
		"""
		Perform the actual login. This method takes the username and password
		passed in when the class was initialized. It then creates a dictionary
		with login information. This dictionary is passed into urllib2 to create
		a Request, which is then passed to ClientCookie.urlopen. This method
		returns a loginResponse, which is the source code from the default
		Iodine module.
		"""
		try: # Just in case we're trying to run without an Internet connection or something
			usernameKey = 'login_username' # Defines the username field name
			passwordKey = 'login_password' # Defines the password field name
			loginUrl = "https://iodine.tjhsst.edu" # Defines the URL that the request will use
			loginInformation = {usernameKey: self.username, passwordKey: self.password} # Creates a request dictionary
			loginInformation = urllib.urlencode(loginInformation) # Encode the login information.
			loginRequest = urllib2.Request(loginUrl, loginInformation) # Creates a Request that is used to login
			loginResponse = ClientCookie.urlopen(loginRequest) # Sends the login to Iodine and stores the PHP session ID.
			loginResponse = loginResponse.read() # Get the HTML/XML from Iodine.
			webpage = BeautifulSoup(loginResponse) # Set up a Beautiful Soup object
			eighthChangeUrl = webpage.find(id="menu_eighth")['href'] # Grab the eighth period change URL
			uid = eighthChangeUrl.split("uid/")[1] # Get the UID based on the eighth period change URL
			self.uid = uid # And set the uid as a class variable, effectively getting the UID for changing things
			self.isAuthenticated = True # Yes, yes we are logged in.
			return True # Yay, no error!
		except Exception, e: # If we failed for whatever reason...
			self.uid = None # Set the uid to none.
			self.isAuthenticated = False # No, no we are not.
			print e
			raise Exception("Error in Authenticator: could not log in.") # Raise an exception.
