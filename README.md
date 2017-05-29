RedditScrapper
==============

Python application gathering data from subreddits and offering it through an
Flask based endpoint.


About
----

The application uses a python script to gather all data and stores it in
a MongoDB database.

The user can get the data in JSON format, by accessing an
endpoint.



Usage
-----
First up, we need to clone the project

`git clone https://github.com/stefanilie/RedditScrapper.git`

You also have to install all the dependencies. So for that, `cd scrapper/ && pip install -r requirements.txt`

Second step, we need to start up the MongoDB Daemon: `mongod --dbpath RedditScrapper/scrapper/data/db`

Please pay attention to where you have your MongoDB instance
installed locally. Usually it's `/data/db`

Prior to starting the scrapper, you need to decide what subreddits you want to scrap.
You can do this by editing the `input.py` file, that can be found in `/scrapper`

Then, we have to start up the scrapper by: `python main.py`

In a separate terminal window, we need to start up the Flask daemon.
First up though, we need to

`cd ../flask && export FLASK_APP=flask_daemon.py`

After that, we simply have to `flask run`

From then on, you can simply access

`http://127.0.0.1:5000/items/?subreddit=SUBREDDIT&from=T1&to=T2&keyword=KWD`

where `SUBREDDIT` is the subreddit you want to browse, `T1` and `T2` are the timestamps between which you want to search, and `KWD` is the keyword you want to look for (if you want to).
