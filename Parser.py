from typing_extensions import runtime


instance = None


class __Data__:
    def __init__(self,
                 Name="new_Controller_0",
                 Ip="192.168.250.1",
                 Port="4880",
                 DbName=None,
                 DbPsswd=None,
                 DbIp=None
                 ) -> None:
        self.__Name__: str = Name
        self.__Ip__: str = Ip
        self.__Port__: str = Port
        self.__DBname__: str = DbName
        self.__DBpsswd__: str = DbPsswd
        self.__DBip__: str = DbIp

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
        else: 
            if Attribute == "IP":
                self.__Ip__ = Value
            else:
                if Attribute == "PORT":
                    self.__Port__ = Value
                else:
                    if Attribute == "DATABASENAME":
                        self.__DBname__ = Value
                    else:
                        if Attribute == "DATABASEPASSWORD":
                            self.__DBpsswd__ = Value
                        else:
                            if Attribute == "DATABASEIP":
                                self.__DBip__ = Value
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
        



