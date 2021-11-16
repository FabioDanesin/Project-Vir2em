import os

import opcua
from opcua import Client
from typing import List

from Logs.Logger import Logger, Filetype
from Parser import get_parsed_data
from Configuration import KeyNames

parsed_data = get_parsed_data()

ip = parsed_data.get(KeyNames.ip)
port = parsed_data.get(KeyNames.port)
url_base = "opc.tcp://"
_url = url_base + ip + ":" + port

instance = None


class Monitor:
    """
        Classe per monitorare i valori all'interno del controllore. Espone metodi di sola lettura dei valori nel
        controller e non chiede richiesta di autenticazione.
    """

    def __init__(self, logfile_name="Monitor Log File"):
        """
        L'inizializzazione della classe prepara un thread separato per il polling. Tali variabili sono estraibili
        solo dalle sottoclassi.

        """

        path = parsed_data.get(KeyNames.logs)
        self.__logger__: Logger = Logger(path, logfile_name, Filetype.LOCAL)

        # Verificato che esiste un solo monitor, si procede alla connessione
        self.__client__: Client = Client(_url)
        self.__url__: str = _url

        try:
            # Connessione del client sul punto di ascolto definito dall' URL
            self.__logger__.write("Tentativo di connessione all'URL " + _url)
            self.__client__.connect()

            self.__logger__.write("Connessione avvenuta con successo")
            self.__obj_node__ = self.__client__.get_objects_node()

            # Estrazione del nome del controller
            controllername = parsed_data.get(KeyNames.controllername)
            self.__logger__.write("Estratto nome del controller: " + controllername)

            # Estrazione delle variabili di stato del controller
            self.__controller_state_variables__: List[opcua.Node] = self.__obj_node__.get_children()
            self.__variables__ = None

            # Ottenimento dei parametri dal controller
            for data in self.__controller_state_variables__:
                # Individua il nodo che contiene il nome del controller
                if data.get_browse_name().Name == controllername:

                    # Lo spazio delle GlobalVars è hardcoded con questo nome
                    for plcvars in data.get_children():
                        if plcvars.get_browse_name().Name == "GlobalVars":
                            self.__variables__: List[opcua.Node] = plcvars.get_children()

            if self.__variables__ is None:
                self.__logger__.write("Errore: nome del controller non trovato")
                raise RuntimeError()

            self.__logger__.write("Ottenute le seguenti variabili globali: ")
            for a in self.__variables__:
                self.__logger__.__write__(str(a) + "\n")

        except Exception:

            # Se a qualsiasi punto dovesse fallire il client si disconnetterà automaticamente
            self.__logger__.write("Errore di connessione")
            self.__client__.disconnect()

            raise RuntimeError()

    def get_variable_node(self, name):
        for a in self.__variables__:
            if a.get_browse_name() == name:
                return a

    @staticmethod
    def get_instance():
        global instance
        """
        Metodo esterno per ottenere l'istanza del monitor. Nota che se un istanza monitor ancora non esiste, ritornerà
        None, senza istanziarne una con parametri a sua scelta.
        :return: l'istanza di Monitor se ne esiste una, None altrimenti.
        """
        if instance is None:
            instance = Monitor()
        return instance

    def __del__(self):
        self.__client__.disconnect()
        print("Monitor disconnected")

    def __str__(self):
        return self.__name__
