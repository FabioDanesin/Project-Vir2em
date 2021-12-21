import os
import pathlib

from Configuration import KeyNames
from Parser import get_parsed_data
from Logs.Logger import Logger, Filetype

connection = True
data = get_parsed_data()
path = pathlib.Path(__file__).parent.resolve().__str__()
tests = os.listdir(path + "/Tests")
print(tests)


def launch_test(name):
    log = Logger(data.get(KeyNames.logs), f"{name} thread", Filetype.LOCAL)
    exc = False
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    try:
        print(f"launching:{name}")
        os.system(f"python3 Tests/{name}")
        log.write("Test completed successfully")
    except Exception as f:
        fstr = str(f)
        print("Exception:" + fstr)
        log.write(f"{fstr}")
        log.write(f"{f.__cause__}")
        exc = True
    finally:
        if exc:
            print(FAILURE)
        else:
            print(SUCCESS)


for n in tests:
    launch_test(n)

print("Test ended")
