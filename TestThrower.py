import os
import threading

from Configuration import KeyNames
from Parser import get_parsed_data
from Logs.Logger import Logger, Filetype

tests = ["DatabaseTest", "SystemTest", "TestClient", "TestLogger", "TestMonitor"]
tests = ["SystemTest"]
connection = True
data = get_parsed_data()


def launch_test(name):
    log = Logger(data.get(KeyNames.logs), f"{name}thread", Filetype.LOCAL)

    try:
        print(f"launching:{name}")
        os.system(f"python3 Tests/{name}.py")
        log.write("Test completed successfully")
    except Exception as f:
        log.write(f"{f}")
        log.write(f"{f.__cause__}")
        log.write(f"{f.__str__()}")

    finally:
        return


threads = []

for n in tests:
    t = threading.Thread(
        name=n,
        target=launch_test(n),
        daemon=True
    )
    threads.append(t)
    t.start()
    t.join()


print("Test ended")
