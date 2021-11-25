import os
import pathlib
import requests
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required, current_user
from Configuration.DBmanager import DBmanager, SqlDataNotFoundError
from flask import Flask, redirect, request, render_template, url_for, make_response

authenticated = False

"""
        Utilities
"""

db = DBmanager.get_instance()

"""
        Configurazione Flask App
"""

app = Flask(__name__)
app.debug = True
templatedir = os.path.join(pathlib.Path(__file__).parent.resolve(), "templates")
app.template_folder = templatedir
app.config['SECRET_KEY'] = "ASDASFCVERV2934282374"
app.config['ENV'] = "development"

bycrypt = Bcrypt(app)

"""login_manager = LoginManager(app)
login_manager.login_view = 'datapage'"""

"""
                    Routes
"""


@app.route("/data", methods=['GET', 'POST'])
def datapage():
    error = None
    if not authenticated:
        return redirect(url_for("load_user"))
    if request.method == 'POST':
        error = "POSTED"

    return render_template("mainpage.html", test=error)


"""

@app.route("/", methods=['GET', 'POST'])
@app.route("/login")
@login_manager.user_loader
def loadser():
    error = False
    reason = ""

    if request.method == 'POST':
        uname = request.form['username']
        pw = request.form['password']
        try:
            db.check_credentials(uname, pw)
            return redirect(url_for("datapage"))
        except SqlDataNotFoundError as sql:
            error = True
            reason = sql.__str__()
            print(reason)

    return render_template("loginpage.html", error=error, reason=reason)

"""


@app.route("/", methods=['GET', 'POST'])
@app.route("/login")
def load_user():
    global authenticated

    error = False
    reason = ""

    if request.method == "POST":
        try:

            db.check_credentials(request.form['username'], request.form['password'])
            authenticated = not authenticated
            return redirect(url_for("datapage"))
        except SqlDataNotFoundError as s:
            error = True
            reason = s.__str__()

    return render_template("loginpage.html", error=error, reason=reason)


if __name__ == '__main__':
    app.run(debug=True, host='localhost')
