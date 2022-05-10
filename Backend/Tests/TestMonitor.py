from Control.Monitor import Monitor
from Globals.Parser import get_parsed_data

data = get_parsed_data()

m = Monitor.get_instance()

print(m.__variables__)
for v in m.__variables__:
    print(f"{v.get_browse_name()}={v.get_value()}")

m.__del__()
