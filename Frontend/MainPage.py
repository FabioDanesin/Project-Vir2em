import requests
from flask import Flask, redirect, request, render_template, url_for, make_response
import os
import pathlib
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required
from Configuration.DBmanager import DBmanager, SqlDataNotFoundError

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

loginmanager = LoginManager(app)
loginmanager.login_view = "loginpage"
loginmanager.login_message_category = "info"

"""
                    Routes
"""


@app.route("/", methods=['GET', 'POST'])
@app.route("/login")
@loginmanager.user_loader
def load_user():
    error = False
    reason = ""

    if request.method == 'POST':
        uname = request.form['username']
        pw = request.form['password']
        try:
            db.check_credentials(uname, pw)
        except SqlDataNotFoundError as sql:
            error = True
            reason = sql.__str__()
            print(reason)

    return render_template("loginpage.html", error=error, reason=reason)


if __name__ == '__main__':
    app.run(debug=True, host='localhost')
