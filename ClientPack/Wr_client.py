import Client


# Inutile
def tuple_to_list(tup_in):
    outl = []
    for a in tup_in:
        outl.append(a)
    return outl


class Actor:
    """
    Questa classe permette a un client di scrivere dati / mandare segnali ad un controllore. Mantiene gli stessi
    privilegi di lettura dati dal Monitor, con l'aggiunta di poter inviare segnali per la scrittura
    """
    def __check_login_credentials_(self, username, password):
        pass
        # TODO: implementare login tramite DB 

    def __init__(self, username, password, monitor: Client.__Monitor = Client.__Monitor.__get_instance__(),
                 _url=Client.url):

        if not self.__check_login_credentials_(username, password):
            # Lo username e la password data non sono validi. Si lancia un errore e la sessione è terminata
            raise PermissionError()

        self.__username__ = username
        self.__monitor__ = monitor
        self.__parameter_nodes = []

        for a in self.get_parameters():
            canwrite = True
            try:
                # Per testare se la variabile può essere scritta si tenta di inserire il valore corrente della variabile
                # stessa. Nel caso peggiore, il permesso è negato e la variabile non è scrivibile. Nel caso migliore,
                # la variabile è scrivibile e il suo valore non cambia.
                # Non implemento questo check ulteriormente perchè ne sto cercando di migliori
                a.set_value(a.get_value())
            except Exception:
                canwrite = False #
            finally:
                self.__parameter_nodes.append(
                    (
                        a.get_browse_name().Name,  # ->string: Nome della variabile
                        canwrite,  # ->bool: Se la variabile è scrivibile
                        a  # ->Node: Nodo della variabile
                    )
                )

    def get_variable(self, name: str):
        for a in self.get_parameters():
            if a.get_browse_name().Name == name:
                return a
        raise RuntimeError().__cause__

    def set_variable(self, name, value):
        var = self.get_variable(name)
        # TODO: implementare check per evitare setting di variabili read-only
        var.set_value(value)

    def get_parameters(self):
        return self.__monitor__.__parameters__
