import json
import praw
import config
from pymongo import MongoClient

def load_credentials():
    with open("passwords/accounts.json") as json_data:
        d = json.load(json_data)
        config.CLIENT_ID = d["client_id"]
        config.CLIENT_SECRET = d["client_secret"]
        config.USERNAME = d["username"]
        config.PASSWORD = d["password"]
        config.USER_AGENT = d["user_agent"]

def make_call():
    try:
        reddit = praw.Reddit(client_id = config.CLIENT_ID,
                            client_secret = config.CLIENT_SECRET,
                            user_agent = config.USER_AGENT,
                            username = config.USERNAME,
                            password = config.PASSWORD)
        #First, get the submisions for the last 2 hours (of today... for now.)
        submisions = reddit.subreddit("python").submissions(1494844431, 1494851631)
        for sub in submisions:
            print sub.title
    except Exception as e:
        print e.message

def db_connect():
    try:
        client = MongoClient()
        db = client.test
    except Exception as e:
        print e.message



load_credentials()
make_call()
# db_connect()
# make_call()
