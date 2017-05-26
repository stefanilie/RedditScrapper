import time
import scrapper

def main():
    user_timestamp = raw_input("Please insert the date timestamp starting"+
                    " from you wish to start the scrapping: ")
    scrapperObj = scrapper.Scrapper()

    print "Running scrapper..."
    # scrapperObj.cleanDB()
    """
    Second way I tried to do the refresh.
    This time I tried sending all parameters, also didn't work with multiple
    parameters at once.

    SetInterval(10, make_call, reddit, db_conn, "python")
    try:
        sleep(35)
    finally:
        thread.stop()
    thread2 = set_interval(make_call(reddit, db_conn, "python"), 15)


    Finally, I gave up and did a very stupid - though working - way of
    handling this task.
    """
    while True:
        for sub in scrapperObj.subreddits:
            scrapperObj.make_call(sub, int(user_timestamp))
        time.sleep(120)

if __name__ == "__main__": main()
