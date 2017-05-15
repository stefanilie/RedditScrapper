import json
import config

def load_credentials():
    with open("passwords/accounts.json") as json_data:
        d = json.load(json_data)
        config.CLIENT_ID = d["client_id"]
        config.PASSWORD = d["password"]
        config.APP_ID = d["app_id"]
        config.APP_SECRET = d["app_secret"]

load_credentials()
print config.APP_ID
print config.APP_SECRET
