import requests
from Configuration.DBmanager import DBmanager as Database, SqlDataNotFoundError
from flask import Flask, redirect, request, render_template, url_for

db = Database.get_instance()
app = Flask(__name__)
app.template_folder = "Templates"


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = False
    if request.method == 'POST':
        uname = request.form['username']
        pw = request.form['password']
        try:
            db.check_credentials(uname, pw)
            return redirect("/data")
        except SqlDataNotFoundError:
            error = True
    return render_template("login.html", error=error)


@app.route("/otherpage", methods=['GET', 'POST'])
def otherpage():
    return render_template("otherpage.html")


@app.route("/mainpage", methods=['GET', 'POST'])
def main_page():
    test = 'posttest'
    print(url_for("/otherpage"))
    if request.method == 'POST':
        test = request.form['text']

        if test == 'spurdo':
            test = requests.post(url=url_for("/otherpage"))

    return render_template("mainpage.html", test=test)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
