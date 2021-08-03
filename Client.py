import threading
import time
from opcua import Client

ip = "157.138.24.165"
port = "4840"
url = "opc.tcp://" + ip + ":" + port

# Istanze della classe monitor. La lunghezza della lista deve essere settata sempre a 1
__monitorinstances__ = []


class __Monitor:
    """
        Classe per monitorare i valori all'interno del controllore. Espone metodi di sola lettura dei valori nel
        controller e non chiede richiesta di autenticazione. NOTA CHE QUESTA CLASSE DEVE ESSERE ISTANZIATA UNA SOLA
        VOLTA!
    """
    __exists__ = False

    def __init__(self, update_time: float, _url: str = url, show_on_console: bool = True):
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
            for data in self.__parameters__:
                print("|>" + data.get_browse_name().Name + " : " + str(data.get_value()))
            time.sleep(sleeptime)

        # Check eseguito per mantenere la proprietà singleton
        if len(__monitorinstances__) == 1:
            print("Esiste già un monitor")
            raise RuntimeError()

        # Verificato che esiste un solo monitor, si procede alla connessione
        self.__client__ = Client(_url)
        self.__url__ = _url

        try:
            # Connessione del client sul punto di ascolto definito dall' URL
            self.__client__.connect()
            # Ottenimento dei parametri dal controller
            self.__parameters__ = self.__client__.get_objects_node().get_children()[1].get_children()[1].get_children()
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

        Client.__monitorinstances__ = [self]  # Proprietà singleton

    # def __init__(self, ip: str, port: str):
    #    self.__init__("opc.tcp://" + ip + port)

    def __str__(self):
        return self.__name__

    @staticmethod
    def __get_instance__():
        """
        Metodo esterno per ottenere l'istanza del monitor. Nota che se un istanza monitor ancora non esiste, ritornerà
        None, senza istanziarne una con parametri a sua scelta.
        :return: l'istanza di Monitor se ne esiste una, None altrimenti.
        """
        if len(__monitorinstances__) == 1:
            return __monitorinstances__[0]
        else:
            return None


"""
def monitor():
    client = Client(url)
    client.connect()
    try:
        obj_node = client.get_objects_node()
        children = obj_node.get_children()
        params = children[1].get_children()[1].get_children()
        while True:
            print("---------------------------------------------------------------------------------------------------")
            for data in params:
                print("|>" + data.get_browse_name().Name + ":" + str(data.get_value()))
            print("---------------------------------------------------------------------------------------------------")

            time.sleep(1)

    except Exception:
        print("Exception thrown")
        traceback.print_exc()

    finally:
        client.disconnect()
"""


def testclassmonitor():
    __Monitor(0.5)


if __name__ == '__main__':
    testclassmonitor()
