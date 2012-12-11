import ClientCookie
import urllib2
class Authenticator:
	def __init__(self, username, password):
		self.username = username
		self.password = password
	def login(self):
		usernameKey = 'login_username'
		passwordKey = 'login_password'
		loginUrl = "https://iodine.tjhsst.edu"
		loginInformation = {usernameKey: self.username, passwordKey: self.password}
		loginRequest = urllib2.Request(loginUrl, loginInformation)
		loginResponse = ClientCookie.urlopen(loginRequest)
		return loginResponse

