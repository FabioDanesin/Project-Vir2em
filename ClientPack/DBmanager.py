import timeit

from sqlalchemy import MetaData, create_engine, inspect, Table
from sqlalchemy.sql import select
from sqlalchemy.ext.automap import automap_base
from Logger import Logger, Filetype

import threading
from time import sleep, perf_counter

db_type = "postgresql"
db_dialect = "psycopg2"
user_name = "fabio"             # Nome del login su postgresql, deve anche essere il nome del database
user_password = "Vir2em_Fabio"  # Password
ip = "localhost"                # IP su cui il DB è locato
port = "5432"

# URL completo. L'ordine dei parametri non deve essere cambiato
url = db_type + "+" + db_dialect + "://" + user_name + ":" + user_password + "@" + ip + ":" + port + "/"

_log_path_ = ""      # TODO: Implementare logging tramite parser


# TODO : debug only
def makedb():
    eng = create_engine(url)
    con = eng.connect()
    inspector = inspect(eng)
    base = automap_base()
    base.prepare(eng, reflect=True)
    return eng, con, inspector, eng, MetaData()


class DBmanager:
    """
    Classe per gestire lettura e scrittura del database in Postgres per la gestione degli accessi. Questa classe
    segue lo stesso design pattern dei singleton. Questa classe non "accende" il database, ma si collega solo ad un
    account già collegato da cui poi opera. Non è necessario imparare la sintassi del database per usare questa classe
    in quanto opera in ORM.
    """
    # Proprietà singleton statica
    __exists__ = None

    def __init__(self, datbase_url, auto_update=True, poll=3):
        def poller(polltime):

            while True:
                sleep(polltime)
                for name in self.__get_all_table_names__():
                    timer = perf_counter()
                    self.__update_table__(name)
                    elapsed = perf_counter() - timer
                    self.__logger__.write(f"Aggiornata tabella {name} in {elapsed:0.3f} secondi")
        # Singleton
        if self.__exists__ is not None:
            raise RuntimeError()
        self.__logger__ = Logger(_log_path_, "Database log", Filetype.LOCAL)

        # Crea l'engine per comunicare con il DB
        self.__engine__ = create_engine(datbase_url)

        # Inspector espone dei metodi per l'ottenimento delle tabelle presenti nel database in modo da avere una visione
        # piena dell'intero schema. Richiede un engine a cui eseguire il binding.
        self.__inspector__ = inspect(self.__engine__)

        # Effettua la connessione all'url
        self.__connection__ = self.__engine__.connect()

        # Questa classe serve per mantenere tutti di dati parzialmente parsati prima di "pusharli" sul database
        self.__metadata__ = MetaData()

        # Questo campo memorizzato sotto forma di dizionario è un contenitore di tutti i dati disponibili nel database.
        # Le tabelle sono memorizzate secondo una coppia chiave - valore. Chiave sarà una stringa standard e il valore
        # sarà una lista di ennuple.
        self.__tables__ = {}
        self.__get_all_rows_in_db__()
        self.__logger__.write("Sincronizzazione avvenuta con successo")

        # Proprietà singleton
        self.__exists__ = self

        if auto_update:
            t = threading.Thread(
                name="Database update",
                target=poller(poll),
                daemon=True
            )

    def check_credentials(self, name, password):
        # Copia senza eliminare la tabella users
        users = self.__tables__.get('users')
        # Compara le triple
        for data in users:
            if (name, password) == (data[1], data[2]):
                return True
        return False

    def __get_all_table_names__(self):
        return self.__inspector__.get_table_names()

    def __get_all_rows_for_tablename__(self, name):
        return self.__inspector__.get_columns(name)

    def __get_all_rows_in_db__(self):
        tablenames = []
        for name in self.__get_all_table_names__():
            tablenames.append(
                Table(
                    name,                          # Nome della tabella
                    self.__metadata__,             # Contenitore dei metadati della tabella
                    autoload_with=self.__engine__  # Importante, dice al database che la tabella è già presente
                )
            )  # Preleva gli attributi dalle tabelle

        for tb in tablenames:
            name = tb.name

            # Esegue una SELECT * FROM <name> e ritorna una lista
            # di tutte le righe
            statement = self.__execute_operation__(select(tb))

            # Pulla i dati dalla lista creata e li inserisce nel
            # dizionario. La chiave corrisponde al nome della tabella
            self.__tables__[name] = statement.fetchall()

    def __update_table__(self, name):
        self.__tables__[name] = self.__execute_operation__(select(name)).fetchall()

    def __execute_operation__(self, __op):
        # Shortcut per esecuzione di query / modifiche sul database
        return self.__connection__.execute(__op)
