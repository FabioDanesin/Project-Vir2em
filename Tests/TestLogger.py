from Control import Logger, Parser, KeyNames

data = Parser.get_parsed_data()

path = data.get(KeyNames.logs)
name = "TESTLOG"
filetype = Logger.Filetype.LOCAL

logger = Logger.Logger(path, name, filetype)

logger.write("WRITE TEST")
print("DONE")
del logger

exit(1)
