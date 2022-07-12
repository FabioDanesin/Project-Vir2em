import datetime
import json
import typing
from typing import Dict, Tuple

import jwt
import requests
from flask import Flask, redirect, request, url_for, make_response, Response, jsonify, abort
from json import loads
from functools import wraps

import Configuration.DBmanager
from Globals import KeyNames
from Configuration.DBmanager import DBmanager, get_from_parsed_data
from Globals.Parser import get_parsed_data
from Logs.Logger import Filetype, Logger
from Utils import hash_str

# from Control import Monitor

# Istanza del parser
parserdata = get_parsed_data()
# cartella delle pagine del frontend
TEMPLATE_DIR = "Frontend/templates"
# monitor = Monitor.Monitor.get_instance()

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
    Classe wrapper semplice per incapsulamento e gestione di errori di contenuto generici per header di richieste,
    cookie eccetera.
    """

    def __init__(self, reason):
        self.__reason__ = reason

    def __str__(self):
        return self.__reason__


def log(s):
    logfile.write(s)


def generate_user_token(username: str, password: str) -> bytes:
    """
    Mette insieme username e password e crea il token
    :param username: Username user che riceve il token
    :param password: Password dello user che riceve il token
    :return: Bytes del token
    """
    # Datetime non è codificabile in JSON. Raggiro il problema trasformando datetime in una stringa timestamp UNIX che
    # non richiede sforzi particolari di serializzazione.
    validity = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    payload = {
        "username": username,
        "password": password,
        "valid_until": str(validity.strftime("%s"))  # La stringa di UNIX timestamp
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


def token_required(function: typing.Callable):
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
                raise RuntimeError("Token assente")

            # Tento di decodificare il token secondo il metodo di encoding prestabilito.
            # Se dovesse essere stato parsato in modo scorretto per via di chiave / algoritmo errati, lancia
            # InvalidSignatureError
            decoded_token = jwt.decode(tok, app.config['SECRET_KEY'], algorithms=["HS256"])

            # Il token è stato decodificato e procedo ad estrarne il contenuto per validarlo
            username = decoded_token.get("username")
            password = decoded_token.get("password")
            date = decoded_token.get("valid_until")
            for t in [username, password, date]:
                # L'error sarebbe lo stesso per tutti.
                if t is None:
                    raise RuntimeError(f"Chiave {t} mancante")
            # La data passata deve essere in UNIX timestamp, che può essere ricreato con un semplice metodo
            date = datetime.datetime.fromtimestamp(int(date))

            if datetime.datetime.utcnow() >= date:
                # Token scaduto. Il frontend deve redirectare al login.
                raise craft_basic_json_response({"$error": "OUTDATED TOKEN"}, status=401)

            # Il token è ancora in corso di validità. Controllo che username e password siano validi
            creds = db.check_credentials(username, password, request.remote_addr)

            # Il controllo è stato concluso con successo. La funzione può procedere.
            return function(*args, **kwargs)

        except (jwt.exceptions.InvalidSignatureError, RuntimeError) as invalid:
            # Trappo entrambe le exception in un singolo statement dato che la gestione dell'errore va fatta da frontend
            # e quindi la risposta è in entrambi i casi la stessa
            return craft_basic_json_response({"$error": str(invalid)}, status=401)

    # ritorno della funzione che fa da wrapper effettivo.
    return wrap


def get_connection_root():
    # Debug
    root = "http"
    if SSL:
        root = root + 's'
    return f"{root}://{HOST}:{PORT}"


def setcookie(key: str, value: typing.Any, response: Response = None, has_age=False) -> Response:
    """
    Funzione wrapper per il setting di un cookide dati la sua chaive e il suo valore.

    :param key: La chiave del cookie
    :param value: Valore da salvare nel cookie
    :param response: Response preesistente da ritornare. Opzionale.
    :return: Response con cookie
    :param has_age: Se il cookie ha un tempo di vita massimo di 1 ora. Se omesso, dura fino alla fine della sessione del
                    browser.
    """
    if response is None:
        resp = make_response()
    else:
        resp = response
    expire = None

    if has_age:
        expire = datetime.datetime.now() + datetime.timedelta(hours=1)

    resp.set_cookie(key, str(value), secure=True, httponly=False, samesite="Strict", expires=expire)

    return resp


def deletecookie(key, response) -> Response:
    """
    Funzione wrapper per la cancellazione del cookie dalla macchina client connessa. Se il cookie non esiste, fallisce
    senza lanciare un eccezione o errore.

    :param key: Chiave del cookie da eliminare.
    :param response: Response preesistente da ritornare. Opzionale.
    :return: None
    """
    if response is None:
        resp = make_response()
    else:
        resp = response
    resp.delete_cookie(key, secure=True, httponly=False, samesite="Strict")

    return resp


def setcookies(key_value_dictionary: Dict[str, typing.Any]) -> Response:
    """

    :param key_value_dictionary: Dizionario di coppie chiave - valore.
    :return: Response con cookie inseriti.
    """
    response = make_response()
    for key in key_value_dictionary:
        response = setcookie(key, key_value_dictionary[key], response)

    return response


# -------------------------------------------------------------------------------------------------------------------- #
#                                             Configurazione Flask App                                                 #
# -------------------------------------------------------------------------------------------------------------------- #

# Ip del server in cui viene eseguito il server flask
HOST = get_from_parsed_data(KeyNames.api_ip)
# Porta del server
PORT = get_from_parsed_data(KeyNames.api_port)
SSL = False
MAXATTEMPTS = 5

# -------------- Inizializzazione di flask -------------- #
app = Flask(__name__)
app.config['SECRET_KEY'] = '0f5d43f1ae8b1926f45c562c2adb7fffcea42fa5c95849d6589398cf768776b3'
app.config['ENV'] = "development"


# -------------------------------------------------------------------------------------------------------------------- #
#                                                     Routes                                                           #
# -------------------------------------------------------------------------------------------------------------------- #

@app.errorhandler(400)
def bad_request_handle(description):
    """
    Wrapper per errore bad request.
    :param description:
    :return:
    """
    return app.response_class(response=description, status=400)


@app.route("/variable_names")
@token_required
def tabnames():
    d_var_name = {}
    print(monitor.__variables__)
    for i in range(0, len(monitor.__variables__)):
        d_var_name[str(i)] = monitor.__variables__[i].get_browse_name()
    response = craft_basic_json_response({"names": d_var_name}, 200)
    return response


@app.route("/setcookie", methods=["GET", "POST"])
def cookie():
    c = request.cookies.get("number")
    print(c)
    if c == "" or c is None:
        c = "0"
    else:
        c = str(int(c) + 1)
    return setcookie("number", c)


@app.route("/testcookie", methods=["GET", "POST"])
def showcookies():
    s = "COOKIES:"
    for c in request.cookies:
        s = s + "<p>" + str(c) + "</p>"
    return s


@app.route("/data/all", methods=["POST"])
@token_required
def get_all_samples():
    """
    Request shortcut per ottenere tutti i dati contenuti nella tabella richiesta.

    Struttura della richiesta:

    {
        "names" : string list
    }
    :return: Dizionario JSON con ogni entry contenente il nome della variabile richiesta e una lista di valori
             registrati per la variabile corrispondente.
    """
    try:
        # Estrazione del payload e assicurata compliance con i mimetype.
        json_payload: str = request.get_json()

        if json_payload is None:
            return app.response_class(
                status=400,
                response="Expected JSON mimetype, but found" + request.mimetype
            )

        # Estrazione del payload. Potrebbe lanciare JSONDecodeError se dovesse fallire.
        json_payload: Dict[str, typing.List[str]] = json.loads(json_payload)

        # Estrazione lista dei nomi. Potrebbe lanciare KeyError
        names = json_payload.pop("names")

        # Per ogni nome estraggo i valori della variabile e li inserisco in un dizionario.
        var_names_content = {}
        for name in names:
            data = db.select_all_in_table(name)
            var_names_content[name] = str(data)

        return craft_basic_json_response(var_names_content)

    except (json.decoder.JSONDecodeError, KeyError) as badreq_error:
        # Uno dei due errori viene ritornato come una Bad Request.
        abort(400, description=str(badreq_error))

    except Configuration.DBmanager.SqlDataNotFoundError as sql_err:
        # L'errore viene ignorato, ma loggato internamente
        log(sql_err)
        pass


@app.route("/data/latest", methods=["POST"])
@token_required
def get_latest():
    """
    Url per ottenere l'ultimo dato inserito nel database in ordine di tempo.
    Struttura della richiesta:
    {
        "name": string
    }

    Composizione della response.
    {
        "value" : number,
        "time": YYYY-MM-DD
    }
    :return:
    """
    try:
        parsed = request.get_json(True)
        name = parsed['name']
        v = db.__plc_data_connection__.execute(
            f"SELECT {name}.value, {name}.timestamp "
            f"FROM {name} "
            "ORDER BY timestamp, hour DESC "
            "LIMIT 1"
        ).fetchone()

        if v is None:
            raise RuntimeError("Variabile has no measurements yet")
        response_payload = {
            "value": v[0],
            "time": v[1]
        }
        resp = jsonify(response_payload)
        return resp


    except json.JSONDecodeError as jserr:
        abort(400, description=(str(jserr)))

    except Configuration.DBmanager.SqlDataNotFoundError as sqlerr:
        abort(404, description=str(sqlerr))

    except Exception as generic_exc:
        print(generic_exc)
        abort(500, description=str(generic_exc))


# Prende una request a Flask e richiede il DB per una variabile
@app.route("/data", methods=["POST"])
@token_required
def parse_request():
    """
    Url per la richiesta di dati per variabili singole.
    Struttura della richiesta:
    {
        "names" : string,
        "begin_day": YYYY-MM-DD", --> Opzionale
        "end_day": YYYY-MM-DD", --> Opzionale
        "begin_hour": "(0|23)", --> Opzionale
        "end_hour": "(0|23)" --> Opzionale
    }
    :return:
    """

    def create_datetime_from_default(defstring: str):
        # Funzione per parse, estrazione e creazione di un datetime per comparare le date in modo più comprensibile
        splitstring = defstring.split("-")
        years = int(splitstring[0])
        month = int(splitstring[1])
        day = int(splitstring[2])
        return datetime.datetime(years, month, day)

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
                "name": name,
                "values": values
            }
        )

    except KeyError as k:
        if app.debug:
            print(f"Key error detected : {k}")
        abort(400, description=f"Nome chiave {k} non valida")

    except ContentException as content:
        abort(400, description=str(content))


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


@app.route("/login", methods=['POST'])
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
            print(u, p)
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
            resp = make_response()
            setcookie("token", encoded_token, resp)
            resp.status_code = 200
            resp.data = "success"  # Per debug.
            return resp
        else:
            errstr = f"Questo URL accetta solo JSON, ma invece è stato dato {request.headers.get('Content-Type')}"
            return abort(400, description=errstr)
    except RuntimeError as rt:
        # Riempimento dei parametri di errore. Verranno messi in display sulla pagina web
        reason = str(rt)
        print(rt)
        responsedict = {"$error": reason}
        resp = craft_basic_json_response(responsedict, 401)
        return resp


@app.route("/test_token_requirement", methods=["POST"])
@token_required
def tokentesting():
    return jsonify(request.get_json(force=True))


@app.route("/")
def test_communication():
    t = {"$message": "the backend is running"}
    return jsonify(t)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


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
