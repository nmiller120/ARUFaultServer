# ARU Fault Server

The intent of the project is to maintain a simple alarm server for a PLC that is accessable to any IP network connected device using 
the MQTT protocol. The basic operation of this server is the following...
 - The server listens for a new fault code to be transmitted from the PLC
 - When a new fault is detected the fault is registered in memory and added to a datalog
 - When a request for the list of current faults is seen on the MQTT broker, the server publishes the current faults to the broker for 
 all connected devices to see
 - If the PLC requests to remove a fault, it is removed from the fault log
 
I have spent a lot of time commenting and adding documentation to the code for this project. I am trying to keep the code in
as readable of condition as possible. Feel free to read through the project files as they may shed light on some of the more technical 
details of the project not covered here. 

Thanks for reading!
