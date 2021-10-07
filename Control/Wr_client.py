from Configuration.DBmanager import DBmanager
from Control import Monitor
from Logs import Logger
from Configuration.Parser import get_parsed_data
from Logs.Logger import Logger, Filetype
from opcua import ua, Node


class Actor:
    """
    Questa classe permette a un client di scrivere dati / mandare segnali ad un controllore. Mantiene gli stessi
    privilegi di lettura dati dal Monitor, con l'aggiunta di poter inviare segnali per la scrittura
    """

    def __check_login_credentials_(self, username: str, password: str):
        if self.__database__.check_credentials(username, password):
            self.__logger__.write("User " + username + " ha effettuato il login")

    def __init__(self, username, password, monitor: Monitor.Monitor = Monitor.Monitor.__get_instance__(),
                 _url=Monitor.url):

        if not self.__check_login_credentials_(username, password):
            # Lo username e la user_password data non sono validi. Si lancia un errore e la sessione è terminata
            raise PermissionError()

        parserdata = get_parsed_data()

        logs_path = parserdata.get("LOGSPATH")
        db_url = parserdata.get("DB")
        self.__logger__ = Logger(logs_path, "Actor:" + username, Filetype.SHARED)
        self.__logger__.write("Attore " + username + " ha effettuato il login con successo")
        self.__database__ = DBmanager(parserdata.get("DATABASEURL"))
        self.__username__ = username
        self.__monitor__ = monitor
        self.__parameter_nodes = []

        for a in self.get_parameters():
            canwrite = True
            try:
                # Per testare se la variabile può essere scritta si tenta di inserire il valore corrente della
                # variabile stessa. Nel caso peggiore, il permesso è negato e la variabile non è scrivibile.
                # Nel caso migliore, la variabile è scrivibile e il suo valore non cambia.
                # Non implemento questo check ulteriormente perchè ne sto cercando di migliori
                a.set_value(a.get_value())
            except Exception:
                canwrite = False
            finally:
                self.__parameter_nodes.append(
                    (
                        a.get_browse_name().Name,  # ->string: Nome della variabile
                        canwrite,  # ->bool: Se la variabile è scrivibile
                        a  # ->Node: Nodo della variabile
                    )
                )

    def __get_variable(self, name: str):
        """
            Metodo privato per l'ottentimento della variabile da scrivere. Ritorna la variabile e un booleano,
            che indica se è scrivibile o meno.
        """
        settable, v = False, None
        for a in self.__parameter_nodes:
            if a[0] == name:
                settable, v = a[1], a[2]

        return settable, v

    def get_variable(self, name):
        return self.__get_variable(name)[1]

    # TODO: TESTARE
    def set_variable(self, name, value):
        """
        Permette di settare la variabile corrispondente al valore richiesto
        :param name: Nome della variabile
        :param value: Valore desiderato
        :return: True se il valore è stato assegnato con successo, False altrimenti
        """

        def get_type_of_data(_id):
            for variant in ua.VariantType:
                if variant.value == _id:  # ua.VariantType è iterabile, non è necessario fare un if/else branch
                    return variant

        def do_set(v, node: Node):  # noqa
            uaVariant = get_type_of_data(node)
            node.set_value(ua.DataValue(ua.Variant(v, uaVariant)))

        # Esempio di scrittura che da successo: ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
        self.__logger__.write("Tentata scrittura della variabile " + name + " a " + str(value))
        rval = False
        try:
            can_set_variable, node = self.__get_variable(name)
            if can_set_variable:
                do_set(value, node)
                rval = True

                self.__logger__.write("Variabile scritta con successo")
            else:
                raise Exception()

        except Exception:
            self.__logger__.write("Variabile di sola lettura. Scrittura ignorata")

        finally:
            return rval

    def get_parameters(self):
        return self.__monitor__.__variables__
