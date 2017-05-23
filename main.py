import time
import scrapper

def main():
    scrapperObj = scrapper.Scrapper()
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
        time.sleep(20)
        scrapperObj.make_call("python")
        scrapperObj.make_call("romania")
        time.sleep(100)

if __name__ == "__main__": main()
