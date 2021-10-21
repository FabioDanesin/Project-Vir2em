from Parser import get_parsed_data
from Configuration import KeyNames
from Control.Monitor import Monitor
from Control.Wr_client import Actor
from Logs.Logger import Logger
logvars = "logvars"

try:
    parsed_data = get_parsed_data()
    ip = parsed_data.get(KeyNames.ip)
    port = parsed_data.get(KeyNames.port)
    url_base = "opc.tcp://157.138.24.165:4840"

    log_mainthread = Logger(__file__, logvars)

    mon = Monitor(_url=url_base)
    act = Actor("Vir2em_Fabio", "linuxmanager")

    blu = act.get_variable("LED_Blue")
    log_mainthread.write(blu)
    log_mainthread.write("VARIABILE LETTA. Tento il settaggio")
    act.set_variable("LED_Blue", False)
    log_mainthread.write("Settato. Valore attuale : " + act.get_variable("LED_Blue"))
    log_mainthread.write("DONE")
    del log_mainthread
    mon.__client__.disconnect()

except:
    mon.__client__.disconnect()  # disc
    exit(112313)
