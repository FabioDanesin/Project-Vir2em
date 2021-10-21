import datetime
import enum
import os

from Configuration import KeyNames
from Parser import get_parsed_data

parsed_data = get_parsed_data()
_path = parsed_data.get(KeyNames.logs)  # Path verso la cartella logs


class Filetype(enum.Enum):
    """
        Classe Enumeratore semplice e facilmente estendibile.
    """
    LOCAL = "LOCAL"
    SHARED = "SHARED"


class Logger:
    """
    Classe rappresentante il system logger. Espone solo 2 metodi, entrambi per la scrittura. Non sono previsti lock.
    Ogni istanza della classe logger produce un nuovo file a se stante.
    """

    def __init__(self, path: str, name: str, filetype: enum.Enum):
        """
        L'inizializzazione di un logger prevede la creazione di un nuovo file di logging. Ogni istanza della classe
        Logger.py è completamente indipendente dalle altre.

        :param path: Percorso a cui si desidera aprire il file di log
        :param name: Nome da inserire a tale file
        :param filetype: Dato di tipo Filetype per distinguere se si tratterà di un file locale o condivisibile via web
        """
        self.opened_file_time = datetime.date.today()  # Salvataggio della data odierna

        # Variabili per il restoring del file.
        self.filepath = path
        self.filename = name
        self.filetype = filetype

        # Apre il file per il logging
        self.file = Logger.__open_file__(self.filetype, self.opened_file_time, self.filename, "w")

        # Orario del timeout
        self.tomorrow = self.opened_file_time + datetime.timedelta(days=1)

        # Inizio logger
        self.write("BEGIN LOG")

    def __write__(self, string):
        self.file.write(string)  # Funzione shortcut per la scrittura. Non edita il messaggio in nessun modo

    @staticmethod
    def __open_file__(__ftype, __time, __name, __mode="w"):
        """
        Funzione per formattare in modo consistente il nome di nuovi file.

        :param __ftype: Tipo di file(ottenuto da Filetype).
        :param __time: orario di creazione del file.
        :param __name: nome che si intende dare al file.
        :param __mode: modalità con cui si vuole aprire il file. Settata a 'write' di default.
        :return: FileIOWrapper al file richiesto, creato nel punto specificato da path.
        """
        tmp = os.path.join(_path, "")
        finalpath = os.path.join(tmp, __ftype.value + " " + __time.__str__() + ":" + __name + ".txt")

        return open(finalpath, __mode)

    @staticmethod
    def __get_time__():
        """
        Ottieni l'ora sotto forma di una tripla di interi.

        :return: una tripla di interi formattata in (hh,mm,ss)
        """
        now = datetime.datetime.now()
        h, m, s = now.hour, now.minute, now.second
        return h, m, s

    def write(self, string):
        """
        Funzione principale per la scrittura. Il risultato conterrà un timestamp formattato in [hh:mm:ss]:
        all'interno del file di log.

        :param string: Stringa che si vuole passare al file di log.
        """
        # Ottenimento e formattazione delle ore, minuti e secondi.
        h, m, s = self.__get_time__()
        timestamp = f"[{str(h)}:{str(m)}:{str(s)}]:"  # Formattazione più chiara così 

        # Il flushing permette che il sistema scriva tutto immediatamente al file, altrimenti resterà in un file IO
        # buffer finchè non verrà chiamata una flush.
        self.__write__(timestamp + string + "\n")
        self.file.flush()

    def __has_expired__(self):
        """
        Controlla se il file di log ha sorpassato le 24 ore di vita e ne crea un altro se questa condizione risulta
        vera
        """
        if self.tomorrow < datetime.datetime.now():
            # Per l'amministratore di sistema
            self.write("END LOG")

            # Fa chiusura automatica del puntatore a file e flushing di qualsiasi cosa sia nel buffer
            self.file.close()

            # Reimposta il tempo di apertura all'ora corrente
            self.opened_file_time = datetime.datetime.now()

            # Sostituisce il file vecchio
            self.file = Logger.__open_file__(self.filetype, self.opened_file_time, self.filename, "w")

            self.write("BEGIN LOG")

    def __del__(self):
        self.write("END LOG")
        self.file.close()  # Non sono sicuro sia necessario, ma per buona misura
