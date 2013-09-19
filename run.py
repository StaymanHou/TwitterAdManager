from TwitterAdManager import TwitterAdManager
import logging
import Lib.Config as Config

CONFIG_FILE_PATH = 'config.ini'
LOG_FILE_PATH = 'log.txt'

#################
# Setup logging #
#################
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
# create file handler which logs warning or higher
fh = logging.FileHandler(LOG_FILE_PATH)
fh.setLevel(logging.WARNING)
# create console handler with a lower log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

################
# Setup config #
################
Config.read(CONFIG_FILE_PATH)

#########
# start #
#########
TAManager = TwitterAdManager('conf.cfg')
TAManager.start()
TAManager.join()