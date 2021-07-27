from flask import Flask, send_file, redirect, abort
from flask_cors import CORS, cross_origin

AUTH_HOST = '127.0.0.1:5001'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/auth/<path:subpath>', methods=['GET', 'POST', 'PUT', 'PATCH'])
@cross_origin()
def auth(subpath):
    return redirect('http://%s/%s' % (AUTH_HOST, subpath), 308)


@app.route('/', methods=['GET'])
def index():
    try:
        return send_file('static/index.html')
    except FileNotFoundError:
        abort(404)


@app.route('/static/<path:subpath>', methods=['GET'])
def static_file(subpath):
    try:
        return send_file('static/%s' % subpath)
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run()
