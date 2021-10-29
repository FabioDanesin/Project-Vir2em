from Configuration.DBmanager import DBmanager, SqlDataNotFoundError

import time
begin_time = time.time()

manager = DBmanager.get_instance()

name = "Vir2em_Fabio"
password = "linuxmanager"

manager.check_credentials(name, password)
try:
    manager.__query_table__('testtable')
except SqlDataNotFoundError as s:
    print(s)

r = manager.__query_table__('users')
print(f"r = {r}")

print(f"Elapsed = {time.time() - begin_time}")
