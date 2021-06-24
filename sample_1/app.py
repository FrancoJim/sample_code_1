from flask import Flask, render_template, request

from .change_machine import make_change


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = request.form.get("amount", type=float)
        if amount:
            return render_template("index.html", coins_bills=make_change(amount))
        else:
            return render_template(
                "index.html", not_numeric="Please, enter a Float or Integer"
            )
    else:
        return render_template("index.html")
