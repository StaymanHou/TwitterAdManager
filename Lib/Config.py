"""A singleton which serves the whole program for getting configurations"""

from ConfigParser import ConfigParser

__Config = None

def read(config_file_path):
	"""Initially set the singleton ConfigParser onto the config_file_path.
	"""
	global __Config
	__Config = ConfigParser()
	try:
		__Config.read(config_file_path)
	except Exception, e:
		raise e

def get():
	"""Return a :class:`ConfigParser.ConfigParser` object.
	"""
	global __Config
	return __Config