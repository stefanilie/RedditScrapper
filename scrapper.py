import json
import praw
from praw.models import MoreComments
import config
import time
import threading
import sched
import time
import SetInterval
import datetime
import calendar
import pymongo
from pymongo import MongoClient

class Scrapper:
    def __init__(self):
        self.db_conn = self.db_connect()
        self.reddit = self.load_credentials()

    def load_credentials(self):
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
        print "i was here"
        return reddit


    def make_call(self, subreddit):
        try:
            #First, get the submisions for the last 2 days (for now...)
            past = datetime.datetime.utcnow() + datetime.timedelta(days=-2)
            past_ut = calendar.timegm(past.timetuple())
            arr_submissions = self.reddit.subreddit(subreddit).submissions(past_ut, int(time.time()))

            for sub in arr_submissions:
                print "\n\nTitle: ", sub.title
                submission = {
                    'id': sub.id,
                    'title': sub.title,
                    'selftext': sub.selftext,
                    'num_comments': sub.num_comments,
                    'created': int(sub.created),
                    'subreddit': subreddit
                }
                result = self.insert_submission(submission)
                print "Insert result: ", result
                for comment in sub.comments.list():
                    if not isinstance(comment, MoreComments):
                        comm = {
                            'id': comment.id,
                            'body': comment.body,
                            'sub_id': sub.id,
                            'subreddit': subreddit,
                            'created': int(comment.created)
                        }
                        result = self.insert_comment(comm)
                        print "Comment insert result: ", result
        except Exception as e:
            print e.message

    def stage_one(self, subreddit, t1, t2, kwd=None):
        if kwd is not None:
            # subs = db.Submissions.find({'subreddit': subreddit, "created": {"$gt": int(t1), "$lt": int(t2)}}, {"$text": {"$search": str(kwd)}})
            subs = self.db_conn.Submissions.find({'subreddit': subreddit, "created": {"$gt": int(t1), "$lt": int(t2)}, "$text": {"$search": str(kwd)}})
            comms = self.db_conn.Comments.find({'subreddit': subreddit, "created": {"$gt": int(t1), "$lt": int(t2)}, "$text": {"$search": str(kwd)}})
            return list(subs)+list(comms)
        else:
            comms = self.db_conn.Comments.find({'subreddit': subreddit, "created": {"$gt": int(t1), "$lt": int(t2)}})
            subs = self.db_conn.Submissions.find({'subreddit': subreddit, "created": {"$gt": int(t1), "$lt": int(t2)}})
            return list(subs)+list(comms)

    def insert_submission(self, submission):
        if self.db_conn.Submissions.find_one({'id': submission['id']}):
            print "submission already exists"
            return submission['id']
        else:
            result = self.db_conn.Submissions.insert_one(submission)
            return result

    def insert_comment(self, comment):
        if self.db_conn.Comments.find_one({'id': comment['id']}):
            print "comment already exists"
            return comment['id']
        else:
            result = self.db_conn.Comments.insert_one(comment)
            return result

    def index_comments(self):
        self.db_conn.Submissions.create_index([("title", pymongo.TEXT), ("created", pymongo.ASCENDING)], name="submissions_index")
        self.db_conn.Comments.create_index([("body", pymongo.TEXT), ("created", pymongo.ASCENDING)], name="comment_index")

    def db_connect(self):
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

    def cleanDB(self):
        self.db_conn.Comments.remove({})
        self.db_conn.Submissions.remove({})
