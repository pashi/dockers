import json
import requests
import shutil
import sys, os

url_prefix = os.getenv('URL_PREFIX')
if url_prefix == None:
    url_prefix = 'http://localhost:5000/dia'

url = '%s' % (url_prefix)
data = None
if not sys.stdin.isatty():
    data = sys.stdin.readlines()

print (''.join(data))

r = requests.post(url, json={"datatype": "dotty", "data": ''.join(data)})

print (r)
js = json.loads(r.content)
id = js['uuid']
print (id)

url = '%s/%s/png' % (url_prefix,id)
print (url)
r = requests.get(url, stream=True)
print (r)
if r.status_code == 200:
    fname = 'output.png'

    with open(fname, 'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)
del r


url = '%s/%s/svg' % (url_prefix,id)
print (url)
r = requests.get(url, stream=True)
print (r)
if r.status_code == 200:
    fname = 'output.svg'

    with open(fname, 'wb') as out_file:
        shutil.copyfileobj(r.raw, out_file)
del r
