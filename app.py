from flask import Flask, render_template, request
from database import Select_sidebar

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello world!<p>"


@app.route("/Search")
def Search():
    sidebar = Select_sidebar()
    item = ""
    return render_template("dashboard.jinja", sidebar=sidebar)


@app.route("/Search", methods=["POST", "GET"])
def Search_requests():
    if request.method == "POST":
        if request.form["Search"] == "dishes":
            return "<p>Very good</p>"

    return render_template("dashboard.jinja")


# <p><input name={{item}} type="radio" value={{item}}></p>
