import os

fields = ["NAME:",
          "IP:",
          "PORT:",
          "DATABASETYPE:",
          "DATABASENAME:",
          "DATABSEPASSWORD:",
          "DATABASEIP:",
          "DATABASEPORT:",
          "DATABASEADMINNAME:",
          "DATABASEADMINPASSWORD:",
          "LOGSPATH:"]

selfpath = os.path.abspath("")
filename = "ProjectData.txt"

if not os.path.exists(os.path.join(selfpath, filename)):
    f = open(os.path.join(selfpath, filename), 'w')
    print("Warning: inputs are case sensitive.")
    for index in fields:
        c = input(fields[index])
        f.write(c)
else:
    print("Program already installed")
