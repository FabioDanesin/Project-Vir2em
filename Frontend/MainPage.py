from flask import Flask, redirect, request, render_template, url_for

app = Flask(__name__)
app.template_folder = "Templates"


@app.route("/otherpage", methods=['POST'])
def other():
    x = 'bruh'
    return render_template("otherpage.html", bruh=x)


@app.route("/mainpage", methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        print("padania")
        return redirect("/otherpage")
    return render_template("mainpage.html", user='bruh')


@app.route("/")
def _redirect():
    return redirect('/mainpage')


if __name__ == '__main__':
    app.debug = True
    app.run()
