import sys
import pprint
from flask import Flask, request

sys.path.append('../scrapper/')
from scrapper import Scrapper


app = Flask(__name__)
scrapper = Scrapper()

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
