import os

sep = os.sep
instance = None
filename = "ProjectData.txt"
rootpath = os.path.abspath("../")
filepath = rootpath + sep + "Configuration" + sep + filename


class __Data__:

    def __init__(self):

        self.__data__ = {}
        with open(filepath, "r") as f:
            lines = f.readlines()
            f.close()

        for line in lines:
            split = line.split(':')
            self.__data__[split[0]] = split[1].strip('\n')

        self.__data__["LOGSPATH"] = rootpath + sep + self.__data__["LOGSPATH"] + sep

    def get(self, Attribute):
        try:
            return self.__data__.get(Attribute)

        except KeyError as k:
            print(k.__cause__)
            print(Attribute + " does not exist")

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
