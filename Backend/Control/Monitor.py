import opcua
from opcua import Client, Node
from typing import List

from Backend.Logs.Logger import Logger, Filetype
from Backend.Globals.Parser import get_parsed_data
from Backend.Globals import KeyNames

parsed_data = get_parsed_data()

ip = parsed_data.get(KeyNames.ip)
port = parsed_data.get(KeyNames.port)
url_base = "opc.tcp://"
_url = url_base + ip + ":" + port

instance = None


class Monitor:
    """
    Classe per monitorare i valori all'interno del controllore. Espone metodi di sola lettura dei valori nel
    controller.
    """

    def __init__(self, logfile_name="Monitor Log File"):
        path = parsed_data.get(KeyNames.logs)
        self.__logger__: Logger = Logger(path, logfile_name, Filetype.LOCAL)

        # Verificato che esiste un solo monitor, si procede alla connessione
        self.__client__: Client = Client(_url)
        self.__url__: str = _url

        try:
            # Connessione del client sul punto di ascolto definito dall' URL
            self.__logger__.write(f"Tentativo di connessione all'URL {self.__url__}")
            self.__client__.connect()

            self.__logger__.write("Connessione avvenuta con successo")
            self.__obj_node__ = self.__client__.get_objects_node()

            # Estrazione del nome del controller
            controllername = parsed_data.get(KeyNames.controllername)
            self.__logger__.write(f"Estratto nome del controller: {controllername}")

            # Estrazione delle variabili di stato del controller
            self.__controller_state_variables__: List[opcua.Node] = self.__obj_node__.get_children()

            # Setup delle variabili di controllo / shortcut per update di stato del monitor.
            self.__variables__ = None
            self.__variables_root_node__ = None
            self.__data_root__ = None

            # Ottenimento dei parametri dal controller
            for data in self.__controller_state_variables__:
                # Individua il nodo che contiene il nome del controller
                if data.get_browse_name().Name == controllername:
                    self.__data_root__ = data

                    # Lo spazio delle GlobalVars è hardcoded con questo nome
                    for plcvars in self.__data_root__.get_children():
                        if plcvars.get_browse_name().Name == "GlobalVars":
                            self.__variables_root_node__ = plcvars
                            self.__variables__: List[opcua.Node] = self.__variables_root_node__.get_children()
                            break

                if self.__variables_root_node__ is not None:
                    break

            if self.__variables__ is None:
                # Errore: Il controller non esiste sull'indirizzo passato.
                self.__logger__.write("Errore: nome del controller non trovato")
                raise RuntimeError()

            self.__logger__.write("Ottenute le seguenti variabili globali: ")
            for a in self.__variables__:
                self.__logger__.__write__(f"\t{str(a)}\n")

        except Exception:
            # Se a qualsiasi punto dovesse fallire il client si disconnetterà automaticamente
            self.__logger__.write("Errore di connessione")
            self.__client__.disconnect()

            raise RuntimeError()

    def get_variable_node(self, name: str) -> Node:
        """
        Ritorna il nodo associato a quella variabile
        :param name: Nome del nodo
        :return: Nodo
        :except RuntimeException: Il nodo richiesto non esiste.
        """
        for a in self.__variables__:
            if a.get_browse_name() == name:
                return a

        self.__logger__.write(f"ERROR: requested node{name} does not exist")
        raise RuntimeError("Requested node does not exist")

    @staticmethod
    def get_instance():
        """
        Metodo esterno per ottenere l'istanza del monitor. Nota che se un istanza monitor ancora non esiste, ritornerà
        None, senza istanziarne una con parametri a sua scelta.
        :return: l'istanza di Monitor se ne esiste una, None altrimenti.
        """

        global instance
        if instance is None:
            instance = Monitor()
        return instance

    def refresh_variables(self) -> None:
        """
        Funzione per l'update dei node presenti nel PLC.
        :return: None
        """
        self.__variables__ = self.__variables_root_node__.get_children()

    def __del__(self):
        self.__client__.disconnect()
        print("Monitor disconnected")

    def __str__(self):
        return self.__name__
