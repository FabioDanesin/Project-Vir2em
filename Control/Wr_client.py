from Control import Monitor
from opcua import ua, Node

instance = None


class Actor:
    """
    Questa classe permette a un client di scrivere dati / mandare segnali ad un controllore. Mantiene gli stessi
    privilegi di lettura dati dal Monitor, con l'aggiunta di poter inviare segnali per la scrittura
    """

    def __init__(self, monitor: Monitor.Monitor = Monitor.Monitor.__get_instance__()):

        self.__monitor__ = monitor
        self.__parameter_nodes__ = []

        for a in monitor.__variables__:
            canwrite = True
            try:
                # Per testare se la variabile può essere scritta si tenta di inserire il valore corrente della
                # variabile stessa. Nel caso peggiore, il permesso è negato e la variabile non è scrivibile.
                # Nel caso migliore, la variabile è scrivibile e il suo valore non cambia.
                self.set_variable(a.get_browse_name(), a.get_value())

            except ReadOnlyWriteException:
                canwrite = False

            finally:
                self.__parameter_nodes__.append(
                    (
                        a.get_browse_name().Name,  # ->string: Nome della variabile
                        canwrite,  # ->bool: Se la variabile è scrivibile
                        a  # ->Node: Nodo della variabile
                    )
                )

    def __get_variable__(self, name: str):
        """
            Metodo privato per l'ottentimento della variabile da scrivere. Ritorna la variabile e un booleano,
            che indica se è scrivibile o meno.
        """
        _node = None
        for triples in self.__parameter_nodes__:
            if triples[0] == name:
                _node = triples

        return _node

    def get_variable(self, name):
        v = self.__get_variable__(name)
        return v[2].get_value()

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
            ua_variant = get_type_of_data(node)
            node.set_value(ua.DataValue(ua.Variant(v, ua_variant)))

        # Esempio di scrittura che da successo: ua.DataValue(ua.Variant(True, ua.VariantType.Boolean))
        # self.__logger__.write(f"Tentata scrittura della variabile {name} a {str(value)} "
        #                      f"da parte di {self.__username__}")
        rval = False
        try:
            v = self.__get_variable__(name)
            can_set_variable, node = v[1], v[2]
            if can_set_variable:
                do_set(value, node)
                rval = True
            else:
                raise ReadOnlyWriteException("Variabile non scrivibile")

        #    except ReadOnlyWriteException:
        #        self.__logger__.write("Variabile di sola lettura. Scrittura ignorata")
        #
        #    except Exception as f:
        #        self.__logger__.write(
        #            f"Utente {self.__username__} ha ottenuto un errore nella scrittura di {name}"
        #            f"{f.__cause__}"
        #        )

        finally:
            return rval

    def get_variable_names(self):
        names = []
        for d in self.__parameter_nodes__:
            names.append(d[0])
        return names

    @staticmethod
    def get_instance():
        global instance
        if instance is None:
            instance = Actor()
        return instance


class ReadOnlyWriteException(Exception):

    def __init__(self, str_err):
        super.__init__(str_err)
        self.__msg__ = str_err

    def __str__(self):
        return self.__msg__
