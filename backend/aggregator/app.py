from flask import Flask, send_file, redirect, abort
from flask_cors import CORS, cross_origin
import os

AUTH_HOST = '127.0.0.1:5001'
FRONTEND_DIR_REL = 'frontend/dist'

if FRONTEND_DIR_REL[0] == '/':
    FRONTEND_DIR = FRONTEND_DIR_REL
else:
    FRONTEND_DIR = '%s/%s' % (os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))),
                              FRONTEND_DIR_REL)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/auth/<path:subpath>', methods=['GET', 'POST', 'PUT', 'PATCH'])
@cross_origin()
def auth(subpath):
    return redirect('http://%s/%s' % (AUTH_HOST, subpath), 308)


@app.route('/web/<path:subpath>', methods=['GET'])
def static_file(subpath):
    try:
        return send_file('%s/%s' % (FRONTEND_DIR, subpath))
    except FileNotFoundError:
        abort(404)


@app.route('/', methods=['GET'])
def index():
    try:
        return send_file('%s/index.html' % FRONTEND_DIR)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run()
