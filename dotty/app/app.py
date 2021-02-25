from flask import Flask, request, abort, jsonify, send_file
import uuid
from graphviz import Digraph, Graph, Source
import os
from os import path
app = Flask(__name__)


datadir = os.getenv('APP_DATA_DIR')
if datadir == None:
    datadir = '/tmp/dotty'

if not path.exists(datadir):
    os.makedirs(datadir)

@app.route('/')
def hello():
    abort(404)

@app.route('/dia/<uuid:id>/png')
def dia(id):
    f = '%s.png' % (str(id))
    filename = path.join(datadir,f)
    if not path.exists(filename):
        abort(404)
    return send_file(filename, mimetype='image/png')

@app.route('/dia', methods=['POST'])
def dia_new():
    content = {}
    try: 
        content = request.json
    except:
        abort(404)
    data = None
    if 'data' in content:
        data = content['data']
    datatype = None
    if not 'type' in content:
        datatype = 'dotty'
    id = str(uuid.uuid4())
    if data:
        if datatype == 'dotty':
            dot = Source (data)
            filename = '%s' % (id)
            dot.render(filename, directory=datadir, format='png')

    return jsonify({"uuid":id, })
    #return data


if __name__ == '__main__':
    app.run(host='0.0.0.0')
