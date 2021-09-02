import os

instance = None


class __Data__:
    def __init__(self,
                 Name="new_Controller_0",
                 Ip="192.168.250.1",
                 Port="4880",
                 DbType='postgresql',
                 DbName=None,
                 DbPsswd=None,
                 DbIp=None,
                 Logspath=None
                 ) -> None:
        self.__Name__: str = Name
        self.__Ip__: str = Ip
        self.__Port__: str = Port
        self.__DBtype__: str = DbType
        self.__DBname__: str = DbName
        self.__DBpsswd__: str = DbPsswd
        self.__DBip__: str = DbIp
        self.__Logspath__: str = os.path.abspath(Logspath)
        self.__DB_admin_name__ = ""
        self.__DB_admin_password__ = ""

    @staticmethod
    def Data():
        global instance
        if instance is None:
            instance = __Data__()
        return instance

    def setAttribute(self, Attribute: str, Value: str):
        Attribute = Attribute.upper()

        if Attribute == "NAME":
            self.__Name__ = Value

        elif Attribute == "IP":
            self.__Ip__ = Value

        elif Attribute == "PORT":
            self.__Port__ = Value

        elif Attribute == "DATABASETYPE":
            self.__DBtype__ = Value

        elif Attribute == "DATABASENAME":
            self.__DBname__ = Value

        elif Attribute == "DATABASEPASSWORD":
            self.__DBpsswd__ = Value

        elif Attribute == "DATABASEADMINNAME":
            return self.__DB_admin_name__

        elif Attribute == "DATABASEADMINPASSWORD":
            return self.__DB_admin_password__

        elif Attribute == "DATABASEIP":
            self.__DBip__ = Value

        elif Attribute == "LOGSPATH":
            self.__Logspath__ = os.path.abspath(Attribute)

        else:
            raise RuntimeError("Unknown Parameter")

    def get(self, Attribute: str):
        if Attribute == "NAME":
            return self.__Name__

        elif Attribute == "IP":
            return self.__Ip__

        elif Attribute == "PORT":
            return self.__Port__

        elif Attribute == "DATABASETYPE":
            return self.__DBtype__

        elif Attribute == "DATABASENAME":
            return self.__DBname__

        elif Attribute == "DATABASEPASSWORD":
            return self.__DBpsswd__

        elif Attribute == "DATABASEADMINNAME":
            return self.__DB_admin_name__

        elif Attribute == "DATABASEADMINPASSWORD":
            return self.__DB_admin_password__

        elif Attribute == "DATABASEIP":
            return self.__DBip__

        elif Attribute == "LOGSPATH":
            return self.__Logspath__

        else:
            raise RuntimeError("Unknown Parameter")


def Parsing():
    f = open('ControllerName.txt', 'r')
    lines: list = []
    splitted: list = []

    info: __Data__ = __Data__.Data()

    lines: list = f.readlines()
    for i in lines:
        splitted = i.split(':')
        info.setAttribute(splitted[0], splitted[1])

    f.close()
