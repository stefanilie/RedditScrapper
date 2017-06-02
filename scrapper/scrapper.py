import os
import sys
import json
import praw
import time
import sched
import config
import pymongo
import calendar
import datetime
import threading

import SetInterval


class Scrapper:
    def __init__(self):
        config.MYDIR = os.path.dirname(__file__)
        self.db_conn = self.db_connect()
        self.reddit = self.load_credentials()
        self.subreddits = self.load_input()

    def load_input(self):
        """
        Loads the list of to be analysed subreddits.

        :return: string array of subreddits.
        :return type: array
        """
        with open(os.path.join(config.MYDIR, "input.json")) as json_data:
            d = json.load(json_data)
            return d["subreddits"]


    def load_credentials(self):
        """
        Authenticates the application with reddit servers.
        In order to do this, it gathers all the credentials needed for
        the process from the accounts.json file.
        The accounts file is part of the .gitignore file, due to security and
        best practice reasons.

        :return: praw object with which all the API calls are later made.
        :return: type JSON object
        """
        # TO DO: Catch exeption for missing credential field
        with open(os.path.join(config.MYDIR, "passwords/accounts.json")) as json_data:
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

    def db_connect(self):
        """
        Connects the application to the existing MongoDB daemon.

        :return: MongoDB db instance.
        """
        try:
            client = pymongo.MongoClient()
            db = client.reddit
            return db
        except Exception as e:
            print e.message

    def make_call(self, subreddit, timestamp):
        """
        The backbone of the application. Using the praw object, it calls
        certain methods from the reddit public API. First, we get the submissions
        from one subreddit, insert them into the db and after it does the same
        for the comments.

        :param subreddit: the name of the subreddit we want to scrap data from
        :param subreddit type: string

        :return: True if everything goes well, False if errors are encountered.
        """
        try:
            subreddit.decode('ascii')

            past = datetime.datetime.now() + datetime.timedelta(days=-2)
            past_ut = calendar.timegm(past.timetuple())
            arr_submissions = self.reddit.subreddit(subreddit).submissions(
                int(timestamp), int(time.time())
            )

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
                    if not isinstance(comment, praw.models.MoreComments):
                        comm = {
                            'id': comment.id,
                            'body': comment.body,
                            'sub_id': sub.id,
                            'subreddit': subreddit,
                            'created': int(comment.created)
                        }
                        result = self.insert_comment(comm)
                        print "Comment insert result: ", result
            return True
        except UnicodeDecodeError:
            print "it was not a ascii-encoded unicode string"
            return False
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return False

    def stage_one(self, subreddit, t1, t2, kwd=None):
        """
        Created in the first place to handle the requirements from stage one,
        it also later developed a way to handle both the stages.
        For three parameters, it queries the DB for all the submissions
        between t1 and t2 (timestamps) in the provided subreddit.
        In the case of four parameters, it searches also for a certain keyword.

        :param subreddit: name of subreddit by which to search submissions/comments
        :param subreddit type: string

        :param t1: timestamp from when it can start looking for
        :param t1 type: int (timestamp)

        :param t2: higher-limit timestamp
        :param t2: int (timestamp)

        :param kwd=None: keyword that returned posts contain
        :param kwd type: string

        :return: List of comments and submissions or False in case of bad params.
        """
        try:
            subreddit.decode('ascii')
            if isinstance(t1, int) and isinstance(t2, int):
                if kwd is not None:
                    kwd.decode('ascii')
                    subs = self.db_conn.Submissions.find({
                        'subreddit': subreddit,
                        "created": {
                            "$gt": int(t1),
                            "$lt": int(t2)
                        },
                        "$text": {"$search": str(kwd)}
                    })
                    comms = self.db_conn.Comments.find({
                        'subreddit': subreddit,
                        "created": {
                            "$gt": int(t1),
                            "$lt": int(t2)
                        },
                        "$text": {"$search": str(kwd)}
                    })
                    return list(subs)+list(comms)
                else:
                    comms = self.db_conn.Comments.find({
                        'subreddit': subreddit,
                        "created": {
                            "$gt": int(t1),
                            "$lt": int(t2)
                        }
                    })
                    subs = self.db_conn.Submissions.find({
                        'subreddit': subreddit,
                        "created": {
                            "$gt": int(t1),
                            "$lt": int(t2)
                        }
                    })
                    return list(subs)+list(comms)
            else:
                return False
        except UnicodeDecodeError:
            print "it was not a ascii-encoded unicode string"
            return False

    def insert_submission(self, submission):
        """
        Inserts a provided submission object into the Submissions collection.

        :param submission: item created from parsing a reddit api object
        :param submission type: JSON object

        :return: code for submission if it already exists, else InsertOneResult obj.
        :return type: InsertOneResult or string
        """
        if self.db_conn.Submissions.find_one({'id': submission['id']}):
            print "submission already exists"
            return submission['id']
        else:
            result = self.db_conn.Submissions.insert_one(submission)
            return result

    def insert_comment(self, comment):
        """
        Inserts the provided comment object in the Comments collection.

        :param comment: comment created with the structure from make_call.
        :param comment type: JSON object

        :return: code for comment if it already exists, else InsertOneResult obj.
        :return type: InsertOneResult or string
        """
        if self.db_conn.Comments.find_one({'id': comment['id']}):
            print "comment already exists"
            return comment['id']
        else:
            result = self.db_conn.Comments.insert_one(comment)
            return result

    def index_comments(self):
        """
        Indexes the comments in order to provide a way to search for keywords.
        Uses default MongoDB indexer.
        """
        self.db_conn.Submissions.create_index(
            [
                ("title", pymongo.TEXT),
                ("created", pymongo.ASCENDING)
            ],
            name="submissions_index"
        )
        self.db_conn.Comments.create_index(
            [
                ("body", pymongo.TEXT),
                ("created", pymongo.ASCENDING)
            ],
            name="comment_index"
        )

    def NOTUSED_set_interval(func, sec):
        """
        One of the first ways of trying to do the "refresh"
        Didn't work because - I think - it wasn't able to call the second time the
        method alongside it's parameters.
        File "/System/Library/Frameworks/Python.framework/Versions/
            2.7/lib/python2.7/threading.py", line 1082, in run
              self.function(*self.args, **self.kwargs)
        TypeError: 'NoneType' object is not callable
        """
        def function_wrapper():
            set_interval(func, sec)
            func()
        t = threading.Timer(sec, function_wrapper)
        t.start()
        return t

    def cleanDB(self):
        """
        Deletes all data from the DB.
        """
        self.db_conn.Comments.remove({})
        self.db_conn.Submissions.remove({})
