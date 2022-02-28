import datetime
import hashlib
import typing

from sqlalchemy import MetaData, create_engine, inspect, Table, Column, VARCHAR, DATE, INTEGER, and_, update
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.ext.automap import automap_base

from Configuration import KeyNames
from Logs.Logger import Logger, Filetype
from Parser import get_parsed_data

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


# Funzione di shortcut per hashing di stringhe
def hash_str(s: str):
    return hashlib.sha256(s.encode()).hexdigest()


instance = None


class DBmanager:
    """
    Classe per gestire lettura e scrittura del database in Postgres per la gestione degli accessi. Questa classe
    segue lo stesso design pattern dei singleton. Questa classe non "accende" il database, ma si collega solo a un
    account già collegato da cui poi opera. Non è necessario imparare la sintassi del database per usare questa classe
    in quanto opera in ORM.
    """

    def __init__(self):
        self.__logger__ = Logger(_log_path_, "Database log", Filetype.LOCAL)

        # Crea un engine per comunicare con il DB
        self.__user_data_engine__ = create_engine(user_database_connection_string)
        self.__plc_data_engine__ = create_engine(plc_data_database_connection_string)

        # Effettua la connessione al database url per i dati user e dati plc
        self.__user_data_connection__ = self.__user_data_engine__.connect()
        self.__plc_data_connection__ = self.__plc_data_engine__.connect()

        # Questa classe serve per mantenere tutti di dati parzialmente parsati prima di caricarli sul database
        self.__user_metadata__ = MetaData(self.__user_data_connection__)
        self.__plc_metadata__ = MetaData(self.__plc_data_connection__)

        # Questo campo memorizzato sotto forma di dizionario è un contenitore di tutti i dati disponibili nel database.
        # Le tabelle sono memorizzate secondo una coppia chiave - valore. Chiave sarà una stringa standard e il valore
        # sarà una lista di ennuple.
        self.__logger__.write("Inizializzazione avvenuta con successo")

    def check_credentials(self, username: str, password: str) -> typing.Dict[str, str]:
        """
        Metodo per il login tramite TLS con username e password. L'account richiesto deve contenere lo username e
        password corrispondenti e non deve essere un account bloccato.

        :param username: Username richiesto
        :param password: Password dell'account
        :return: Dictionary con dettagli dello user(ID, Nome, Password)
        """
        self.__logger__.write(f"User {username} is attempting login")

        metadata = self.__user_metadata__
        engine = self.__user_data_engine__

        # Pulla gli users
        users = self.__query_table__("users", metadata, engine)
        # Hasha la password. Il db contiene solo password hashate con SHA-256.
        if hash:
            hashed_name, hashed_password = hash_str(username), hash_str(password)
        else:
            hashed_name = username
            hashed_password = password

        for data in users:

            tname = data[1]  # Username
            tpassword = data[2]  # Password associata
            islocked = data[8]  # Booleano per il blocco account. False=account libero, True=account bloccato

            if hashed_name == tname and hashed_password == tpassword:
                if islocked:
                    self.__logger__.write(f"WARNING:User {username} is a locked account")
                    raise RuntimeError(f"{username}'s account is locked. This incident will be reported")

                self.__logger__.write(f"User {username} has logged")
                return {
                    "ID": data[0],
                    "Name": data[1],
                    "Password": data[2]
                }

        raise SqlDataNotFoundError(f"Data for {username} not found")

    def select_all_in_table(self, tablename) -> typing.List:
        """
        Ritorna una lista di ennuple(pari al numero di colonne della tabella richiesta) contenenti tutti i dati
        nella tabella con quel nome.
        :param tablename: Nome della tabella richiesta
        :return: Lista di ennuple
        """
        # MetaData contiene una lista di "chiavi" corrispondenti ai nomi delle tabelle contenuti al suo interno(NON all'
        # interno del database). Se ci sono due tabelle nei due database con lo stesso nome, verrà loggato un warning
        # e l'operazione verrà abortita.

        user_db_keys, plc_metadata_keys = self.__user_metadata__.tables.keys(), self.__plc_metadata__.tables.keys()

        # Ritorna true se il nome della tabella è contenuto nell'insieme dato
        c1, c2 = tablename in user_db_keys, tablename in plc_metadata_keys

        if c1 and c2:
            s = f"WARNING: 2 similar tables detected in User database and Plc metadata database by the name {tablename}"
            self.__logger__.write(s)
            raise RuntimeError("Duplicate table detected")

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
        # Shortcutting
        engine = self.__plc_data_engine__
        connection = self.__plc_data_connection__
        metadata = self.__plc_metadata__

        # Trasformo il dato in stringa e ottengo data e ora
        stringdata = str(value)
        __time = datetime.datetime.now()
        hour = __time.hour
        table = None  # Serve solo per evitare il warning

        try:
            # Tento di fetchare la tabella dal database
            table = self.__get_existing_table__(name, metadata, engine)
        except NoSuchTableError:
            # La tabella non esiste. Deve essere creata
            table = Table(
                name,
                metadata,
                Column("Timestamp", DATE, nullable=False),
                Column("Hour", INTEGER, nullable=False),
                Column("Value", VARCHAR(20), nullable=False)
            )
        finally:
            # Preparazione statement per l'insert
            insert_data = (__time, hour, stringdata)
            statement = table.insert(insert_data)

            # Esecuzione. Non deve ritornare nulla
            self.__execute_plc_data_operation__(statement)

    def get_variable_in_timeframe(self, name: str, begin_date: str, end_date: str, begin_hour: str = None,
                                  end_hour: str = None) \
            -> typing.List[typing.Tuple[datetime.date, int, str]]:
        """
        Ritorna una lista della tabella dal nome corrispondente a name nel range di data e ora richiesta.
        :param name: Nome della variabile richiesta
        :param begin_date: Limite inferiore della data di registrazione
        :param end_date: Limite superiore della data di registrazione
        :param begin_hour: Limite inferiore per l'ora di registrazione
        :param end_hour: Limite superiore per l'ora di registrazione
        :return: Lista di tipo date * int * string, rispettivamente data, ora e valore registrato.
        """
        # Solo per scopi di naming
        engine = self.__plc_data_engine__
        metadata = self.__plc_metadata__

        # Fetcho la tabella 'name' contenuta nel database
        table = self.__get_existing_table__(name, metadata, engine)

        # Estraggo le colonne "Timestamp" e "Hour" di table
        timestamp_column = table.c["Timestamp"]
        hour_column = table.c["Hour"]

        if begin_hour is None:
            # Caso neutro, qualsiasi ora va bene
            begin_clause = and_(True)
        else:
            # Obbligatoria come sintassi, altrimenti non compila correttamente
            begin_clause = and_(hour_column >= begin_hour).compile()

        # Lo stesso identico procedimento è fatto per l'ora di limite inferiore
        if end_hour is None:
            end_clause = and_(True)
        else:
            end_clause = and_(end_hour <= hour_column).compile()

        # Composizione della clausola WHERE
        where_clause = and_(begin_date <= timestamp_column, end_date >= timestamp_column, begin_clause, end_clause)

        # Statement finale è SELECT * FROM 'table' WHERE 'where_clause'
        statement = table.select().where(where_clause)

        # Wrappa l'esecuzione e ritorna la risposta dal DB
        result = self.__execute_user_data_operation__(statement)

        return result.fetchall()  # .fetchall() garantisce che il tipo di ritorno sia corretto

    @staticmethod
    def __get_existing_table__(name, metadata, engine) -> Table:
        """
        Ritorna l'oggetto corrispondente alla tabella contenuto nel DB
        :param name: Nome della tabella
        :param metadata: Metadati utilizzati per contenere la tabella richiesta
        :param engine: Engine stanziato per quella tabella e metadati
        :return: Tabella di nome richiesto
        """
        return Table(
            name,
            metadata,
            # Questo parametro carica automaticamente la tabella nei metadati se
            # già presente nel database
            autoload_with=engine
        )

    def __execute_user_data_operation__(self, __op):
        """
        Shortcut per esecuzione di query / modifiche sul database
        :param __op: Operazione da eseguire
        :return: Risultato della execute. Potrebbe essere None
        """
        return self.__user_data_connection__.execute(__op)

    def __execute_plc_data_operation__(self, __op):
        """
        Shortcut per l'esecuzione di interrogazioni / aggiunte dati al database per le variabili del PLC
        :param __op: Operazione da eseguire
        :return: Risultato della execute. Potrebbe essere None
        """
        return self.__plc_data_connection__.execute(__op)

    def __query_table__(self, tablename: str, metadata, engine):
        """
        Esegue il SELECT * della tabella passata come tablename. Richiede i suoi metadati e il suo engine.
        Dato che il contenuto può variare, sta al chiamante sapere il tipo di ritorno in modo preventivo.
        Se la tabella non esiste nel database, ritorna None.

        :param tablename: Nome della tabella.
        :param metadata: Metadati in cui la tabella è registrata.
        :param engine: Engine usato per stabilire e mantenere la connessione.
        :return: Lista dei contenuti della tabella.
        """
        if not isinstance(tablename, str):
            raise TypeError("A string is required")
        result = None
        try:
            # Si può fare una select su una tabella già presente nel database
            table = self.__get_existing_table__(tablename, metadata, engine)

            # SELECT * FROM 'table'
            statement = table.select()

            # Esegue il fetch di tutto il contenuto della tabella
            result = self.__execute_user_data_operation__(statement).fetchall()

        except NoSuchTableError as f:
            self.__logger__.write(f.__cause__)

        finally:
            return result

    def lock_user(self, username, password) -> None:
        """
        Funzione per bloccare le credenziali di uno user dopo aver raggiunto un numero di tentativi massimi durante il
        login. Se la coppia username, password non esiste nella tabella delle credenziali del database, i dati non
        variano.
        :param username: Username da lockare
        :param password: Password da lockare
        :return: None
        """
        # TODO: chiedere a Caiazza se usare solo lo username o meno
        table = self.__get_existing_table__('users', self.__user_metadata__, self.__user_data_engine__)
        statement = update(table) \
            .where(and_(table.c['name'] == username, table.c['password'] == password)) \
            .values(Locked=True)

        self.__execute_user_data_operation__(statement)


class SqlDataNotFoundError(RuntimeError):

    def __init__(self, option):
        super()
        self.__s__ = option

    def __str__(self):
        return self.__s__
