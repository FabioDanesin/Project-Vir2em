######################################################
# FIXME: import di psycopg2 fallisce, non so come mai
######################################################
from flask_sqlalchemy import *
from sqlalchemy import MetaData, Table, Column, create_engine


pgsql_name = "postgres"  # Nome del login su postgresql
pgsql_password = "SuperUser"  # Password
pgsql_ip = "127.0.0.1"      # IP su cui il DB è locato
pgsql_port = "5432"         # port

db_url = "postgresql://" + pgsql_name + "@" + pgsql_password + pgsql_ip + ":" + pgsql_port


class DBmanager:
    """
    Classe per gestire lettura e scrittura del database in Postgres per la gestione degli accessi. Questa classe
    segue lo stesso design pattern dei singleton. Questa classe non "accende" il database, ma si collega solo ad un
    account già collegato da cui poi opera. Non è necessario imparare la sintassi del database per usare questa classe
    in quanto opera in ORM.
    """

    def __init__(self, url):
        # Mantenimento della proprietà singleton assicurato tramite questo campo
        self.__exists__ = []

        # Check a runtime per il controllo della proprietà singleton.
        # Potrebbe non essere foolproof ma è l'una del mattino quindi ci penso domani
        if len(self.__exists__) == 1 and self.__exists__[0] is not None:
            raise RuntimeError()

        # Crea l'engine per comunicare con il DB
        self.__engine__ = create_engine(url, dialect="postgresql", echo=True)

        # Effettua la connessione all'url
        self.__connection__ = self.__engine__.connect()

        # Proprietà singleton
        self.__exists__ = [self]

        # Questa classe serve per mantenere tutti di dati parzialmente parsati prima di "pusharli" sul database
        self.__metadata__ = MetaData()

