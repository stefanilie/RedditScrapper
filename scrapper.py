import json
import praw
import config
import time
import threading
from pymongo import MongoClient

def load_credentials():
    with open("passwords/accounts.json") as json_data:
        d = json.load(json_data)
        config.CLIENT_ID = d["client_id"]
        config.CLIENT_SECRET = d["client_secret"]
        config.USERNAME = d["username"]
        config.PASSWORD = d["password"]
        config.USER_AGENT = d["user_agent"]

    reddit = praw.Reddit(client_id = config.CLIENT_ID,
                        client_secret = config.CLIENT_SECRET,
                        user_agent = config.USER_AGENT,
                        username = config.USERNAME,
                        password = config.PASSWORD)
    return reddit


def make_call(reddit, db_conn, subreddit):
    try:
        #First, get the submisions for the last 2 hours (of today... for now.)
        arr_submissions = reddit.subreddit(subreddit).submissions(1494844431, 1494851631)

        for sub in arr_submissions:
            print "\n\nTitle: ", sub.title
            submission = {
                'id': sub.id,
                'title': sub.title,
                'selftext': sub.selftext,
                'num_comments': sub.num_comments,
                'created': time.time(),
                'subreddit': subreddit
            }
            result = insert_submission(db_conn, submission)
            print "Insert result: ", result
            for comment in sub.comments.list():
                comm = {
                    'id': comment.id,
                    'body': comment.body,
                    'sub_id': sub.id
                }
                result = insert_comment(db_conn, comm)
                print "Comment insert result: ", result
    except Exception as e:
        print e.message

def insert_submission(db, submission):
    if db.Submissions.find_one({'id': submission['id']}):
        print "submission already exists"
        return submission['id']
    else:
        result = db.Submissions.insert_one(submission)
        return result

def insert_comment(db, comment):
    if db.Comments.find_one({'id': comment['id']}):
        print "comment already exists"
        return comment['id']
    else:
        result = db.Comments.insert_one(comment)
        return result

def db_connect():
    try:
        client = MongoClient()
        db = client.reddit
        return db
    except Exception as e:
        print e.message

def set_interval(func, sec):
    def function_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, function_wrapper)
    t.start()
    return t

def cleanDB(db):
    db.Comments.remove({})
    db.Submissions.remove({})


def main():
    reddit = load_credentials()
    db_conn = db_connect()
    cleanDB(db_conn)
    thread = set_interval(make_call(reddit, db_conn, "python"), 10)
    # thread2 = set_interval(make_call(reddit, db_conn, "python"), 15)

    # make_call(reddit, db_conn, "python")


if __name__ == "__main__": main()
