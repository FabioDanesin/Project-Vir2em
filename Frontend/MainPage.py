import json
import os
import pathlib
from random import Random

import requests
# Danilo non toccare sta roba

from flask import Flask, redirect, request, render_template, url_for, make_response, Response
from Configuration.DBmanager import DBmanager, SqlDataNotFoundError

authenticated = False
TEMPLATE_DIR = "templates"
DEFAULT_NONCE_LENGTH = 128

#
# Utilities
#

db = DBmanager.get_instance()
random = Random()


def generate_nonce(length=DEFAULT_NONCE_LENGTH):
    s = ""

    for a in range(length):
        i = random.randint(33, 126)  # Caratteri contemplati da UTF-8 che non sono caratteri speciali.
        charachter = chr(i)
        s = s + charachter

    return s


#
# Configurazione Flask App
#

HOST = "localhost"

app = Flask(__name__)
app.debug = True
app.template_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), TEMPLATE_DIR)
app.config['SECRET_KEY'] = "ASDASFCVERV2934282374"
app.config['ENV'] = "development"

# bycrypt = Bcrypt(app)


#
# Routes
#

@app.route("/datarequest", methods=["POST"])
def get_data():
    if request.method == "POST":
        body = request.json
        print(body)
        response = requests.Response()
        response.status_code = 200

        return Response(
            status=200,
            response=json.dumps(
                {
                    "Name": "Sensor",
                    "Value": 21
                }
            ),
            content_type="application/json"
        )


@app.route("/sendrequest", methods=["GET"])
def request_url():
    datadict = {
        "Dataname": "NAME",
        "Datavalue": "231"
    }
    r = requests.post(
        "http://127.0.0.1:5000",
        json=datadict
    )
    print(r)
    print(str(r.cookies))
    return "success"


@app.route("/data", methods=['GET', 'POST'])
def datapage():
    error = None
    if not authenticated:
        return redirect(url_for("load_user"))
    if request.method == 'POST':
        error = "POSTED"

    return render_template("mainpage.html", test=error)


@app.route("/logout")
def logout():
    global authenticated
    authenticated = False
    redirect(url_for("load_user"))


@app.route("/", methods=['GET', 'POST'])
@app.route("/login")
def load_user():
    global authenticated

    error = False
    reason = ""

    if request.method == "POST":
        try:

            # db.check_credentials(request.form['username'])
            db.check_credentials("Vir2em_Fabio")
            authenticated = True
            return redirect(url_for("datapage"))
        except SqlDataNotFoundError as s:
            error = True
            reason = s.__str__()

    return render_template("loginpage.html", error=error, reason=reason)


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=443, ssl_context=('cert.pem', 'key.pem'))
