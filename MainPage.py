import datetime
import typing
from random import Random
from typing import Dict, List, Optional

import requests
# Danilo non toccare sta roba

from flask import Flask, redirect, request, render_template, url_for, make_response, Response
from flask_login import login_required, current_user, LoginManager, UserMixin, logout_user
from json import loads, dumps

# import Control.Monitor
from Configuration import KeyNames
from Configuration.DBmanager import DBmanager, SqlDataNotFoundError
from Parser import get_parsed_data
from Logs.Logger import Filetype, Logger

# Istanza del parser
parserdata = get_parsed_data()
# cartella delle pagine del frontend
TEMPLATE_DIR = "templates"
# Attualmente non impiegato
DEFAULT_NONCE_LENGTH = 128

#
# Utilities
#

db = DBmanager.get_instance()
# monitor = Control.Monitor.Monitor.get_instance()
# attualmente non impiegato
random = Random()
# Nome del file dei log
Logname = "FlaskApplicationLog"
# Crea un file di log sul percorse dei log recuperando il path della cartella di log da ProjectData.txt
logfile = Logger(parserdata.get(KeyNames.logs), Logname, Filetype.LOCAL)


def log(s):
    logfile.write(s)


# Al momento non usata (usata per comunicazione con scramp)
def generate_nonce(length=DEFAULT_NONCE_LENGTH):
    s = ""

    for a in range(length):
        i = random.randint(33, 126)  # Caratteri contemplati da UTF-8 che non sono caratteri speciali.
        charachter = chr(i)
        s = s + charachter

    return s


# -------------------------------------------------------------------------------------------------------------------- #
class User(UserMixin):
    """
    Classe "pupazzetto" per facilitare le politiche di flask_login
    """
    logged_in_users: List[str] = []

    def __init__(self, identity: str):
        if identity in User.logged_in_users:
            raise UserAlreadyLoggedInException(f"{identity} is already logged in")

        self.id = identity
        self.logged_in = True

    def get_id(self):
        return self.id

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.id is not None

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.get_id()
        return False

    def __ne__(self, other):
        if isinstance(other, User):
            return not self.__eq__(other)
        return False


class UserAlreadyLoggedInException(RuntimeError):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


# -------------------------------------------------------------------------------------------------------------------- #
# Configurazione Flask App
#

# Ip del server in cui viene eseguito il server flask
HOST = parserdata.get(KeyNames.site_ip)
# Porta del server
PORT = parserdata.get(KeyNames.site_port)
SSL = False
MAXATTEMPTS = 5

# Inizializzazione di flask -------------- #
app = Flask(__name__)
app.config['SECRET_KEY'] = "ASDASFCVERV2934282374"
app.config['ENV'] = "development"
app.template_folder = "./Frontend/templates"

login_manager = LoginManager()
login_manager.init_app(app)


# ---------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
def get_connection_root():
    root = "http"
    if SSL:
        root = root + 's'
    return f"{root}://{HOST}:{PORT}"


# bycrypt = Bcrypt(app)


def setcookie(key: str, value: typing.Any, resp=None) -> None:
    """
    Funzione wrapper per il setting di un cookide dati la sua chaive e il suo valore. Opzionalmente è possibile passare
    un oggetto di make_response() per alleggerire il lavoro del garbage collector.

    :param key: La chiave del cookie
    :param value: Valore da salvare nel cookie
    :param resp: Istanza opzionale di make_response()
    :return: None
    """
    if resp is None:
        resp = make_response()
    resp.set_cookie(key, str(value), secure=True, httponly=False, samesite="Strict")


def deletecookie(key, resp=None) -> None:
    """
    Funzione wrapper per la cancellazione del cookie dalla macchina client connessa. Se il cookie non esiste, fallisce
    senza lanciare un eccezione o errore.

    :param key: Chiave del cookie da eliminare.
    :param resp: Istanza opzionale di make_response.
    :return: None
    """
    if resp is None:
        resp = make_response()
    resp.delete_cookie(key, secure=True, httponly=False, samesite="Strict")


#
# Routes
#

# Prende una request a Flask e richiede il DB per una variabile
# TODO: terminare la richiesta al DB
@login_required
@app.route("/datarequest")
def parse_request(jsonrequest: str):
    year = datetime.datetime.now().year
    defaults = {
        "begin_day": f"{year}-01-01",
        "end_day": f"{year}-12-31",
        "begin_hour": "0",
        "end_hour": "23"
    }

    try:
        with loads(jsonrequest) as loaded_json_data:
            name = loaded_json_data['name']
            timeframe: Dict = loaded_json_data['timeframe']
            for key in timeframe.keys():
                defaults[key] = timeframe[key]

        data = db.get_variable_in_timeframe(
            name,
            defaults['begin_day'],
            defaults['end_day'],
            defaults['begin_hour'],
            defaults['end_hour']
        )
        list_json = dumps(data)
        r = requests.post(
            '',  # TODO: definire URL per posting di dati da mettere su grafico.
            json=list_json
        )

    except KeyNames as k:
        print(f"Key error detected : {k}")


# Test di funzionamento di json (inutile al momento)
@login_required
@app.route("/sendrequest", methods=["GET"])
def request_url():
    datadict = {
        "Dataname": "NAME",
        "Datavalue": "231"
    }
    print(request.cookies)
    r = requests.post(
        f"{get_connection_root()}/datarequest",
        json=datadict
    )
    return str(r)


# Funzione di logout dell'utente da flask
# TODO: da terminare e rivedere
@app.route("/logout")
@login_required
def logout() -> Response:
    """
    Logout user
    :return:
    """
    logout_user()
    print("logout")
    return redirect(url_for("load_user"))


@login_manager.user_loader
def load_user(uid: str) -> Optional[User]:
    """
    Callback di flask_login per il login dello user. Prende una singola stringa.

    :param uid: Identificazione dello user, in realtà la coppia Username#Password
    :return: Istanza della classe User se il login ha successo, None altrimenti.
    """
    splitted = uid.split("#")
    cookiekey = 'attempts'  # Chiave per il cookie dei tentativi di accesso. Non è dipendente da password.
    u = splitted[0]  # Username non hashato.
    p = splitted[1]  # Password non hashata.
    resp = make_response()  # Response del server.

    try:
        # Controllo credenziali
        credentials = db.check_credentials(u, p)

        # Controllo superato con successo. Lo user può accedere al sito.
        deletecookie(cookiekey, resp)

        return User(credentials["ID"])

    except RuntimeError:
        # Accaduto un errore di qualche tipo. Incremento del cookie dei tentativi.
        c = request.cookies.get(cookiekey, default='0', type=int)

        if c == MAXATTEMPTS:
            # Tentativi massimi raggiunti. Se lo username è presente nel database, quello username viene considerato
            # compromesso e dovrà essere sbloccato in base alle politiche dell'azienda.
            db.lockUser(u, p)
            deletecookie(cookiekey, resp)

        else:
            # Incrementa.
            setcookie(cookiekey, c + 1, resp)

        return None


@app.route("/", methods=['GET', 'POST'])
@app.route("/login")
def login() -> str:
    """
    Funzione di login per Flask
    :return:
    """
    error = False  # Se ai è verificato un errore
    reason = ""  # Che errore si è verificato

    error = False
    reason = ""
    if request.method == "POST":
        # Al momento della pressione del bottone d'invio, la funzione legge i dati dalla pagina di HTML e ottiene
        # username e password
        u = request.form["username"]
        p = request.form["password"]

        try:
            # Utilizzo della callback. Formatto la stringa come 'username#password' al fine di passare una stringa sola
            if load_user(f"{u}#{p}") is None:
                # Lo user richiesto non esiste
                raise RuntimeError()
            # La funzione load_user ha individuato delle credenziali valide. Procede al login
            load_user(f"{u}#{p}")
            return redirect(url_for("request_url"))  # noqa, Ritorna comunque una string alla fine del redirect

        except RuntimeError as rt:
            # Riempimento dei parametri di errore. Verranno messi in display sulla pagina web
            error = True
            reason = rt.__str__()
            # TODO: rafforzare procedura anti bruteforcing con database

            log(reason)

    # Se siamo qui o la pagina è appena stata aperta o si è verificato un errore
    return render_template("loginpage.html", error=error, reason=reason)


# -------------------------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    sslcont = ('cert.pem', 'key.pem')
    app.debug = True
    app.template_folder = './Frontend/templates'
    if SSL:
        app.run(debug=True, host=HOST, port=PORT, ssl_context=sslcont)
    else:
        app.run(debug=True, host=HOST, port=PORT)
