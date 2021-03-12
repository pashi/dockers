import feedparser
import json
import os, time
from datetime import date
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

# xx
# * FEED_URL
# * MAX_DAYS
# * AZURE_BLOB
# * AZURE_PATH

url = os.getenv("URL")
max_days = os.getenv("MAX_DAYS")
x = 0
try:
    x = int (max_days)
except:
    pass
# how old feed posts we handle
max_age = 60 * 60 * 24 * x

time_now = time.time()
after_time = 1

if max_age > 0:
    after_time = time_now - max_age

use_azure_blob = False

def write_json(fname,data, indent=0):
    try:
        with open(fname, 'w') as f:
            json.dump(data, f, indent=indent)
    except:
        pass

def write_to_blob(fname):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container="data", blob=fname)
    with open(fname, "rb") as data:
        blob_client.upload_blob(data, blob_type="BlockBlob", overwrite=True)

def read_json_data(fname):
    try:
        with open(fname, 'r') as f:
            data = json.load(f)
            return data
    except:
        pass
    return []


def read_rss(url):
    global use_azure_blob

    feedfilename = 'feed.json'

    tp = {}
    feed = []
    try:
        feed = feedparser.parse( url )
    except:
        pass
    write_json(feedfilename, feed, 2)
    #if use_azure_blob == True:
    #    write_to_blob(feedfilename)
    if ('entries' in feed):
        ## edit here if you would like to change some fields what to store
        xx = ['id', 'link','title','summary','published_parsed']
        for entry in feed['entries']:
            d = {}
            for x in xx:
                d[x] = getattr(entry, x, None)
            d_tp = time.strftime("%Y%m", d['published_parsed'])
            #d['timepartition'] = d_tp
            ts = time.strftime("%s", d['published_parsed'])
            d['ts'] = int(ts)
            if int(ts) < after_time:
                continue

            if not d_tp in tp:
                tp[d_tp] = []
            tp[d_tp].append(d)
    del feed
    return tp

def read_tp_data(tp):
    data = read_json_data('data.%s.json' % (tp))
    return data



def get_old_tp_data(tp):
    return read_tp_data(tp)



def get_distinct(aa,bb):
    k = {}
    data = []
    for a in aa:
        n = '%s-%s' % (a['ts'],a['id'])
        k[n] = True
        data.append(a)
    for b in bb:
        n = '%s-%s' % (b['ts'],b['id'])
        if not n in k:
            data.append(b)
            k[n] = True
    return data

rss_data = read_rss(url)
write_json('rss.json', rss_data, 2)

d = {}
for time_partition in sorted(rss_data.keys(), reverse=False):
    old_rss = get_old_tp_data(time_partition)
    new_rss = rss_data[time_partition]
    data = get_distinct(old_rss,new_rss)
    fname = 'data.%s.json' % (time_partition)
    write_json(fname, data, 2)



#print (rss_data)