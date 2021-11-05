import Control.Monitor
from Control.Wr_client import Actor
from Parser import get_parsed_data
from Configuration import KeyNames

data = get_parsed_data()

name = data.get(KeyNames.db_admin_name)
password = data.get(KeyNames.db_admin_password)

actor = Actor(password)
if actor.set_variable("Reset", False):
    print("Variabile settata con successo :) ")
    print("ecco delle tette : (.)(.)")
else:
    print("Variabile non settata")

Control.Monitor.Monitor.__get_instance__().__client__.disconnect()
