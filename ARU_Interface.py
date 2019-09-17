# module defines a single class ARU_Interface, this class handles the communication
# between the PLC and the raspberry pi. The interface needed to be very basic because
# we did not have access to a PLC to test with and we were not allowed to run software
# on GMs network.The solution we went with involved 5 bits being transmitted via
# 5 separate discrete outputs on the PLC and recieved by the raspberry pis GPIO.
# One extra discrete output was provided by the PLC the we denote as the latch pin.
# When this latch pin goes high it signals to the raspberry pi that it is currently
# providing to the pi a fault to be logged. Each fault needs provided separately and
# to remove a fault the PLC is to resend a fault code.

import const
from LatchTimer import *  # handles timing of the latch bit
import RPi.GPIO as GPIO

class ARU_Interface:
    latch = None # latchTimer object
    faultDict = {} # list of faults

    def __init__(self, faultDict):
        # init latchTimer with debounce time of 1 second
        self.latch = LatchTimer(1000)

        # init fault dictionary
        self.faultDict = faultDict

        #setup latch bit as discrete input with pullup resistor
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(const.latchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # setup listener for when latch pin on falling edge
        GPIO.add_event_detect(const.latchPin, GPIO.FALLING, self.latchHandler)

        # setup fault code bits as inputs
        for x in range(len(const.faultPin)):
            GPIO.setup(const.faultPin[x], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def readFault(self):
        # decodes the fault based on the state of the discrete inputs transmitted
        # by PLC. Registers the fault in the program
        faultCode = 0
        y = len(const.faultPin) - 1
        for x in range(len(const.faultPin)):
            reading = int(not GPIO.input(const.faultPin[x]))
            faultCode += reading * (2**y)
            y -= 1
        return faultCode

    def tearDown(self):
        # invoked when the program ends, releases control of GPIO
        GPIO.cleanup()

    def latchHandler(self, pin):
        # method is invoked when latch bit goes high, if the latch pin is low
        # and is debounced, read the fault into the faultDict
        if not GPIO.input(const.latchPin) and self.latch.checkBounce():
            fault = self.readFault()
            if fault in self.faultDict:
                del self.faultDict[fault]
            else:
                self.faultDict.update({fault:time.ctime()})
            print(self.faultDict)
