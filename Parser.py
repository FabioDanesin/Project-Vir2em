import os

sep = os.sep
instance = None
filename = "Configuration/ProjectData.txt"
rootpath = os.path.abspath("")
filepath = rootpath + sep + filename

defaults = {
    "NAME": "new_Controller_0",
    "IP": "192.168. 1.200",
    "PORT": "4840",
    "DATABASETYPE": "postgres",
    "DATABASENAME": "postgres",
    "DATABSEPASSWORD": "linuxmanager",
    "DATABASEIP": "localhost",
    "DATABASEPORT": "5432",
    "DATABASEADMINNAME": "postgres",
    "DATABASEADMINPASSWORD": "postgres",
    "LOGSPATH": sep + "Logs"
}


class __Data__:

    def __init__(self):

        self.__data__ = {}
        with open(filepath, "r") as f:
            lines = f.readlines()
            f.close()

        for line in lines:
            split = line.split(':')
            if not split[1] == "":
                self.__data__[split[0]] = split[1].strip('\n')

        self.__data__["LOGSPATH"] = rootpath + sep + self.__data__["LOGSPATH"] + sep

    def get(self, attribute):
        try:
            return self.__data__.get(attribute)

        except KeyError as k:
            print(k.__cause__)
            print(attribute + " does not exist")

    @staticmethod
    def get_instance():
        global instance
        if instance is None:
            instance = __Data__()
        return instance


def get_parsed_data():
    if instance is None:
        return __Data__.get_instance()
    else:
        return instance