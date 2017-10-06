# IoT Drone

## MAVLink

MAVLink a.k.a. Micro Air Vehicle Link is a protocol for communicating with drones (small unmanned vehicles). Its nature is a header-only marshaling library.
MAVLink has been originated in 2009. License - LGPL.
Also, MAVLink is a binary protocol.

MAVLink may use TCP, UDP or a serial port. It is at first used to connect GCS (Ground Control Station) to a drone.

If you choose MAVLink, you should generate a **dialect** for communication. A dialect should be arranged as an XML file of some specific format. Also, there are dialect files for well-known types of vehicles(e.g. pixhawk.xml).
From that XML file, MAVLink's Python scripts generate corresponding module. Available programming languages are:
* C
* C#
* Java
* JavaScript
* Lua 
* Python 2.7+

Python2 is literally MAVLink's "native" language and excellent to write a short script.

ser_pkt is an alternative. It's arranged as a C++ module. Not updated for 3 years. :(

## MAVLink libraries


### pymavlink

The most straightforward way to use MAVLink in Python is by pymavlink. But it has wrappers.

### MAVProxy

MAVProxy is a command line tool GCS. Not intended to be used as a module. pymavlink is its dependency.

The way it should be used:
```$ mavproxy.py --master=/dev/ttyUSB0```

### DroneKit

[DroneKit](http://dronekit.io/) may be used to deal with drones via MAVLink. Actually, another pymavlink's wrapper.
```python
import time
import dronekit

def handle(self, name, msg):
    print(msg)

vehicle = dronekit.connect(address="/dev/ttyUSB0")
vehicle.add_message_listener("HEARTBEAT", handle)
while True:
    time.sleep(1)
vehicle.close()
```

## How does it work

At one hand, there should be added handlers of some packet types (in this case, "ATTITUDE" and "OPTICAL_FLOW_RAD"). A packet type is a type of message from a drone. In a message it sends its state.

Thus, you don't have to flood your drone with requests: "what is the attitude?", "what's the distance?", your drone send its state as it refreshes.

## How should it be launched

### AWS backend
1. A DynamoDB table with partition key "mavpackettype" (type - String).
1. A Lambda instance to extract current drone's state. Example of code is located in "getDroneTelemetry" directory.
1. An API Gateway instance.

### DynamoDB refreshing script

1. virtualenv -p python2 venv
1. source venv/bin/activate
1. pip install -r requirements.txt
1. create ```.env``` file with ADDRESS (/dev/ttyUSB0, if you use USB-connected radio modem as we do), REGION (AWS region) and TABLE_NAME (name of your DynamoDB table) values
1. chmod +x script.py
1. ./script.py

When you need the script, just interrupt it ith ```Ctrl + C```.
