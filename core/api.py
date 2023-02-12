from flask import Flask, make_response, request, jsonify
from flask_autoindex import AutoIndex
from threading import Thread, Event, Lock
from core.scheduler import timetable
import time
import os


def run_app(api_host='0.0.0.0', api_port=8080, debug=True):
    app = Flask(__name__)
    app.config['DEBUG'] = debug
    files_index = AutoIndex(app, os.path.curdir + '/logs', add_url_rules=False)


    @app.route('/schedule/generate', methods=['POST'])
    def generate():
        data = request.get_json()
        path = os.path.join("logs", str(int(time.time())))

        Thread(target=timetable, args=(path,)).start()

        return "Generating schedule ..."


    @app.route('/schedule/view')
    @app.route('/schedule/view/<path:path>')
    def autoindex(path='.'):
        return files_index.render_autoindex(path)


    @app.route('/', methods=['GET'])
    def test():
        return "Welcome!"


    app.run(host=api_host, port=api_port, debug=debug)
