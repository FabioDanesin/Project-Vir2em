import os

servicepath = "/etc/systemd/system"
servicename = "OpcUa.service"
selfpath = pathlib.Path(__file__).parent.resolve().__str__()
filename = "ProjectData.txt"
projectdescription = ""

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


def installationf():
    if not os.path.exists(os.path.join(selfpath, filename)):
        f = open(os.path.join(selfpath, filename), 'w')
        print("Warning: inputs are case sensitive.")
        for index in fields:
            c = input(fields[index])
            f.write(c)
        f.close()
    else:
        print("Program already installed")
