from Backend.Configuration.DBmanager import DBmanager, SqlDataNotFoundError

import time
begin_time = time.time()

manager = DBmanager.get_instance()

name = "Vir2em_Fabio"
password = "linuxmanager"

try:
    manager.check_credentials(name)
except SqlDataNotFoundError as s:
    print(s)

manager.add_variable_sample("testvariable", 21)
data = manager.select_all_in_table("testvariable")
print(f"Select on tabletest={data}")
