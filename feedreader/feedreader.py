import feedparser
import json, csv
import os, time, glob, logging, sys, datetime
from datetime import date
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import azure.core

# xx
# * FEED_URL
# * MAX_DAYS
# * AZURE_BLOB
# * AZURE_PATH

url = os.getenv("URL")
max_days = os.getenv("MAX_DAYS")
azure_blob = os.getenv("AZURE_BLOB")
azure_blob_container = os.getenv("AZURE_BLOB_CONTAINER")
clean_workdir = os.getenv("CLEAN_WORKDIR")
debug = os.getenv("DEBUG")

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
if not azure_blob == None and not azure_blob == '':
    use_azure_blob = True

if clean_workdir == '1' or clean_workdir == 'True':
    clean_workdir = True
else:
    clean_workdir = False

if debug == '1' or debug == 'True':
    debug = True
else:
    debug = False

if azure_blob_container == None or azure_blob_container == '':
    azure_blob_container = 'data'


read_from_blob = True

## logging start ##
loglevel = logging.INFO
if debug:
    loglevel = logging.DEBUG

logger = logging.getLogger('feedreader')
logger.setLevel(loglevel)
ch = logging.StreamHandler()
ch.setLevel(loglevel)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
## logging end ##

timetup = time.gmtime()
processtime = time.strftime('%Y%m%dT%H%M%S', timetup)
feedfilename = 'feed.%s.json' % (processtime)
rssfilename = 'rss.%s.json' % (processtime)
logger.debug('feedfilename:%s' % (feedfilename))

def write_json(fname,data, indent=0):
    logger.debug('write_json:%s' % (fname))
    try:
        with open(fname, 'w') as f:
            json.dump(data, f, indent=indent)
    except:
        pass

def write_csv(fname,data):
    logger.debug('write_csv:%s' % (fname))
    #try:
    with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=';',quotechar='|',quoting=csv.QUOTE_MINIMAL)
            fieldnames = ['ts', 'id', 'link', 'title', 'summary','tags']
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';',quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for item in data:
                dt = datetime.datetime.utcfromtimestamp(item['ts'])
                iso_format = dt.isoformat() + 'Z'
                item['ts'] = iso_format
                del item['published_parsed']
                if len(item['tags']) > 0:
                    item['tags'] = ','.join(item['tags'])
                else:
                    item['tags'] = ''
                writer.writerow(item)
    #except:
    #    pass

def get_blob_client(fname):
    blob_service_client = BlobServiceClient.from_connection_string(azure_blob)
    blob_client = blob_service_client.get_blob_client(container=azure_blob_container, blob=fname)
    return blob_client

def upload_blob(fname):
    blob_client = get_blob_client(fname)
    content_type = None
    x,y = os.path.splitext(fname)
    if y == '.json':
        content_type = 'application/json'
    elif y == '.csv':
        content_type = 'text/csv'
    with open(fname, "rb") as data:
        blob_client.upload_blob(data, blob_type="BlockBlob", overwrite=True, content_type=content_type)

def download_blob(fname):
    try:
        blob_client = get_blob_client(fname)
        with open(fname, "wb") as data:
            download_stream = blob_client.download_blob()
            data.write(download_stream.readall())
    except azure.core.exceptions.ResourceNotFoundError:
        # no blob found.. continue
        logger.warning('download_blob:not_found:%s' % (fname))

def read_json_data(fname):
    logger.debug('read_json_data:%s' % (fname))

    if read_from_blob:
        logger.debug('read_json_data:read_from_blob:%s' % (fname))
        download_blob(fname)
    try:
        with open(fname, 'r') as f:
            data = json.load(f)
            return data
    except:
        logger.debug('read_json_data:%s:failed' % (fname))
        pass
    return []


def read_rss(url):
    global use_azure_blob

    tp = {}
    feed = []
    try:
        feed = feedparser.parse( url )
    except:
        logger.debug('read_rss:FAIL:%s' % (url))
        pass
    write_json(feedfilename, feed, 2)
    if ('entries' in feed):
        ## edit here if you would like to change some fields what to store
        xx = ['id', 'link','title','summary','published_parsed']
        for entry in feed['entries']:
            d = {'tags':[]}
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
            if 'tags' in entry:
                tag_list = {}
                for tag in entry['tags']:
                    if 'term' in tag:
                        t_tag_name = tag['term']
                        for t_k in t_tag_name.split(';'):
                            t_k_fixed = t_k.strip().lower()
                            if not t_k_fixed == '':
                                tag_list[t_k_fixed] = True
                d['tags'] = sorted(list(tag_list.keys()))

            tp[d_tp].append(d)
    del feed
    return tp

def read_tp_data(tp):
    data = read_json_data('data.%s.json' % (tp))
    return data



def get_old_tp_data(tp):
    return read_tp_data(tp)

def remove_temp_files():
    for f in ['feed','data','rss']:
        x = glob.glob('%s.*.json' % (f))
        for z in x:
            os.remove(z)

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

if clean_workdir:
    remove_temp_files()



rss_data = read_rss(url)
write_json(rssfilename, rss_data, 2)

d = {}
files_to_upload = [ rssfilename, feedfilename ]
for time_partition in sorted(rss_data.keys(), reverse=False):
    old_rss = get_old_tp_data(time_partition)
    new_rss = rss_data[time_partition]
    data = get_distinct(old_rss,new_rss)
    fname = 'data.%s.json' % (time_partition)
    cfname = 'data.%s.csv' % (time_partition)
    write_json(fname, data, 2)
    write_csv(cfname,data)
    files_to_upload.append(fname)
    files_to_upload.append(cfname)

if use_azure_blob:
    x = glob.glob('data.*.json')
    for f in x:
        files_to_upload.append(f)

    for f in files_to_upload:
        logger.debug('upload:%s' % (f))
        upload_blob(f)

#print (rss_data)