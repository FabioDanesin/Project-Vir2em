import os
import subprocess

servicepath = "/etc/systemd/system"
servicename = "OpcUa.service"
selfpath = os.path.abspath("")
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

if not os.path.exists(os.path.join(selfpath, filename)):
    f = open(os.path.join(selfpath, filename), 'w')
    print("Warning: inputs are case sensitive.")
    for index in fields:
        c = input(fields[index])
        f.write(c)
    f.close()
else:
    print("Program already installed")

if not os.path.exists(os.path.join(servicepath, servicename)):
    f = open(os.path.join(servicepath, servicename))
    print("Setting up startup service")
    f.write("[Unit]\n")
    f.write("Description=" + "<" + projectdescription + ">\n\n")
    f.write("[Service]\n")
    f.write("User=<root>\n")
    f.write("WorkingDirectory=<" + selfpath + ">\n")
    f.write("ExecStart=/bin/bash -c\n\n")
    f.write("[Install]\n")
    f.write("WantedBy=multi-user.target")
    f.close()
    bashCommand = "sudo systemctl daemon-reload"
    process = subprocess.Popen(bashCommand.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    bashCommand = "sudo systemctl enable " + servicename
    process = subprocess.Popen(bashCommand.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    process.communicate()
else:
    print("Service Already setup")
