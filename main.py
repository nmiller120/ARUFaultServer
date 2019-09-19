# Senior Design Project, ARU Fault Server
# Nick Miller, Tim Dager
# Last Update: Dec, 2018
# Project Description:
#   The ARU Fault server runs as a daemon on the Rasberry Pi, this program
#   listens for a new fault code to be transmitted from the PLC, when a new
#   when a new fault is detected the fault is registered in memory. When a
#   request for the fault list is published on the MQTT broker the the sofware
#   publishes a response containing all fault data.


import RPi.GPIO as GPIO # implements an interface with the raspberry pi's GPIO
import time # used to keep track of event times
import const # module stores program constants
import threading # implements threading
import paho.mqtt.client as mqtt # implements MQTT protocol for this application
import socket # used to get this device's hostname
from ARU_Interface import * # implements the interface with the PLC controlling the air rotational unit

lastSavedTime = 0.0
statusOK = True # goes low when connection times out
ConnectedToBroker = False # goes high when connected to broker


def closeComms():
    # function used to close communication ports and gracefully shutdown the program
    global statusOK
    statusOK = False
    client.unsubscribe("aru_rqst")
    global ConnectedToBroker
    ConnectedToBroker = False
    aru.tearDown()
    print("Comms Closed")

def logWrite(filename, toWrite):
    # function writes data and events to specified log file, used to retain memory after
    # power cycle
    wFile = open(filename + '.log', 'a+')
    wFile.write(str(time.ctime()) + ':' + toWrite + "\n")
    wFile.close()

def blinkStatusLED(pin):
    # blink status LED, used to troubleshoot Pi, if LED is blinking the program is
    # probably running ok
    chirp = 0.05
    try:
        while statusOK:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(chirp)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(5)
    except RuntimeError:
        pass
    finally:
        print("Leaving status thread")

def publishFaultsONS(topic = "aru_periodic"):
    # function is called to publish all recorded fault data to the specified topic
    print("Publishing to topic: " + topic)
    response = ""
    endOfMsg = "endOfMsg"
    keyList = faultDict.keys()
    localLogSave = ""
    if(not faultDict):
        print("empty list")
        client.publish(topic, "No faults")
        client.publish(topic, endOfMsg)
    else:
        for key in keyList:
            response =  str(hex(key)) + ": "  + const.faultString[key] + "\n"
            print("publish: " + response)
            client.publish(topic, response)
            localLogSave = localLogSave + response
        client.publish(topic, endOfMsg)
        global lastSavedTime
        if(time.time() - lastSavedTime > 60*30):
            logWrite("faults", localLogSave)
            lastSavedTime = time.time()


def readMessage(client, userdata, msg):
    # implements the readMessage function required for the message_callback feature
    # of the MQTT library. When a message is published to the topic "aru_rqst"
    # a message containing fault data is published to the topic "aru_resp"
    rcvdCMD = str(msg.payload.decode("utf-8"))
    print("Recieved " + rcvdCMD + " on topic aru_rqst")
    if rcvdCMD == "get faults":
        publishFaultsONS("aru_resp")
    else:
        logWrite("access", rcvdCMD)

def on_disconnect(client, userdata, rc):
    # function called by MQTT library on disconnect, prints message to console and
    # closes out communications
    print("Lost connection to broker")
    statusOK = False
    closeComms()


# get the hostname of this device and attempt to contact the MQTT broker hosted
# on this device
hName = socket.gethostname()
print(hName)
broker =  hName

# client is this application
client = mqtt.Client("Python ARU")

faultDict = {} # dictionary to contain fault data
aru = ARU_Interface(faultDict) # aru interface object created to handle communication with PLC

GPIO.setup(const.statusLED, GPIO.OUT) # initialize status LED, blinks when good
GPIO.setup(const.errorLED, GPIO.OUT) # initialize error LED, red when no connection can be made


# This program begins running long before the MQTT broker starts, program keeps attempting a connection
# until either one is made or we run out of tries.
for x in range(60):
    try:
        # when a connection is made, the program does the following
        # - disables the error LED
        # - subscribes to topic aru_rqst
        # - adds a mesage callback to the client object that invokes the funciton
        # readMessage when a message is published to the topic aru_rqst
        # - provides a function to the MQTT client object to invoke on disconnect
        print("connection attempt " + str(x))
        print("broker is " + broker)
        client.connect(broker)
        client.loop_start()
        client.subscribe("aru_rqst")
        client.message_callback_add("aru_rqst", readMessage)
        client.on_disconnect =  on_disconnect
        print("connection sucsess")
        GPIO.output(const.errorLED, GPIO.LOW)
        ConnectedToBroker = True
        break
    except:
        # attempt a connection in couple seconds
        GPIO.output(const.errorLED, GPIO.HIGH)
        print("attempt failed")
        time.sleep(2)


# if a connection is made to the broker a thread is opened that blinks the LED
# the entire time this program runs
if ConnectedToBroker:
    status = threading.Thread(target = blinkStatusLED, args = (const.statusLED,))
    status.start()

# The rest of program is an infinite wait loop, handlers for PLC communication are
# implemented by the ARU_Interface object, handlers for fault data request are implemented
# by the MQTT.client object, status LED blinks in a separate thread
try:
    while ConnectedToBroker:
        pass


# if keyboard interupt or no longer connected to broker, close comms and end program
except KeyboardInterrupt:
    print("Session Interrupted")

finally:
    closeComms()
