import time


class TimestampHelper():

    def getTimestamp(self):
        return time.time()

    def getNanoSecondTimestamp(self):
        obj = time.gmtime(0)
        epoch = time.asctime(obj)
        nanoSec = time.time_ns()
        return nanoSec
