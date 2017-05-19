from scrapper import Scrapper
import time

def main():
    scrapperObj = Scrapper()
    scrapperObj.make_call("python")
    # scrapperObj.make_call("romania")
    # reddit = load_credentials()
    # db_conn = db_connect()
    # scrapperObj.index_comments(scrapperObj.db_conn)
    # cleanDB(db_conn)

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
    # while True:
    #     time.sleep(10)
    #     scrapperObj.make_call(reddit, db_conn, "python")
    #     scrapperObj.make_call(reddit, db_conn, "romania")
    #     time.sleep(50)

if __name__ == "__main__": main()
