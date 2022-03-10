import threading
import time
import typing

import opcua

from opcua import Node
from Configuration import KeyNames
from Control import Monitor, Actor
from Configuration.DBmanager import DBmanager
from Parser import get_parsed_data

monitor = Monitor.Monitor.get_instance()
db = DBmanager.get_instance()
actor = Actor.Actor.get_instance()

SAMPLE_TIME = 0.01
PUSH_SLEEPTIME = 1


# def add_plc_data(data_node: opcua.Node):
#     name = data_node.get_browse_name()
#
#     if name not in plcdata.keys():
#         plcdata[name] = [data_node.get_value()]
#     else:
#         plcdata[name].append(data_node.get_value())
#
#     if len(plcdata[name]) == SAMPLE_LIST_MAXLEN:
#         avg = sum(plcdata[name]) / SAMPLE_LIST_MAXLEN
#         db.add_variable_sample(name, avg)
#         plcdata[name] = []
#         time.sleep(PUSH_SLEEPTIME)
#
#
# def updater():
#     while True:
#         for v in monitor.__variables__:
#             add_plc_data(v)
#         time.sleep(SAMPLE_TIME)
#
#
# def get_data_value_(name: str):
#     return monitor.get_variable_node(name).get_value()
#
#

class ReaderThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self.monitor = Monitor.Monitor.get_instance()

    def start(self) -> None:
        parsed_data = get_parsed_data()
        MAXSAMPLES = parsed_data.get(KeyNames.samples)

        v = self.monitor.__variables__
        plcdata = {
            node.get_browse_name(): (node, 0, None) for node in v
        }

        while True:
            self.monitor.refresh_variables()
            for row in v:
                node: Node = row[0]
                iteration: int = row[1]
                meta_data: typing.Any = row[2]

                iteration += 1
                v = node.get_value()
                if isinstance(v, (int, float, complex)):
                    meta_data += v

                elif isinstance(v, bool):
                    if v:
                        meta_data += 1

                else:
                    print("Type error")
                    print(type(v))

                if iteration == MAXSAMPLES:
                    r = (node, 0, 0)
                    plcdata[node.get_browse_name()] = r
                    db.add_variable_sample(node.get_browse_name(), meta_data)
            time.sleep(1)
