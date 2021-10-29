import threading

import Configuration.DBmanager
import Control.Monitor as Monitor
from Control.Wr_client import Actor
from Logs.Logger import Logger

logvars = "logvars"


def do_test(log_mainthread: Logger, act: Actor):
    try:

        var_name = "Reset"
        try:
            log_mainthread.write("Begin test")
        except UnboundLocalError as ul_err:
            print("Error. Logger = None")
            print(f"{ul_err} : causa = {ul_err.__cause__}")
            raise RuntimeError()
        print("Actor and monitor created")
        reset = act.get_variable(var_name)
        print(f"Fetched value from reset = {reset}")
        log_mainthread.write(f"Valore della variabile reset = {reset}")
        log_mainthread.write(f"Tento scrittura a {not reset}")
        print(threading.current_thread().name)
        try:
            print("Writing...")
            act.set_variable(var_name, not act.get_variable(var_name))
            print("||DONE||")
        except Exception as bp_err:
            log_mainthread.write(f"{bp_err}: {(bp_err.__cause__.__str__())}")
        finally:
            print("Deleting " + log_mainthread.__str__())
            del log_mainthread
            del act
            print("Act is deded")

    except Exception as f:
        log_mainthread.write("Caught exception")
        log_mainthread.write(f"{f} , cause = {f.__cause__}")
        exit(112313)

    finally:

        print("exited multilevel try-catch")

monitor = Monitor.Monitor.__get_instance__()

r = Configuration.DBmanager.DBmanager.get_instance()

_act = Actor("Vir2em_Fabio", "linuxmanager")

lg = Logger(__file__, logvars)

t = threading.Thread(
    name="SystemTest",
    target=lambda: do_test(lg, _act),
    daemon=True,
)

t.start()
t.join()
del _act
# monitor.__client__.disconnect()
print("Deleted Monitor")
