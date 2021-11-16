import threading
import time
import opcua

from Control import Monitor, Actor
from Configuration.DBmanager import DBmanager

monitor = Monitor.Monitor.get_instance()
db = DBmanager.get_instance()
actor = Actor.Actor.get_instance()

SAMPLE_TIME = 0.01
SAMPLE_LIST_MAXLEN = 100
PUSH_SLEEPTIME = 1
plcdata = {}


def add_plc_data(data_node: opcua.Node):
    name = data_node.get_browse_name()

    if name not in plcdata.keys():
        plcdata[name] = [data_node.get_value()]
    else:
        plcdata[name].append(data_node.get_value())

    if len(plcdata[name]) == SAMPLE_LIST_MAXLEN:
        avg = sum(plcdata[name]) / SAMPLE_LIST_MAXLEN
        db.add_variable_sample(name, avg)
        plcdata[name] = []
        time.sleep(PUSH_SLEEPTIME)


def updater():
    while True:
        for v in monitor.__variables__:
            add_plc_data(v)
        time.sleep(SAMPLE_TIME)


def get_data_value_(name: str):
    return monitor.get_variable_node(name).get_value()


t = threading.Thread(target=updater, daemon=True)
t.start()
t.join()
