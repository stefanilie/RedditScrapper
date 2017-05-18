from flask import Flask
from flask import request
import scrapper

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Ciorba de burta"

@app.route('/items/')
def stage_one():
    args = list(request.args)
    if len(args)==4:
        subreddit = request.args.get('subreddit')
        t1 = request.args.get('from')
        t2 = request.args.get('to')
        kwd = request.args.get('keyword')
        db = scrapper.db_connect()
        subs = scrapper.stage_one(db, subreddit, int(t1), int(t2), str(kwd))
        return str(subs)
    elif len(args)==3:
        subreddit = request.args.get('subreddit')
        t1 = request.args.get('from')
        t2 = request.args.get('to')
        db = scrapper.db_connect()
        subs = scrapper.stage_one(db, subreddit, int(t1), int(t2))
        return str(subs)


if __name__ == "__main__": main()
