import os
import threading
from Control.Monitor import Monitor
from Control.Wr_client import Actor
from Logs.Logger import Logger

tests = ["DatabaseTest", "SystemTest", "TestServer", "TestClient", "TestLogger", "TestMonitor"]
connection = True

monitor =

def launch_test(name):
    try:
        print(f"launching:{name}")
        os.system(f"Tests/{name}.py")
    except Exception as f:
        print(f"{name} threw exception: {f}")


for n in tests:
    t = threading.Thread(
        name=n,
        target=launch_test(n),
        daemon=True
    )



