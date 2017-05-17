import json
import praw
import config
import time
import threading
import sched
import time
import SetInterval
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

# One of the first ways of trying to do the "refresh"
# Didn't work because - I think - it wasn't able to call the second time the
# method alongside it's parameters.
# File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 1082, in run
#       self.function(*self.args, **self.kwargs)
# TypeError: 'NoneType' object is not callable
def NOTUSED_set_interval(func, sec):
    pdb.set_trace()
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
    app = Flask(__name__)

    # Second way I tried to do the refresh. This time I tried sending all the parameters
    # also didn;t work with multiple parameters at once.
    # SetInterval(10, make_call, reddit, db_conn, "python")
    # try:
    #     sleep(35)
    # finally:
    #     thread.stop()
    # thread2 = set_interval(make_call(reddit, db_conn, "python"), 15)


    # Finally, I gave up and did a very stupid - though working - way of
    # handling this task.
    while True:
        time.sleep(10)
        make_call(reddit, db_conn, "python")
        time.sleep(50)

if __name__ == "__main__": main()
