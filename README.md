# ARU Fault Server

The intent of the project is to design an alarm server for a PLC that is accessable to any IP network connected device using 
the MQTT protocol. This project was developed as part of my Senior Design Project that was sponsored by General Motors. The basic operation of this server is the following...
 - The server listens for a new fault code to be transmitted from the PLC
 - When a new fault is detected the fault is registered in memory and added to a datalog
 - When a request for the list of current faults is seen on the MQTT broker, the server publishes the current faults to the broker for 
 all connected devices to see
 - If the PLC requests to remove a fault, it is removed from the fault log
 
## Interface Between PLC and Pi

### Communication 
We were somewhat limited with what we could do with the communication link between the PLC and the Raspberry Pi. We did not have the budget to purchase a PLC to work with, we were not allowed to run code on the plant IP network and, we were not allowed to wire any physical connections between our Pi and the PLC for testing purposes. The solution we came up with involved creating a simple communication protocol by passing bits between the PLC and Pi using each device's discrete I/O. The protocol works as described below...
- The PLC provides 6 discrete outputs that are to be recieved by the Raspberry Pi via the Pi's general purpose I/O.
- 5 of these outputs are used to encode a 5 bit value that is to be read by the Pi. This value represents a fault code.
- 1 of the outputs is used as a latch bit. When this bit goes high it signals to the pi that the 5-bit fault code is ready to be read. If the code is not in the Pi's log, it is added and timestamped. If the code is in the log, it is removed. 

### Level Shifting

The Discrete I/O of the PLC and the Raspberry Pi do not operate on the same voltage levels. AB Compactlogix PLCs operate on 24V logic levels and the Raspberry Pi operates on 3.3V logic levels. To solve this issue a level shifting circuit was designed so the two devices could exchange data without risking damage to the hardware. Two different circuits were designed, one to shift down from 24VDC to 3.3VDC and another to shift the logic up from 3.3VDC to 24VDC. 

This level shifting was achieved using a PC817C opto-isolator IC. When a voltage is applied to the input pins of this IC it lights an LED that transmits an optical signal that is read by a phototransistor within the IC package. When the phototransistor is saturated it allows current to flow between the output pins of the IC. The circuit designs are shown below. 

#### 3.3V to 24V Level Shifter

![3.3VDC to 24VDC Shifter](https://i.imgur.com/BRy7iPK.png)

#### 24V to 3.3V Level Shifter

![24V to 3.3V Shifter](https://i.imgur.com/n9rWjta.png)

## MQTT Protocol

The MQTT protocol works on a publish-subscribe system. IP hosts interact with a server called a "broker" that manages the exchange of messages between hosts. Clients connect to the broker and can subscribe to topics and view messages being sent to that topic, or the clients can publish messages themselves. In this project the fault server running on the Pi acts as both a publisher and subscriber. 

## Communication Between Raspberry Pi and Connected Devices

All devices connected to the MQTT broker hosted on the Raspberry Pi are able to recieve fault data published to the topic "aru_resp". The clients are also able to publish the message "get faults" to the topic "aru_rqst" and prompt the alarm server to publish it's fault data. MQTT client applications can easily be downloaded for free on Windows, Linux, and Mac, as well as on iOS and Android. So any device that is able to connect to the fault server is able to view the fault data. 

I have spent a lot of time commenting and adding documentation to the code for this project. I am trying to keep the code in
as readable of condition as possible. Feel free to read through the project files as they may shed light on some of the more technical 
details of the project not covered here. 

Thanks for reading!

### Additional Info:
Eclipse Mosqitto, MQTT Broker and desktop client: https://mosquitto.org/

