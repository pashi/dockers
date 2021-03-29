from flask import Flask, request, abort, jsonify, send_file, render_template, make_response, redirect
import uuid
import os
from os import path
import glob
import json
app = Flask(__name__)

def get_desc():
    with open('data/info.txt','r') as fp:
        return fp.read()
    return None

def is_active_slot(id):
    name = os.path.join('data','slot%s' % (id),'active' )
    if os.path.exists(name):
        return True
    return False

def is_answers(id,key):
    ret = []
    name = os.path.join('data','answers','slot%s' % (id), key )
    if os.path.exists(name):
        return True
    return False

def write_answers(id,key,data):
    ret = []
    name = os.path.join('data','answers','slot%s' % (id), key )
    with open(name, 'w') as fp:
        fp.write(data)

def get_slots(key=None):
    ret = []
    for f in sorted(glob.glob('data/slot*/info.txt')):
        dirname = os.path.dirname(f)
        is_active = os.path.exists(os.path.join(dirname,'active'))
        slotname = os.path.basename(dirname)
        with open(f,'r') as fp:
            data = fp.read()
        d = {'slot': slotname, 'active': is_active, 'data':data, 'answer': None}
        if not key == None:
            d['answer'] = is_answers(d['slot'].replace('slot',''),key)
        ret.append(d)
    return ret

def get_answers(id):
    ret = []
    filename = os.path.join('data','slot%s' % (id), 'data.json')
    with open(filename,'r') as fp:
        data = json.load(fp)
    for item in data:
        ret.append({'answerkey': item, 'answervalue': data[item]})
    return ret
    

def validate_key(id):
    name = os.path.join('data','key',id)
    if os.path.exists(name):
        return True
    return False

@app.route('/login', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        key = request.form['key']
        if validate_key(key):
            resp = make_response(redirect('/slots/'))
            resp.set_cookie('key', key)
            return resp
    return render_template('login.html')

@app.route('/logout', methods = ['POST', 'GET'])
def logout():
    resp = make_response(redirect('/login'))
    resp.set_cookie('key', 'invalid')
    return resp


@app.route('/slots/')
def slots():
    key = request.cookies.get('key')
    if not validate_key(key):
        return make_response(redirect('/logout'))
    return render_template('slots.html', slots=get_slots(key), key=key, description=get_desc())

@app.route('/slots/<int:id>', methods = ['POST', 'GET'])
def slot(id):
    key = request.cookies.get('key')
    if not validate_key(key):
        return make_response(redirect('/logout'))
    if request.method == 'POST':
        if not is_active_slot(id):
            return make_response(redirect('/slots/'))
        if is_answers(id,key):
            return make_response(redirect('/slots/'))
        vote = request.form['vote']
        write_answers(id,key,vote)
    return render_template('slot.html', answers=get_answers(id), key=key, voted=is_answers(id,key), slot=id)

if __name__ == '__main__':
    os.makedirs(os.path.join('data','answers'),exist_ok=True)
    for x in get_slots():
        os.makedirs(os.path.join('data','answers',x['slot']),exist_ok=True)
    os.makedirs(os.path.join('data','key'),exist_ok=True)
    debug = os.getenv('APPDEBUG')
    if not debug == None:
        debug = True
    else:
        debug = False
    app.run(host='0.0.0.0', port=5000, debug=debug)
