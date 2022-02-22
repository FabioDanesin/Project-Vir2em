import json
import os
import pathlib
from random import Random
from typing import Dict, List

import requests
# Danilo non toccare sta roba

from flask import Flask, redirect, request, render_template, url_for, make_response, Response
from flask_login import login_required, current_user, LoginManager, UserMixin, logout_user

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
random = Random()
Logname = "FlaskApplicationLog"
logfile = Logger(parserdata.get(KeyNames.logs), Logname, Filetype.LOCAL)


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

app = Flask(__name__)
app.debug = True
app.template_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), TEMPLATE_DIR)
app.config['SECRET_KEY'] = "ASDASFCVERV2934282374"
app.config['ENV'] = "development"

login_manager = LoginManager()
login_manager.init_app(app)


# bycrypt = Bcrypt(app)


#
# Routes
#

@app.route("/datarequest", methods=["POST"])
def parse_request(jsonrequest : json):



@login_required
@app.route("/sendrequest", methods=["GET"])
def request_url():
    datadict = {
        "Dataname": "NAME",
        "Datavalue": "231"
    }
    r = requests.post(
        "http://127.0.0.1:5000/datarequest",
        json=datadict
    )
    return str(r)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("load_user"))


@login_manager.user_loader
def load_user(uid: str):
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

            load_user(f"{u}#{p}")

            return redirect(url_for("request_url"))  # noqa, Ritorna comunque una string alla fine del redirect
        except RuntimeError:
            error = True
            reason = f"Data for user {u} does not exist"

    return render_template("loginpage.html", error=error, reason=reason)


@app.route("/foo")
def foo():
    return "Nothing"


if __name__ == '__main__':
    app.template_folder = './Frontend/templates'
    app.run(debug=True, host=HOST, port=PORT)
