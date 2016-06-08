---
layout: post
title: "Mimicking udev rules with PySerial"
description: "Because unfortunately Windows"
category: Programming
tags: [python, serial, experimental automation]
---
{% include JB/setup %}

My research group in grad school had an unfortunate culture of stealing equipment from
other people's experiments when they weren't around. I participated in this culture as well,
 but I tried to replace the things I took before they returned. However, this did not
 spare me from the ire of a Postdoc[^1] who pointed out that windows assigns
  device names by serial number, thus my replacing a power meter with an identical
  copy had caused him an hour of debugging time until he opened up the device manager.

Later, out of grad school and working on robots with even more hardware, I discovered
the joy of writing udev rules and spared myself many hours of plugging in usb cables to
see what they enumerate as.

I'm now out of robotics and back in experimental physics. Most
experimental physicists aren't linux users, so a lot of scientific equipment is sold with
 drivers which are only functional on Windows.

I had reverted back to plugging and unplugging cables, until the other experimental
physicist at work switched out the hardware in my experimental setup overnight. After
I had calmed down, decided to find another way.

Here's my solution. [PySerial](http://pyserial.readthedocs.io/) has a lovely tool
called *list_ports* which will list a
 bunch of handy information about the available com ports. By matching the vendor and
 product IDs, (or in the case of devices that both use the FTDI FT232R chip, also the 
 serial number) I can guess the devices:


```
from serial import Serial
from serial.tools import list_ports

# hardware is represented as a tuple of (vid, pid, serial_number (if needed), baud_rate)
HARDWARE = {'temperature_controller': (1027, 24577, 'serial1', 115200),
            'counter': (1027, 24577, 'serial2', 19200),
            'motor_controller': (5824, 1155, 9600),
            'laser': (10682, 2, 115200)}

def map_hardware():
    com_ports = dict()
    for key, value in HARDWARE_IDS.items():
        found_port = False
        for port in list_ports.comports():
            if len(value) > 3:
                if port.vid == value[0] and port.pid == value[1] and port.serial_number == value[2]:
                   found_port = True
                   com_ports[key] = port.device
                   break
            else:
                if port.vid == value[0] and port.pid == value[1]:
                   found_port = True
                   com_ports[key] = port.device
                   break
        if not found_port:
            raise RuntimeError("device matching ids for key: ", key, " not found")
    return com_ports

ports = map_hardware()
handles = dict()

for key in ports.keys():
    handles[key] = Serial(ports[key], HARDWARE[key][-1])
```

This is a simplification. I import modules from [InstrumentKit](https://github.com/Galvant/InstrumentKit) to
 do the actual communication rather than writing the commands directly to the handles.

[^1]: Brendon, if you're reading, I'm still sorry about this.
