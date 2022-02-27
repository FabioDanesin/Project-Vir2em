import datetime
import os
import pathlib
import threading
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

parserdata = get_parsed_data()
TEMPLATE_DIR = "templates"
DEFAULT_NONCE_LENGTH = 128

#
# Utilities
#

db = DBmanager.get_instance()
# monitor = Control.Monitor.Monitor.get_instance()
random = Random()
Logname = "FlaskApplicationLog"
logfile = Logger(parserdata.get(KeyNames.logs), Logname, Filetype.LOCAL)


def log(s):
    logfile.write(s)


def generate_nonce(length=DEFAULT_NONCE_LENGTH):
    s = ""

    for a in range(length):
        i = random.randint(33, 126)  # Caratteri contemplati da UTF-8 che non sono caratteri speciali.
        charachter = chr(i)
        s = s + charachter

    return s


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


#
# Configurazione Flask App
#

HOST = parserdata.get(KeyNames.site_ip)
PORT = parserdata.get(KeyNames.site_port)
SSL = False
MAXATTEMPTS = 5

app = Flask(__name__)
app.config['SECRET_KEY'] = "ASDASFCVERV2934282374"
app.config['ENV'] = "development"
app.template_folder = "./Frontend/templates"

login_manager = LoginManager()
login_manager.init_app(app)


def get_connection_root():
    root = "http"
    if SSL:
        root = root + 's'
    return f"{root}://{HOST}:{PORT}"


# bycrypt = Bcrypt(app)


#
# Routes
#

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
        # TODO: finire

    except KeyNames as k:
        print(f"Key error detected : {k}")


@login_required
@app.route("/sendrequest", methods=["GET"])
def request_url():
    datadict = {
        "Dataname": "NAME",
        "Datavalue": "231"
    }

    r = requests.post(
        f"{get_connection_root()}/datarequest",
        json=datadict
    )
    return str(r)


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
    u = splitted[0]
    p = splitted[1]

    try:
        credentials = db.check_credentials(u, p)
        return User(credentials["ID"])

    except RuntimeError:
        return None


@app.route("/", methods=['GET', 'POST'])
@app.route("/login")
def login() -> str:
    error = False
    reason = ""
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        try:
            cookiename = 'attempts'
            cookievalue = request.cookies.get(cookiename)
            # TODO: finire

            return redirect(url_for("request_url"))  # noqa, Ritorna comunque una string alla fine del redirect

        except RuntimeError as RT:
            error = True
            reason = f"Data for user {u} does not exist"
            log(reason)

    return render_template("loginpage.html", error=error, reason=reason)


if __name__ == '__main__':
    sslcont = ('cert.pem', 'key.pem')
    app.debug = True
    app.template_folder = './Frontend/templates'
    if SSL:
        app.run(debug=True, host=HOST, port=PORT, ssl_context=sslcont)
    else:
        app.run(debug=True, host=HOST, port=PORT)
