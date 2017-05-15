import json
import praw
import config

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
        subreddit = reddit.subreddit("python")
        print "Display name: ",subreddit.display_name
        print "Title: ", subreddit.title
        print "Description: ", subreddit.description
    except Exception as e:
        print e.message

load_credentials()
make_call()
