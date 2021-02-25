import os
import datetime
import flask
import json
import pytz
from flask import request
from os import walk


app = flask.Flask(__name__)
app.config["DEBUG"] = True

dirname = os.path.dirname(__file__)
login_dir = dirname + "/accounts"
info_dir = dirname + "/info"
ip_dir = dirname + "/ip"


def make_file(data, dirpath):
    dt = datetime.datetime.now()
    timezone = pytz.timezone('Asia/Shanghai')
    d_aware = dt.astimezone(timezone)
    filename = d_aware.strftime("%Y%m%d_%H%M%S") + ".txt"
    filename = os.path.join(dirpath, filename)
    with open(filename, "w") as f:
        for key in data:
            f.write(str(key) + ": " + str(data[key]) + "\n")


@app.route("/", methods=['GET'])
def hello():
    ip_files = []
    for (dirpath, dirnames, filenames) in walk(ip_dir):
        ip_files.extend(filenames)
        break
    login_files = []
    for (dirpath, dirnames, filenames) in walk(login_dir):
        login_files.extend(filenames)
        break
    info_files = []
    for (dirpath, dirnames, filenames) in walk(info_dir):
        info_files.extend(filenames)
        break

    html = "<div>IP Files: <ul>"
    for file in ip_files:
        html += "<li>" + file + "</li>"
    html += "</ul></div>"
    html += "<div>Login Files: <ul>"
    for file in login_files:
        html += "<li>" + file + "</li>"
    html += "</ul></div>"
    html += "<div>Info Files: <ul>"
    for file in info_files:
        html += "<li>" + file + "</li>"
    html += "</ul></div>"

    return html


@app.route('/ip', methods=['POST'])
def record_ip():
    data = request.get_json()
    make_file(data, ip_dir)
    return json.dumps({'status': 'success'})


@app.route('/login', methods=['POST'])
def record_login():
    data = request.get_json()
    make_file(data, login_dir)
    return json.dumps({'status': 'success'})


@app.route('/info', methods=['POST'])
def record_info():
    data = request.get_json()
    make_file(data, info_dir)
    return json.dumps({'status': 'success'})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
