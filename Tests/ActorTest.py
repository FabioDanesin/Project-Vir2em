from Control.Actor import Actor
from Configuration.DBmanager import DBmanager
RESET = 'Reset'
NAME = "Vir2em_Fabio"
PW = "linuxmanager"
manager = DBmanager.get_instance()

print("Begin system test")

manager.check_credentials(NAME)
actor = Actor.get_instance()
names = actor.get_variable_names()
print(f"PLC variable names={names}")
resetvalue = actor.get_variable(RESET)
print(resetvalue)
actor.set_variable(RESET, not resetvalue)

actor.__monitor__.__del__()
del actor

