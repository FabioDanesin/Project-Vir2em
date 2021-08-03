import Client


def tuple_to_list(tup_in):
    l = []
    for a in tup_in:
        l.append(a)
    return a


class Actor(Client.__Monitor):

    def __check_login_credentials_(self, username, password):
        pass
        # TODO: implementare login tramite DB 

    def __init__(self, session_timeout, update_time, username, password, show_on_console=True, _url=Client.url):

        if not self.__check_login_credentials_(username, password):
            raise PermissionError()
        self.__username__ = username

        super().__init__(update_time, show_on_console, _url)
        self.__parameter_nodes = []

        for a in super().__parameters__:
            canwrite = True
            try:
                a.set_value(a.get_value())
            except Exception:
                canwrite = False
            finally:
                self.__parameter_nodes.append(
                    (
                        a.get_browse_name().Name,  # ->string: Nome della variabile
                        canwrite,  # ->bool: Se la variabile è scrivibile
                        a   # ->Node: Nodo della variabile
                    )
                )

    def get_variable(self, name: str):
        for a in super().__parameters__:
            if a.get_browse_name().Name == name:
                return a
        raise RuntimeError().__cause__

    def set_variable(self, name, value):
        var = self.get_variable(name)
        # TODO: implementare check per evitare setting di variabili read-only
        var.set_value(value)