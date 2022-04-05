import datetime
import json
import typing
from typing import Dict, List, Optional, Tuple, Any
import jwt

import requests
# Danilo non toccare sta roba

from flask import Flask, redirect, request, render_template, url_for, make_response, Response, jsonify, session
from flask_login import login_required, current_user, LoginManager, UserMixin, logout_user
from json import loads, dumps
from functools import wraps

# import Control.Monitor
import Utils
from Configuration import KeyNames
from Configuration.DBmanager import DBmanager, SqlDataNotFoundError
from Parser import get_parsed_data
from Logs.Logger import Filetype, Logger
from Utils import hash_str, generate_nonce

# from Frontend.Common import ReaderThread

# Istanza del parser
parserdata = get_parsed_data()
# cartella delle pagine del frontend
TEMPLATE_DIR = "Frontend/templates"

#
# Utilities
#

db = DBmanager.get_instance()
# monitor = Control.Monitor.Monitor.get_instance()

# Nome del file dei log
Logname = "FlaskApplicationLog"
# Crea un file di log sul percorse dei log recuperando il path della cartella di log da ProjectData.txt
logfile = Logger(parserdata.get(KeyNames.logs), Logname, Filetype.LOCAL)


def log(s):
    logfile.write(s)


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
        return not self.__eq__(other)


class UserAlreadyLoggedInException(RuntimeError):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def generate_token(name):
    token = {'user' : name, 'exp' : str(datetime.datetime.utcnow() + datetime.timedelta(hours=1))}
    print(token)
    return {'token' : token}

def validate_token(tok: bytes):
    try:
        # Token parsing. Potrebbe essere un token 'fabbricato', quindi si controlla prima.
        t = jwt.decode(tok, app.config['SECRET_KEY'], algorithms=["HS256"])

        username = t.get('user')
        date = t.get('exp')

        if datetime.datetime.utcnow() >= date:
            r = RuntimeError()
            r.__cause__ = "INVALID"
            raise r
        if username not in db.select_all_in_table('users'):
            log("Username inseistente in token")
            raise RuntimeError("Username inesistente")

        return True

    except jwt.exceptions.InvalidSignatureError:
        return False

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
app.config['SECRET_KEY'] = generate_nonce(128)
app.config['ENV'] = "development"

login_manager = LoginManager()
login_manager.init_app(app)


# -------------------------------------------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------------------------------------------- #
def get_connection_root():
    root = "http"
    if SSL:
        root = root + 's'
    return f"{root}://{HOST}:{PORT}"

def token_valid(token):
    @wraps(token)
    def validate(*args, **kwargs):
        t = request.cookies.get("token")
        if t is not None and validate_token(t):
            return "LOL"
        # TODO: finire
    return validate


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
@login_required
@app.route("/geturls")
def urls():
    dresp = {
        "data": "/datarequest",
        "test": "/sendrequest"
    }

    return jsonify(dresp)

@app.route("/setcookie", methods=["GET","POST"])
def cookie():
    if request.method == "POST":
        payload = request.get_json(force=True)
        setcookie("content", {"$content":payload})
    else:
        setcookie("content", {"$content":"defaultcookie"})
    return "DONE"

@app.route("/testcookie", methods=["GET","POST"])
def test():
    r = make_response()
    r.set_cookie('content', 'content')
    return str(request.cookies.get("content"))

# Prende una request a Flask e richiede il DB per una variabile
# TODO: terminare la richiesta al DB
@login_required
@app.route("/datarequest", methods=["POST"])
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

        return jsonify(
            db.get_variable_in_timeframe(
                name,
                defaults['begin_day'],
                defaults['end_day'],
                defaults['begin_hour'],
                defaults['end_hour']
            )
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

    return jsonify(datadict)


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
    request.cookies.clear()
    return redirect(url_for("load_user"))


@login_manager.user_loader
def load_user(uid: str) -> Tuple[Optional[User], Optional[Any]]:
    """
    Callback di flask_login per il login dello user. Prende una singola stringa.

    :param uid: Identificazione dello user, in realtà la coppia Username#Password
    :return: Istanza della classe User se il login ha successo, None altrimenti.
    """
    splitted = uid.split("#")

    u = splitted[0]   # Username non hashato.
    p = splitted[1]   # Password non hashata.
    ip = splitted[2]  # Indirizzo IP.

    try:
        u = hash_str(u)
        p = hash_str(p)
        # Controllo credenziali
        credentials = db.check_credentials(u, p, ip)
        # Il controllo è stato superato.
        return User(credentials["ID"]), credentials

    except RuntimeError:

        # Una parte della procedura ha lanciato un errore. Loggo il tentativo di connessione a database e a logfile e
        # ritorno None.

        db.log_connection_attempt(ip, hash_str(u), hash_str(p))

        log(f"User at ip {ip} tried accessing the account at username {u}, which is registered as {hash_str(u)} in the "
            f"database.")

        return None, None

@app.route("/login", methods=['GET','POST'])
def login() -> Response:
    """
    Funzione di login per Flask
    :return:
    """

    # Al momento della pressione del bottone d'invio, la funzione legge i dati dalla POST e ottiene
    # username e password
    try:
        if request.headers.get('Content-Type') == 'application/json':
            body = request.get_json(force=True)  # Il json viene parsato automaticamente dal metodo.
            u = body["username"]
            p = body["password"]

            ipaddr: str = str(request.remote_addr)

            # Utilizzo della callback. Formatto la stringa come 'username#password#ip' al fine di passare una
            # stringa sola
            user, response = load_user(f"{u}#{p}#{ipaddr}")
            if user is None:
                # Lo user richiesto non esiste
                raise RuntimeError("Username o password errati")

            # La funzione load_user ha individuato delle credenziali valide. Procede al login
            token = generate_token(f"{hash_str(u)}#{hash_str(p)}")

            response = jwt.encode(
                token,
                app.config['SECRET_KEY'],
                algorithm="HS256"
            )
            setcookie("Token", response, make_response())
            return response  # noqa, Ritorna comunque una string alla fine del redirect
        else:
            raise RuntimeError(f"Questo URL accetta solo JSON, ma invece è stato dato "
                               f"{request.headers.get('Content-Type')}")
    except RuntimeError as rt:
        # Riempimento dei parametri di errore. Verranno messi in display sulla pagina web
        reason = str(rt)
        responsedict = {"$error": reason}
        log(reason)

        return Response(
            response=json.dumps(responsedict),
            status=404
        )

@app.route("/debug", methods=["GET"])
def deb():
    html = request.get_json(True)

    return str(html)


@app.route("/dashboard/table")
def table():
    return render_template("/dashboard/table")


@app.route("/dashboard/storico")
def hystory():
    return render_template("/dashboard/storico")

@app.route("/")
def m():
    return render_template("index.html")

# -------------------------------------------------------------------------------------------------------------------- #

def init():
    app.debug = True
    app.template_folder = './static'

    # ReaderThread().start()


if __name__ == '__main__':
    init()
    sslcont = ('cert.pem', 'key.pem')
    if SSL:
        app.run(debug=True, host=HOST, port=PORT, ssl_context=sslcont)
    else:
        app.run(debug=True, host=HOST, port=PORT)
