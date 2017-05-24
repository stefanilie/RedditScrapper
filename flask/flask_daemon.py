import os
import sys
import pdb
import pprint
from flask import Flask, request

"""
This doesn't work using docker because it can't see the scrapper folder.
(Pdb) sys.path
[
    '/flask',
    '/usr/local/lib/python27.zip',
    '/usr/local/lib/python2.7',
    '/usr/local/lib/python2.7/plat-linux2',
    '/usr/local/lib/python2.7/lib-tk',
    '/usr/local/lib/python2.7/lib-old',
    '/usr/local/lib/python2.7/lib-dynload',
    '/usr/local/lib/python2.7/site-packages',
    '../scrapper/'
]

Need to make Docker access the files from scrapper folder.
"""
MYDIR = os.path.dirname(__file__)
pdb.set_trace()
sys.path.append(os.path.join(MYDIR, "../scrapper/"))

import scrapper


app = Flask(__name__)
scrapper = scrapper.Scrapper()

@app.route('/')
def hello_world():
    return "Ciorba de burta"

@app.route('/items/')
def stage_one():
    args = list(request.args)
    subreddit = request.args.get('subreddit')
    t1 = request.args.get('from')
    t2 = request.args.get('to')
    db = scrapper.db_connect()
    if len(args)==4:
        kwd = request.args.get('keyword')
        subs = scrapper.stage_one(subreddit, int(t1), int(t2), str(kwd))
        return pprint.pformat(subs, indent=4)
    elif len(args)==3:
        subs = scrapper.stage_one(subreddit, int(t1), int(t2))
        return pprint.pformat(subs, indent=4)
