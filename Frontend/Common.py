from Control import Monitor, Wr_client
from Configuration.DBmanager import DBmanager

monitor = Monitor.Monitor.__get_instance__()
db = DBmanager.get_instance()
actor = Wr_client.Actor.get_instance()

def get_plc_data():
    with monitor.__variables__ as variables:
        d = {}

