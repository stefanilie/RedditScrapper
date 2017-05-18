from flask import Flask
from flask import request
import scrapper

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Ciorba de burta"

@app.route('/items/')
def stage_one():
    subreddit = request.args.get('subreddit')
    t1 = request.args.get('from')
    t2 = request.args.get('to')
    db = scrapper.db_connect()
    subs = scrapper.stage_one(db, subreddit, int(t1), int(t2))
    return str(subs)

if __name__ == "__main__": main()
