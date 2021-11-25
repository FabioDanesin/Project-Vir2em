import os
import pathlib

instance = None
filename = "Configuration/ProjectData.txt"
rootpath = pathlib.Path(__file__).parent.resolve().__str__()
filepath = os.path.join(rootpath, filename)


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

        self.__data__["LOGSPATH"] = os.path.join(rootpath, self.__data__["LOGSPATH"]) + os.sep

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
    return __Data__.get_instance()
