from sqlalchemy import MetaData, create_engine, inspect, Table
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import NoSuchTableError

from Configuration import KeyNames
from Parser import get_parsed_data
from Logs.Logger import Logger, Filetype

import time
import hashlib

parsed_data = get_parsed_data()


def get_from_parsed_data(name):
    return parsed_data.get(name)


db_type = get_from_parsed_data(KeyNames.db_type)

# Nome del login su postgresql, deve anche essere il nome del database
user_name = get_from_parsed_data(KeyNames.db_admin_name)

# Password
user_password = get_from_parsed_data(KeyNames.db_admin_password)

# IP su cui il DB è locato
ip = get_from_parsed_data(KeyNames.db_ip)
port = get_from_parsed_data(KeyNames.db_port)

# URL completo. L'ordine dei parametri non deve essere cambiato
database_url = f"{db_type}+psycopg2://{user_name}:{user_password}@{ip}:{port}/fabio"
_log_path_ = parsed_data.get(KeyNames.logs)


# TODO : debug only
def makedb():
    eng = create_engine(database_url)
    con = eng.connect()
    inspector = inspect(eng)
    base = automap_base()
    base.prepare(eng, reflect=True)
    return eng, con, inspector, eng, MetaData()


instance = None


# TODO: rivedere commenti.
class DBmanager:
    """
    Classe per gestire lettura e scrittura del database in Postgres per la gestione degli accessi. Questa classe
    segue lo stesso design pattern dei singleton. Questa classe non "accende" il database, ma si collega solo ad un
    account già collegato da cui poi opera. Non è necessario imparare la sintassi del database per usare questa classe
    in quanto opera in ORM.
    """

    def __init__(self):

        self.__logger__ = Logger(_log_path_, "Database log", Filetype.LOCAL)

        # Crea l'engine per comunicare con il DB
        self.__engine__ = create_engine(database_url)

        # Inspector espone dei metodi per l'ottenimento delle tabelle presenti nel database in modo da avere una
        # visione piena dell'intero schema. Richiede un engine a cui eseguire il binding.
        # self.__inspector__ = inspect(self.__engine__) # non usato. può essere rimosso

        # Effettua la connessione all'database_url
        self.__connection__ = self.__engine__.connect()

        # Questa classe serve per mantenere tutti di dati parzialmente parsati prima di "pusharli" sul database
        self.__metadata__ = MetaData()

        # Questo campo memorizzato sotto forma di dizionario è un contenitore di tutti i dati disponibili nel database.
        # Le tabelle sono memorizzate secondo una coppia chiave - valore. Chiave sarà una stringa standard e il valore
        # sarà una lista di ennuple.
        self.__logger__.write("Sincronizzazione avvenuta con successo")
        self.instance = self

    def check_credentials(self, name: str, password: str):
        def hash_str(s: str):
            return hashlib.sha256(s.encode()).hexdigest()

        self.__logger__.write(f"User {name} is attempting to log in")

        timestart = time.time()  # Timer
        # Copia i contenuti la tabella users
        users = self.__query_table__('users')
        hashedpass = hash_str(password)
        hashedname = hash_str(name)

        # Compara le triple
        for data in users:

            if hashedname == data[1] and hashedpass == data[2]:
                timenow = time.time() - timestart
                self.__logger__.write(f"User {name} login successful. Elapsed time={timenow}")
                return data[3]

        raise SqlDataNotFoundError(f"Data for {name} not found")

    def __execute_operation__(self, __op):
        # Shortcut per esecuzione di query / modifiche sul database
        return self.__connection__.execute(__op)

    def __query_table__(self, tablename: str):
        if not isinstance(tablename, str):
            raise TypeError("A string is required")
        result = None
        try:
            # Si può fare una select su una tabella già presente nel database
            table = Table(
                tablename,
                self.__metadata__,
                # Questo parametro carica automaticamente la tabella nei metadati se
                # già presente nel database
                autoload_with=self.__engine__
            )
            statement = table.select()
            result = self.__execute_operation__(statement).fetchall()
        except NoSuchTableError as f:
            self.__logger__.write(f.__cause__)
        finally:
            return result

    @staticmethod
    def get_instance():
        global instance
        if instance is None:
            instance = DBmanager()
        return instance


class SqlDataNotFoundError(Exception):

    def __init__(self, option):
        super()
        self.__s__ = option

    def __str__(self):
        return self.__s__
