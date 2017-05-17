from flask import Flask
from pymongo import MongoClient
import scrapper

db_conn = MongoClient()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Ciorba de burta"

def main():
    db_conn = scrapper.db_connect()


if __name__ == "__main__": main()
