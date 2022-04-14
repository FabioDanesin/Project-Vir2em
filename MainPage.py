import datetime
import json
import typing
from typing import Dict
import jwt

# Danilo non toccare sta roba

from flask import Flask, redirect, request, url_for, make_response, Response, jsonify
from json import loads
from functools import wraps

# import Control.Monitor
from Globals import KeyNames
from Configuration.DBmanager import DBmanager
from Globals.Parser import get_parsed_data
from Logs.Logger import Filetype, Logger
from Utils import hash_str

# from Frontend.Common import ReaderThread

# Istanza del parser
parserdata = get_parsed_data()
# cartella delle pagine del frontend
TEMPLATE_DIR = "Frontend/templates"

# -------------------------------------------------------------------------------------------------------------------- #
#                                                  Utilities                                                           #
# -------------------------------------------------------------------------------------------------------------------- #

db = DBmanager.get_instance()
# monitor = Control.Monitor.Monitor.get_instance()

# Nome del file dei log
Logname = "FlaskApplicationLog"
# Crea un file di log sul percorse dei log recuperando il path della cartella di log da ProjectData.txt
logfile = Logger(parserdata.get(KeyNames.logs), Logname, Filetype.LOCAL)

class ContentException(RuntimeError):
    """
    Classe wrapper semplice per incapsulamento e gestione di errori di contenuto generici per header di richieste, cookie
    eccetera.
    """
    def __init__(self, reason):
        self.__reason__ = reason

    def __str__(self):
        return  self.__reason__

def log(s):
    logfile.write(s)

def generate_user_token(username: str, password: str)->bytes:
    """
    Mette insieme username e password e crea il token
    :param name: Username user che riceve il token
    :param payload: Password dello user che riceve il token
    :return: Bytes del token
    """
    # Datetime non è codificabile in JSON. Raggiro il problema trasformando datetime in una stringa timestamp UNIX che
    # non richiede sforzi particolari di serializzazione.
    validity = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    payload = {
        "username" : username,
        "password" : password,
        "valid_until" : str(validity.strftime("%s"))  # La stringa di UNIX timestamp
    }

    return jwt.encode(
        payload,
        key=app.config["SECRET_KEY"],
        algorithm="HS256"
    )

def craft_basic_json_response(payload: typing.Any, status=200):
    """
    Crea la tipica response con JSON settando contenuto e header in modo appropriato.
    :param payload: Contenuto da serializzare in json
    :param status: Status della risposta. Default a 200
    :return: Response con JSON e header appropriati
    """
    response = app.response_class(
        response=jsonify(payload),
        status=status
    )
    response.headers["Content-Type"] = "application/json"
    response.headers["Encoding"] = "UTF-8"
    return response

def token_required(function : typing.Callable):
    """
    Questa funzione cerca di validare la firma del token ricevuto. Si aspetta di trovarlo nell'header della request
    sotto il nome 'token'.

    :param function: La funzione a cui applicare il decorator
    :return: None se il token è valido. Response con error altrimenti.
    """
    @wraps(function)
    def wrap(*args, **kwargs):
        try:
            # Cerco di ottenere il token dagli headers. Se dovesse essere assente lancio RuntimeError
            tok = request.headers.get('token')
            if tok is None:
                # Token non inviato
                return craft_basic_json_response({"$error":"Token assente"}, status=401)

            # Tento di decodificare il token secondo il metodo di encoding prestabilito.
            # Se dovesse essere stato parsato in modo scorretto per via di chiave / algoritmo errati, lancia
            # InvalidSignatureError
            decoded_token = jwt.decode(tok, app.config['SECRET_KEY'], algorithms=["HS256"])

            # Il token è stato decodificato e procedo ad estrarne il contenuto per validarlo
            username = decoded_token["username"]
            password = decoded_token["password"]
            date = decoded_token["valid_until"]

            # La data passata deve essere in UNIX timestamp, che può essere ricreato con un semplice metodo
            date = datetime.datetime.fromtimestamp(int(date))


            if datetime.datetime.utcnow() >= date:
                # Token scaduto. Il frontend deve redirectare al login.
                raise craft_basic_json_response({"$error":"OUTDATED TOKEN"}, status=401)

            # Il token è ancora in corso di validità. Controllo che username e password siano validi
            creds = db.check_credentials(username, password, request.remote_addr)

            # Il controllo è stato concluso con successo. La funzione può procedere.
            return function(*args, **kwargs)

        except (jwt.exceptions.InvalidSignatureError , RuntimeError) as invalid :
            # Trappo entrambe le exception in un singolo statement dato che la gestione dell'errore va fatta da frontend
            # e quindi la risposta è in entrambi i casi la stessa
            return craft_basic_json_response({"$error" : str(invalid)}, status=401)
    # ritorno della funzione che fa da wrapper effettivo.
    return wrap

def get_connection_root():
    # Debug
    root = "http"
    if SSL:
        root = root + 's'
    return f"{root}://{HOST}:{PORT}"


def setcookie(key: str, value: typing.Any, resp=None) -> None:
    """
    Funzione wrapper per il setting di un cookide dati la sua chaive e il suo valore.

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


# -------------------------------------------------------------------------------------------------------------------- #
#                                             Configurazione Flask App                                                 #
# -------------------------------------------------------------------------------------------------------------------- #

# Ip del server in cui viene eseguito il server flask
HOST = parserdata.get(KeyNames.site_ip)
# Porta del server
PORT = parserdata.get(KeyNames.site_port)
SSL = False
MAXATTEMPTS = 5

# Inizializzazione di flask -------------- #
app = Flask(__name__)
app.config['SECRET_KEY'] = '0f5d43f1ae8b1926f45c562c2adb7fffcea42fa5c95849d6589398cf768776b3'
app.config['ENV'] = "development"

# -------------------------------------------------------------------------------------------------------------------- #
#                                                     Routes                                                           #
# -------------------------------------------------------------------------------------------------------------------- #

@app.route("/geturls")
def urls():
    dresp = {
        "data": "/datarequest",
        "test": "/sendrequest"
    }

    return jsonify(dresp)


@app.route("/setcookie", methods=["GET", "POST"])
def cookie():
    if request.method == "POST":
        payload = request.get_json(force=True)
        setcookie("content", {"$content": payload})
    else:
        setcookie("content", {"$content": "defaultcookie"})
    return "DONE"


@app.route("/testcookie", methods=["GET", "POST"])
def test():
    r = make_response()
    r.set_cookie('content', 'content')
    return str(request.cookies.get("content"))


# Prende una request a Flask e richiede il DB per una variabile
@app.route("/datarequest", methods=["POST"])
@token_required
def parse_request():
    """

    :param token:
    :param jsonrequest:
    :return:
    """
    def create_datetime_from_default(defstring: str):
        # Funzione per parse, estrazione e creazione di un datetime per comparare le date in modo più comprensibile
        splitstring = defstring.split("-")
        year = splitstring[0]
        month = splitstring[1]
        day = splitstring[2]
        return  datetime.datetime(year, month, day)

    # Anno corrente
    year = datetime.datetime.now().year
    # Valori inline di default, se i valori nella richiesta dovessero essere assenti. Questi valori vengono sovrascritti
    # dai valori già definiti dentro alla richiesta
    defaults = {
        "begin_day": f"{year}-01-01",
        "end_day": f"{year}-12-31",
        "begin_hour": "0",
        "end_hour": "23"
    }

    try:
        jsonrequest = request.get_json()  # Pullo il json dalla richiesta.
        if jsonrequest is None:  # Se il contenuto è di tipo sbagliato, viene lanciato un errore di contenuto
            raise ContentException(f"Atteso json per questo url ma ricevuto {str(request.content_type)}")

        # Con questa sintassi, loaded_json_data viene eliminato finito lo statement
        with loads(jsonrequest) as loaded_json_data:
            name = loaded_json_data['name']  # Nome della variabile
            timeframe: Dict = loaded_json_data['timeframe']  # Timeframe richiesto
            for key in timeframe.keys():
                # Sostituisco le chiavi di default.
                defaults[key] = timeframe[key]

            # Performo un check per assicurarmi che le date siano consistenti(begin <= end)
            begin_day = create_datetime_from_default(defaults["begin_day"])
            end_day = create_datetime_from_default(defaults["end_day"])
            begin_hour = int(defaults["begin_hour"])
            end_hour = int(defaults["end_hour"])
            if not (begin_hour <= end_hour and begin_day <= end_day):
                raise ContentException("Formattazione delle date errato")

        values = db.get_variable_in_timeframe(
                name,
                defaults['begin_day'],
                defaults['end_day'],
                defaults['begin_hour'],
                defaults['end_hour']
            )

        return craft_basic_json_response(
            {
                "name":name,
                "values":values
            }
        )

    except KeyError as k:
        if app.debug:
            print(f"Key error detected : {k}")

        return craft_basic_json_response(
            {
                "$error": f"Nome chiave {k} non valida"
            },
            status=400
        )

    except ContentException as content:
        return craft_basic_json_response(
            {
                "$error": str(content)
            },
            status=400
        )


# Test di funzionamento di json (inutile al momento)
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
def logout() -> Response:
    """
    Logout user
    :return:
    """
    if app.debug:
        print("logout")
    request.cookies.clear()
    return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login() -> Response:
    """
    Funzione di login per Flask
    :return:
    """
    status = 404
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
            u = hash_str(u)
            p = hash_str(p)

            # Controllo credenziali
            credentials = db.check_credentials(u, p, ipaddr)
            if credentials is None:
                # Lo user richiesto non esiste. Registro il tentativo di connessione e ritorno un exception
                db.log_connection_attempt(ipaddr, u, p)
                raise RuntimeError("Username o password errati")

            # La funzione check_credentials ha individuato delle credenziali valide.
            # Creo il token, contenente username e password hashati dello user e validità.
            encoded_token = generate_user_token(u, p)

            # Dato che encoded_token è un tipo bytes, che non può essere serializzato a JSON, ritorno il token con una
            # custom response di testo normale
            return app.response_class(
                response=encoded_token,
                content_type="text/plain",
                status=200
            )
        else:
            status = 400
            raise RuntimeError(f"Questo URL accetta solo JSON, ma invece è stato dato "
                               f"{request.headers.get('Content-Type')}")
    except RuntimeError as rt:
        # Riempimento dei parametri di errore. Verranno messi in display sulla pagina web
        reason = str(rt)
        if app.debug:
            print(rt)
        responsedict = {"$error": reason}
        log(reason)

        return Response(
            response=json.dumps(responsedict),
            status=status
        )

@app.route("/test_token_requirement", methods=["POST"])
@token_required
def tokentesting():

    return jsonify(request.get_json(force=True))

@app.route("/")
def test_communication():
    t = {"$message": "the backend is running"}
    return jsonify(t)


# -------------------------------------------------------------------------------------------------------------------- #

def init():
    app.debug = True

    # ReaderThread().start()


if __name__ == '__main__':
    init()
    sslcont = ('cert.pem', 'key.pem')
    if SSL:
        app.run(debug=True, host=HOST, port=PORT, ssl_context=sslcont)
    else:
        app.run(debug=True, host=HOST, port=PORT)
