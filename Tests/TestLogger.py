from Configuration import KeyNames
import Parser
from Logs import Logger

data = Parser.get_parsed_data()

path = '/'
name = "TESTLOG"
filetype = Logger.Filetype.LOCAL

logger = Logger.Logger(path, name, filetype)

logger.write("WRITE TEST")
print("DONE")
del logger

exit(1)
