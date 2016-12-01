from flask import Flask
app = Flask(__name__)

@app.route('/')
def load_page():
    return 'Water footprint page goes here!'
