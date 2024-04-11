from flask import Flask, jsonify
from mc_fetcher import mc_fetch
from et_fetcher import et_fetch
from th_fetcher import th_fetch

app = Flask(__name__)

@app.route("/moneycontrol")
def mc():
    data = mc_fetch()
    return jsonify({
        "data": data
    }), 200

@app.route("/economic_times")
def et():
    data = et_fetch()
    return jsonify({
        "data": data
    }), 200

@app.route("/the_hindu")
def bs():
    data = th_fetch()
    return jsonify({
        "data": data
    }), 200

if __name__ == "__main__":
    app.run()