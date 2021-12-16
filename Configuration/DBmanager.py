import datetime
import typing
import time
import hashlib

from typing import Tuple

from sqlalchemy import MetaData, create_engine, inspect, Table, Column, VARCHAR, DATE, INTEGER, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import NoSuchTableError

from Configuration import KeyNames
from Parser import get_parsed_data
from Logs.Logger import Logger, Filetype

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
user_database_connection_string = f"{db_type}+psycopg2://{user_name}:{user_password}@{ip}:{port}/users"
plc_data_database_connection_string = f"{db_type}+psycopg2://{user_name}:{user_password}@{ip}:{port}/data"
_log_path_ = parsed_data.get(KeyNames.logs)


# TODO : debug only
def make_user_data():
    udb_eng = create_engine(user_database_connection_string)
    udb_con = udb_eng.connect()
    udb_inspector = inspect(udb_eng)
    udb_base = automap_base()
    udb_base.prepare(udb_eng, reflect=True)
    return udb_eng, udb_con, udb_inspector, udb_base


def make_data():
    d_eng = create_engine(plc_data_database_connection_string)
    d_con = d_eng.connect()
    d_insp = inspect(d_eng)
    d_base = automap_base()
    d_base.prepare(d_eng, reflect=True)
    return d_eng, d_con, d_insp, d_base


# Utility function per hashare
def hash_str(s: str):
    return hashlib.sha256(s.encode()).hexdigest()


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
        self.__user_data_engine__ = create_engine(user_database_connection_string)
        self.__plc_data_engine__ = create_engine(plc_data_database_connection_string)

        # Inspector espone dei metodi per l'ottenimento delle tabelle presenti nel database in modo da avere una
        # visione piena dell'intero schema. Richiede un engine a cui eseguire il binding.

        # Effettua la connessione al database url per i dati user e dati plc
        self.__user_data_connection__ = self.__user_data_engine__.connect()
        self.__plc_data_connection__ = self.__plc_data_engine__.connect()

        # Questa classe serve per mantenere tutti di dati parzialmente parsati prima di "pusharli" sul database
        self.__user_metadata__ = MetaData(self.__user_data_connection__)
        self.__plc_metadata__ = MetaData(self.__plc_data_connection__)

        # Questo campo memorizzato sotto forma di dizionario è un contenitore di tutti i dati disponibili nel database.
        # Le tabelle sono memorizzate secondo una coppia chiave - valore. Chiave sarà una stringa standard e il valore
        # sarà una lista di ennuple.
        self.__logger__.write("Inizializzazione avvenuta con successo")

    def check_credentials(self, name: str) -> Tuple[bytes, bytes, bytes, bytes]:
        # Procedura di login per scram. La rimozione è in corso d'opera

        self.__logger__.write(f"User {name} is attempting to log in")

        timestart = time.time()  # Timer
        # Copia i contenuti la tabella users
        users = self.__query_table__('users', self.__user_metadata__, self.__user_data_engine__)
        hashedname = hash_str(name)

        # Compara le triple
        for data in users:

            if hashedname == data[1]:
                timenow = time.time() - timestart
                self.__logger__.write(f"User {name} login successful. Elapsed time={timenow}")

                saltbyte = data[4].encode()
                serversecretbyte = data[5].encode()
                userkeybyte = data[6].encode()
                iterationbyte = data[7]

                return saltbyte, userkeybyte, serversecretbyte, iterationbyte

        raise SqlDataNotFoundError(f"Data for {name} not found")

    def check_tls_credentials(self, username: str, password: str) -> str:
        self.__logger__.write(f"User {username} attempts login")
        metadata = self.__user_metadata__
        engine = self.__user_data_engine__

        users = self.__query_table__("users", metadata, engine)

        hashed_name, hashed_password = hash_str(username), hash_str(password)

        for data in users:

            tname = data[1]
            tpassword = data[2]
            islocked = data[8]

            if hashed_name == tname and hashed_password == tpassword:
                if islocked:
                    self.__logger__.write(f"User {username} is a locked account")
                self.__logger__.write(f"User {username} has logged")
                return data[3]

        raise SqlDataNotFoundError(f"Data for {username} not found")

    def update_scram_variables(self,
                               username: str,
                               salt: str,
                               stored_key: str,
                               server_key: str,
                               iteration_count: str
                               ) -> None:
        metadata = self.__user_metadata__
        engine = self.__user_data_engine__

        table = self.__get_existing_table__("users", metadata, engine)

        statement = table.update() \
            .where(table.c["name"] == hash_str(username)) \
            .values(
            salt=salt,
            server_secret=server_key,
            client_secret=stored_key,
            iteration=iteration_count
        )

        self.__execute_user_data_operation__(statement)

    def select_all_in_table(self, tablename) -> typing.List:

        if tablename in self.__user_metadata__.tables.keys():
            meta = self.__user_metadata__
            engine = self.__user_data_engine__
            operation = self.__execute_user_data_operation__
        elif tablename in self.__plc_metadata__.tables.keys():
            meta = self.__plc_metadata__
            engine = self.__plc_data_engine__
            operation = self.__execute_plc_data_operation__

        else:
            raise SqlDataNotFoundError(f"Table {tablename} does not exist")

        table = self.__get_existing_table__(tablename, meta, engine)
        statement = table.select()
        return operation(statement).fetchall()

    @staticmethod
    def get_instance():
        global instance

        if instance is None:
            instance = DBmanager()
        return instance

    def add_variable_sample(self, name: str, value) -> None:
        """
        Funzione per aggiungere il valore di una variabile al database delle variabili del PLC.
        Se la tabella associata a quella variabile non esiste, viene creata.
        :param name: Nome della variabile
        :param value: Valore della media
        """
        engine = self.__plc_data_engine__
        connection = self.__plc_data_connection__
        metadata = self.__plc_metadata__

        stringdata = str(value)
        __time = datetime.datetime.now()
        hour = __time.hour

        if not engine.dialect.has_table(connection, name):
            table = Table(
                name,
                metadata,
                Column("Timestamp", DATE, nullable=False),
                Column("Hour", INTEGER, nullable=False),
                Column("Value", VARCHAR(20), nullable=False)
            )
            table.create(engine)
        else:
            table = self.__get_existing_table__(name, metadata, engine)

        insert_data = (__time, hour, stringdata)
        statement = table.insert(insert_data)

        self.__execute_plc_data_operation__(statement)

    def get_variable_in_timeframe(self, name, begin_day, end_day, begin_hour=None, end_hour=None):
        engine = self.__plc_data_engine__
        metadata = self.__plc_metadata__

        table = self.__get_existing_table__(name, metadata, engine)
        timestamp_column = table.c["Timestamp"]
        hour_column = table.c["Hour"]
        if begin_hour is None:
            # Caso neutro
            begin_clause = and_(True)
        else:
            # Obbligatoria come sintassi, altrimenti non compila
            begin_clause = and_(hour_column >= begin_hour).compile()

        if end_hour is None:
            end_clause = and_(True)
        else:
            end_clause = and_(end_hour <= hour_column).compile()

        where_clause = and_(begin_day <= timestamp_column, end_day >= timestamp_column, begin_clause, end_clause)
        statement = table.select().where(where_clause.compile())
        res = self.__execute_plc_data_operation__(statement).fetchall()

        return res

    @staticmethod
    def __get_existing_table__(name, metadata, engine) -> Table:
        return Table(
            name,
            metadata,
            # Questo parametro carica automaticamente la tabella nei metadati se
            # già presente nel database
            autoload_with=engine
        )

    def __execute_user_data_operation__(self, __op):
        # Shortcut per esecuzione di query / modifiche sul database
        return self.__user_data_connection__.execute(__op)

    def __execute_plc_data_operation__(self, __op):
        return self.__plc_data_connection__.execute(__op)

    def __query_table__(self, tablename: str, metadata, engine):
        if not isinstance(tablename, str):
            raise TypeError("A string is required")
        result = None
        try:
            # Si può fare una select su una tabella già presente nel database
            table = self.__get_existing_table__(tablename, metadata, engine)
            statement = table.select()
            result = self.__execute_user_data_operation__(statement).fetchall()
        except NoSuchTableError as f:
            self.__logger__.write(f.__cause__)
        finally:
            return result


class SqlDataNotFoundError(Exception):

    def __init__(self, option):
        super()
        self.__s__ = option

    def __str__(self):
        return self.__s__
