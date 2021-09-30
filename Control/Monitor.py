import threading
import time

from opcua import Client
from Logs.Logger import Logger, Filetype
from Configuration.Parser import get_parsed_data
from Configuration import KeyNames

parsed_data = get_parsed_data()

ip = parsed_data.get(KeyNames.ip)
port = parsed_data.get(KeyNames.port)
url_base = "opc.tcp://"
url = url_base + ip + ":" + port


class Monitor:
    """
        Classe per monitorare i valori all'interno del controllore. Espone metodi di sola lettura dei valori nel
        controller e non chiede richiesta di autenticazione. NOTA CHE QUESTA CLASSE DEVE ESSERE ISTANZIATA UNA SOLA
        VOLTA!
    """

    # Istanze della classe monitor. La lunghezza della lista deve essere settata sempre a 1

    instance = None

    def __init__(self, update_time: float = 3, _url: str = url, show_on_console: bool = True):
        """
        L'inizializzazione della classe prepara un thread separato per il polling. Tali variabili sono estraibili
        solo dalle sottoclassi.

        :param update_time: tempo di sleep del monitor prima di riaggiornare i valori
        :param _url: punto di ascolto del monitor. Si presume che un server sia già aperto sull'URL dato
        :param show_on_console: stampa i risultati a console se True
        """

        # Funzione per un thread daemon separato, esegue la lettura e il display dei valori contenuti nel controllore
        # e li stampa a console.
        def polling(sleeptime):
            while True:
                for d in self.__variables__:
                    print("|>" + d.get_browse_name().Name + " : " + str(d.get_value()))
                time.sleep(sleeptime)

        path = parsed_data.get(KeyNames.logs)
        self.__logger__ = Logger(path, "Monitor Log File", Filetype.LOCAL)

        self.instance = None

        # Check eseguito per mantenere la proprietà singleton
        if self.instance is not None:
            self.__logger__.write("Un altra istanza di monitor è già presente nel sistema")
            raise RuntimeError("Un altra istanza di monitor è già presente nel sistema")

        # Verificato che esiste un solo monitor, si procede alla connessione
        self.__client__ = Client(_url)
        self.__url__ = _url

        try:
            # Connessione del client sul punto di ascolto definito dall' URL
            self.__logger__.write("Tentativo di connessione all'URL " + _url)
            self.__client__.connect()

            self.__logger__.write("Connessione avvenuta con successo")
            self.__obj_node__ = self.__client__.get_objects_node()

            # Estrazione del nome del controller
            controllername = open("../Configuration/ProjectData.txt", "r").readline(30).split(":")[1].strip("\n") # TODO: riscrivi
            self.__logger__.write("Estratto nome del controller: " + controllername)

            # Estrazione delle variabili di stato del controller
            self.__controller_state_variables__ = self.__obj_node__.get_children()
            self.__variables__ = None

            # Ottenimento dei parametri dal controller
            for data in self.__controller_state_variables__:
                # Individua il nodo che contiene il nome del controller
                if data.get_browse_name().Name == controllername:

                    # Lo spazio delle GlobalVars è hardcoded con questo nome
                    for plcvars in data.get_children():
                        if plcvars.get_browse_name().Name == "GlobalVars":
                            self.__variables__ = plcvars.get_children()

            if self.__variables__ is None:
                self.__logger__.write("Errore: nome del controller non trovato")
                raise RuntimeError()

            self.__logger__.write("Ottenute le seguenti variabili globali: ")
            for a in self.__variables__:
                self.__logger__.__write__(str(a) + "\n")

        except Exception:

            # Se a qualsiasi punto dovesse fallire il client si disconnetterà automaticamente
            self.__logger__.write("Errore di connessione all'database_url " + self.__url__)
            self.__client__.close_session()
            self.__client__.disconnect()

            raise RuntimeError()

        if show_on_console:
            # Start del thread per il pinging automatico del server
            t = threading.Thread(
                name="Poller",
                target=polling(update_time),  # Impossibile metterci una lambda dentro :(
                daemon=True
            )
            t.start()
            t.join()

        self.instance = self  # Proprietà singleton

    @staticmethod
    def __get_instance__():
        """
        Metodo esterno per ottenere l'istanza del monitor. Nota che se un istanza monitor ancora non esiste, ritornerà
        None, senza istanziarne una con parametri a sua scelta.
        :return: l'istanza di Monitor se ne esiste una, None altrimenti.
        """
        if Monitor.instance is None:
            Monitor()
        return Monitor.instance

    def __del__(self):
        self.__logger__.write("END LOG")
        del self.__logger__
        self.instance = None
        self.__client__.disconnect()

    def __str__(self):
        return self.__name__
