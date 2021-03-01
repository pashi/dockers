from treelib import Node, Tree
from graphviz import Digraph, Graph
import json, base64
import requests
import shutil
import argparse, os

def read_json_data(fname):
    try:
        with open(fname, 'r') as f:
            data = json.load(f)
            return data
    except:
        pass
    return []

map_keys = {}
noden = 0
def get_key(name, k=None):
    global noden
    r = name
    # if request key is some of defined key
    for x in map_keys:
        if map_keys [x] == name:
            return name
    
    # if user predefined key
    if not k == None:
        r = k
        map_keys [ name ] = r
    elif not name in map_keys:
        r = "node%s" % (noden)
        noden += 1
        map_keys [ name ] = r
    else:
        r = map_keys [ name ]
    return r

cnt=1
def get_subgraph_name():
    global cnt
    name = "cluster_%s" % (cnt)
    cnt += 1
    return name


def recursive(p,d=0,label=None):

    name = "main"
    if d > 0:
        name = get_subgraph_name()
    comment = "depth %s" % (d)
    dot = Digraph(name=name, comment=comment)
    if not label == None:
        dot.attr(label=label)
    if type(p).__name__ == 'dict':
        for k in p:
            dot.label = k
            v = p[k]
            if 'children' in v:
                s = recursive(v['children'],(d+1), k)
                dot.subgraph(s)
    elif type(p).__name__ == 'list':
        for x in p:
            if type(x).__name__ == 'str':
                n_key = get_key(x)
                dot.node(n_key, label=x)
                continue
            for k in x:
                #n_key = get_key(k)
                #dot.node(n_key, label=k)
                v = x[k]
                if 'children' in v:
                    s = recursive(v['children'],(d+1),k)
                    dot.subgraph(s)

    return dot

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--json', help='filename')
    parser.add_argument('--dotoutput', help='filename')
    parser.add_argument('--pngoutput', help='filename', default='output.png')
    url_prefix = os.getenv('URL_PREFIX')
    parser.add_argument('--url', help='filename', default=url_prefix)


    args = parser.parse_args()

    tree = Tree()

    data = read_json_data(args.json)
    if 'nodes' in data:
        for x in data [ 'nodes' ]:
            name = x['name']
            key = ''
            parent = None
            if 'key' in x:
                key = get_key(name,x['key'])
            else:
                key = get_key(name)
            if 'parent' in x:
                parent = get_key(x['parent'])
                #print (name, key, parent, x['parent'])
            tree.create_node(name, key, parent)
    print (map_keys)
    tree.show()
    x = recursive(tree.to_dict())
    if 'edges' in data:
        for d in data [ 'edges' ]:
            src = get_key(d['src'])
            dst = get_key(d['dst'])
            color = 'black'
            if 'color' in d:
                color = d [ 'color' ]
            x.edge(src,dst, color=color)
    #print (x.source)
    if args.dotoutput:
    #print (json.dumps(data))
        with open(args.dotoutput, 'w') as f:
            f.write(x.source)
    if args.url:
        url = '%s' % (args.url)
        r = requests.post(url, json={"datatype": "dotty", "data": x.source})
        js = json.loads(r.content)
        id = js['uuid']
        url = '%s/%s/png' % (args.url,id)
        print (url)
        r = requests.get(url, stream=True)
        print (r)
        if r.status_code == 200:
            with open(args.pngoutput, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)


if __name__ == "__main__":
    main()
