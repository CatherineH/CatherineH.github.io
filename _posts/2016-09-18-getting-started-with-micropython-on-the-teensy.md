---
layout: post
title: "Getting Started with MicroPython on the Teensy"
description: "first steps"
category: programming
tags: [python, teensy, micropython, embedded]
---
{% include JB/setup %}

This morning I was able to compile and upload micropython and my first 
*main.py* to the [Teensy 3.2](https://www.pjrc.com/teensy/) development 
board. Once micropython was compiled and uploaded, it wasn't too much 
effort to get my teensy to drive the upper matrix of an Adafruit 9x16 
charlieplexed LED matrix.

![A teensy driving a charlieplexed matrix with a heart](https://pbs.twimg.com/media/CspTWUuUsAAnZ2w.jpg:large)

This post is intended as a recipe for getting to this point on debian linux machines.

Download the required toolchains
================================

In order to compile micropython for the teensy, three tools are needed: 
the gcc-arm-embedded toolchain, arduino and the teensyduino project.

To install the gcc-arm-embedded, add the ppa and install with apt-get:

```
sudo add-apt-repository ppa:team-gcc-arm-embedded/ppa
sudo apt-get update
sudo apt-get install gcc-arm-embedded
```
[Download arduino from arduino.cc](https://www.arduino.cc/en/Main/Software) and install using the *install.sh* script.

[Download teensyduino from pjrc.com](http://www.pjrc.com/teensy/td_download.html) and install by making the *TeensyduinoInstall.linux32* binary executable and then running it. You must have arduino previously installed in order for teensyduino to properly install.

Running MicroPython
===================

Download git and clone the micropython repository:

```
sudo apt-get install git
git clone https://github.com/micropython/micropython.git
```

Change directory into teensy:

```
cd teensy
```

Compile the .elf file and .hex file into the build directory:

```
ARDUINO=~/arduino-1.6.11 make
```

Upload the hex file to your teensy. You will need to run this as sudo unless you installed the [teensy udev rules](https://www.pjrc.com/teensy/49-teensy.rules).

```
sudo ARDUINO=~/arduino-1.6.11 make deploy
```

The teensy port of micropython will automatically set the teensy's USB protocol to support a virtual serial port. Once the device is reset, it should show up in *lsusb* as a teensyduino serial port, whereas initially it was listed as *Van Ooijen Technische Informatica Teensy*.

```
$ lsusb
Bus 003 Device 110: ID 16c0:0483 Van Ooijen Technische Informatica Teensyduino Serial 
```

It should also now appear in /dev as a ttyACM device:

```
$ ls /dev/ttyACM*
/dev/ttyACM0
```

If you have multiple ACM devices plugged into your machine, it may enumerate as something other than *ttyACM0*. You can ensure that your teensy always enumerates to the same port using a udev rule. 

To verify that micropython is working, you will need to create a serial connection. I prefer screen as a command-line terminal utility as it requires less set-up than minicom, but both work.

```
sudo apt-get install screen
sudo screen /dev/ttyACM0 115200
```

After pressing the enter key, you should see the familiar three chevrons of the python interpreter. To verify that we can communicate with the teensy's output pins, we can turn on the LED:

```
>>> import pyb
>>> led = pyb.LED(1)
>>> led.on()
```

The Teensy's LED should turn on.

Adding main.py
==============

Now that we've confirmed that micropython can be built and uploaded to the teensy, 
it would be nice to have some persistent code running on the teensy. To do this, 
we need to add some python scripts to our hex. MicroPython looks for two scripts 
- *boot.py* that will execute once on boot (like the setup section of an arduino sketch) 
and *main.py* that executes after boot (like the loop section of an arduino sketch, except 
that it will not run continously unless you have a while True: loop).

Since the teensy does not have a micro SD card like the pyboard, it will not show up as 
removable media. Instead, your scripts must be added to the hex file. The teensy port of 
micropython comes with a script called *add-memzip.sh* that will append these scripts to the 
.hex image that is flashed to the Teensy's flash memory.

To add the python files to the hex, run the script add-memzip.sh between making and deploying:
```
ARDUINO=~/arduino-1.6.11 make
bash add-memzip.sh build/micropython.hex build/micropython.hex path_to_scripts
sudo ARDUINO=~/arduino-1.6.11 make deploy
```


