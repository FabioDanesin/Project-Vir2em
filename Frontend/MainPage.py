from flask import Flask, redirect, request, render_template, url_for

app = Flask(__name__)
app.template_folder = "Templates"


@app.route("/otherpage", methods=['POST'])
def other():
    return render_template("otherpage.html")


@app.route("/mainpage", methods=['POST'])
def main_page_post():
    d = request.form['text']
    return d


@app.route("/mainpage")
def main_page():
    return render_template("mainpage.html", test='posttest')


@app.route("/")
def _redirect():
    return redirect('/mainpage')


if __name__ == '__main__':
    app.debug = True
    app.run()
