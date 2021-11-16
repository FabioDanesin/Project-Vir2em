import os
from Configuration import KeyNames
from Parser import get_parsed_data
from Logs.Logger import Logger, Filetype

connection = True
data = get_parsed_data()
path = os.path.abspath("")
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
        print("Exception:" + f)
        log.write(f"{f}")
        log.write(f"{f.__cause__}")
        log.write(f"{f.__str__()}")
        exc = True
    finally:
        if exc:
            print(FAILURE)
        else:
            print(SUCCESS)


for n in tests:
    launch_test(n)

print("Test ended")
