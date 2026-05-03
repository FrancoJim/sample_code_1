from flask import Flask, jsonify, render_template, request

from .change_machine import make_change

app = Flask(__name__)


def _to_json(result: dict) -> dict:
    return {
        "total": str(result["total"]),
        "change": [
            {
                "denom_name": item["denom_name"],
                "count": item["count"],
                "denom_amount": str(item["denom_amount"]),
            }
            for item in result["change"]
        ],
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = request.form.get("amount", type=float)
        if amount is None:
            return render_template("index.html", error="Please enter a numeric value")
        result = make_change(amount)
        if "error" in result:
            return render_template("index.html", error=result["error"])
        return render_template("index.html", result=result)
    return render_template("index.html")


@app.route("/api/v1/change")
def api_change():
    raw = request.args.get("amount")
    if raw is None:
        return jsonify({"error": "Missing required query parameter: amount"}), 400
    try:
        amount = float(raw)
    except ValueError:
        return jsonify({"error": "amount must be a numeric value"}), 400

    result = make_change(amount)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(_to_json(result))
