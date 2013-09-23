import requests

class TwitterSession(object):
	"""docstring for TwitterSession"""

	account = None
	session = None
	is_login = False

	def __init__(self, account):
		super(TwitterSession, self).__init__()
		self.account = account
		self.session = requests.Session()

	def login(self):
		self.is_login = True
		