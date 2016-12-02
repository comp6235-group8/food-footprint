from flask import Flask, Response
import json
app = Flask(__name__)

@app.route('/')
def load_page():
    data = json.dumps([{"tomato": 1.12}, {"potato": 2.12}])
    resp = Response(response=data,
                    status=200,
                    mimetype="application/json")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
