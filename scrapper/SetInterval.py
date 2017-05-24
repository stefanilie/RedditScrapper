from threading import Timer

# Class inspired from a stackoverflow thread, that for a while seemed to be a
# valid solution for my threading parameter issue. More than likely this is
# the right way to handle this problem. Will return to this to further investigate.
class SetInterval(object):
    def __init__(self, interval, function, *args, **kwargs):
        self.timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running(True)

    def stop(self):
        self._timer.cancel()
        self.is_running = False
