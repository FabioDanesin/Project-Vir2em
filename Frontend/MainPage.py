import json

import requests
from flask import Flask, redirect, request, render_template, url_for

app = Flask(__name__)
app.template_folder = "Templates"


@app.route("/otherpage", methods=['POST'])
def other():
    return 'bruh moment'


@app.route("/mainpage", methods=['GET', 'POST'])
def main_page():
    test = 'posttest'

    if request.method == 'POST':
        test = request.form['text']

        if test == 'spurdo':
            o = json.loads(test)
            test = requests.post(url_for("/otherpage"), json=o)

    return render_template("mainpage.html", test=test)


@app.route("/")
def _redirect():
    return redirect("/mainpage")


if __name__ == '__main__':
    app.debug = True
    app.run('localhost', 8000)

