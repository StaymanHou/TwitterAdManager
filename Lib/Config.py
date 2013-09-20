from ConfigParser import ConfigParser

__Config = None

def read(config_file_path):
	global __Config
	__Config = ConfigParser()
	try:
		__Config.read(config_file_path)
	except Exception, e:
		raise e

def get():
	global __Config
	return __Config