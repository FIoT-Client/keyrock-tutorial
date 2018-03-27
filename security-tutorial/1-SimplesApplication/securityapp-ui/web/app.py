from flask import Flask, render_template, request
from config import BaseConfig
import requests

app = Flask(__name__)
app.config.from_object(BaseConfig)

url_service = "http://127.0.0.1:5055/"


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/hello", methods=['GET'])
def hello():
    r = requests.get(url_service + "service1")
    return render_template('index.html', content=r.text)


@app.route("/username", methods=['GET'])
def username():
    r = requests.get(url_service + "service1/" + request.args.get('username'))
    return render_template('index.html', content=r.text)


@app.route("/list", methods=['GET'])
def list():
    r = requests.get(url_service + "service2/list")
    return render_template('index.html', content=r.text)


@app.route("/add", methods=['GET'])
def add():
    r = requests.get(url_service + "service2/add/" + request.args.get('name'))
    return render_template('index.html', content=r.text)


@app.route('/reset')
def reset():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5050)
