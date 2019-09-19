# Module Description: 
# Module defines a single class LatchTimer that helps debounce the latch bit,
# and keeps track of the time since the last latch. We did not have access to a
# PLC to implement this project so we improvised using manual switches that
# require a long debounce time.

import time

class LatchTimer:
    lastLatch = None # time of last latch
    bounce = None # time required between valid latches

    def __init__(self, bounceTime):
        self.bounce = bounceTime
        self.lastLatch = self.millis()


    def millis(self):
        # return milliseconds since epoch
        return int(round(time.time() * 1000))

    def checkBounce(self):
        # returns true if this function was NOT called during a bounce timeout, 
        # returns false if this function was called during a bounce timeout. 
        latchTime = self.millis()
        difference = latchTime - self.lastLatch
        self.lastLatch = latchTime
        if (difference > self.bounce): 
            return True
        else:
            return False




