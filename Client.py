import threading
import time
from opcua import Client

ip = "157.138.24.165"
port = "4840"
url = "opc.tcp://" + ip + ":" + port


class __Monitor:
    """
        Classe per monitorare i valori all'interno del controllore. Espone metodi di sola lettura dei valori nel
        controller e non chiede richiesta di autenticazione. NOTA CHE QUESTA CLASSE DEVE ESSERE ISTANZIATA UNA SOLA
        VOLTA!
    """
    # Istanze della classe monitor. La lunghezza della lista deve essere settata sempre a 1

    def __init__(self, update_time: float, _url: str = url, show_on_console: bool = True):
        """
        L'inizializzazione della classe prepara un thread separato per il polling. Tali variabili sono estraibili
        solo dalle sottoclassi.

        :param update_time: tempo di sleep del monitor prima di riaggiornare i valori
        :param _url: punto di ascolto del monitor. Si presume che un server sia già aperto sull'URL dato
        :param show_on_console: stampa i risultati a console se True
        """

        # Funzione per un thread daemon separato, esegue la lettura e il display dei valori contenuti nel controllore
        # e li stampa a console. Da verificare se serve mantenerlo così o se è possibile usare una lambda
        def polling(sleeptime):
            for d in self.__variables__:
                print("|>" + d.get_browse_name().Name + " : " + str(d.get_value()))
            time.sleep(sleeptime)

        self.__monitorinstances__ = []

        # Check eseguito per mantenere la proprietà singleton
        if len(self.__monitorinstances__) == 1:
            print("Esiste già un monitor")
            raise RuntimeError()

        # Verificato che esiste un solo monitor, si procede alla connessione
        self.__client__ = Client(_url)
        self.__url__ = _url

        try:
            # Connessione del client sul punto di ascolto definito dall' URL
            self.__client__.connect()
            self.__obj_node__ = self.__client__.get_objects_node()

            # Estrazione del nome del controller
            controllername = open("ControllerName.txt", "r").readline(30)

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
                print("Errore: controller non trovato. Il nome dato è " + controllername)
                raise RuntimeError()

        except Exception:

            # Se a qualsiasi punto dovesse fallire il client si disconnetterà automaticamente
            print("Client has failed to connect at URL " + self.__url__)
            self.__client__.disconnect()
            raise RuntimeError()

        if show_on_console:
            # TODO: verificare con ps a command line che questo thread muoia dopo la terminazione del mainthread
            t = threading.Thread(
                target=polling(update_time),
                daemon=True
            )
            t.start()
            t.join()

        self.__monitorinstances__ = [self]  # Proprietà singleton

    # def __init__(self, ip: str, port: str):
    #    self.__init__("opc.tcp://" + ip + port)

    def __str__(self):
        return self.__name__

    def __get_instance__(self):
        """
        Metodo esterno per ottenere l'istanza del monitor. Nota che se un istanza monitor ancora non esiste, ritornerà
        None, senza istanziarne una con parametri a sua scelta.
        :return: l'istanza di Monitor se ne esiste una, None altrimenti.
        """
        if len(self.__monitorinstances__) == 1 and self.__monitorinstances__[1] is not None:
            return self.__monitorinstances__[0]
        else:
            return None

    def __del__(self):
        self.__monitorinstances__ = []
        self.__client__.disconnect()


def testclassmonitor():
    __Monitor(0.5)


if __name__ == '__main__':
    testclassmonitor()
