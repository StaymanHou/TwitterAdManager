from Lib.TwitterAdAnalyzer import WriteENGPHVerseUser, WriteENGPHVerseIntst
import Lib.Config as Config

CONFIG_FILE_PATH = 'config.ini'

Config.read(CONFIG_FILE_PATH)

fi_id = raw_input('Please enter the FI_ID of the account you want to analyze:\n')

WriteENGPHVerseUser(fi_id)
WriteENGPHVerseIntst(fi_id)