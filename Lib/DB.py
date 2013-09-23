import Config
import MySQLdb

class DB(object):
	"""docstring for DB"""

	host = ''
	username = ''
	password = ''
	db = ''
	key = ''
	connect = None

	def __init__(self):
		super(DB, self).__init__()
		config = Config.get()
		self.host = config.get('DataBase', 'host')
		self.username = config.get('DataBase', 'username')
		self.password = config.get('DataBase', 'password')
		self.db = config.get('DataBase', 'db')
		self.key = config.get('DataBase', 'encrypt_key')
		self.connect = MySQLdb.connect(self.host, self.username, self.password, self.db)
		self.connect.autocommit(True)

	def __del__(self):
		if self.connect is not None:
			self.connect.close()

	def get_connect(self):
		return self.connect

	def execute(self, exetuple):
		cur = self.connect.cursor(MySQLdb.cursors.DictCursor)
		try:
			cur.execute(*exetuple)
		except Exception, e:
			raise e
		return cur

