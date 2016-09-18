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
and 
- *main.py* that executes after boot (like the loop section of an arduino sketch, except 
that it will not run continously unless you have a while True: loop).

Since the teensy does not have a micro SD card like the pyboard, it will not show up as 
removable media. Instead, your scripts must be added to the hex file.

To add the code to the hex, copy the files to the memzip_files folder before making:

```
cp path_to_scripts/* memzip_files
ARDUINO=~/arduino-1.6.11 make
sudo ARDUINO=~/arduino-1.6.11 make deploy
```

The teensy port of micropython comes with a script called *add-memzip.sh* that will append these scripts to the 
.hex image that is flashed to the Teensy's flash memory. I've had varying degrees of luck using this script since merging two incompatible binaries together will brick the hex, but it does cut down on the compile time.

```
bash add-memzip.sh build/micropython.hex build/micropython.hex path_to_scripts
```

A Brief Intro to the Code
=========================

My charlieplex driver is available on github, as part of a [larger demo board project](https://github.com/CatherineH/micropython-teensy-demo/tree/master/src) I'm currently working on. 

The part of this driver that references pyb is the function *pin_state*:

```python
def pin_state(i, state):
    # set pin i to either low (0), high (1) or floating (2). Setting the pin
    # to floating requires setting it as an input pin (and thus has high
    # resistance)
    pin_name = 'D' + str(i)
    if state == 2:
        pin = pyb.Pin(pin_name, pyb.Pin.IN)
    else:
        pin = pyb.Pin(pin_name, pyb.Pin.OUT)
        if state == 0:
            pin.low()
        else:
            pin.high()
```

pyb allows pins to be referenced by string name. You can find a list of pins by executing the code:

```
>>> import pyb
>>> dir(pyb.Pin.board)
['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16', 'D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31', 'D32', 'D33', 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17', 'A18', 'A19', 'A20', 'LED']
```

As you can see, all 34 digital pins and 21 analog pins are available. Pins can be initialized to input or output using:

```python
pin = pyb.Pin(pin_name, pyb.Pin.IN)
pin = pyb.Pin(pin_name, pyb.Pin.OUT)
```

If it is an output pin, it can be set to high or low using:

```python
pin.low()
pin.high()
```

I will document reproducing more of the teensy's features as I continue with this project.

