---
layout: post
title: "My Teensy Pipeline"
description: "scripts on scripts on scripts on scripts"
category: programming
tags: [teensy, python, micropython, arduino]
---
{% include JB/setup %}

This post describes my software and scripting pipeline for compiling hex images for the teensy and uploading them to teensies. If you're playing around with arduino or a teensy for the first time, I would not recommend doing this. Instead, [follow PJRC's instructions on using teensyduino](http://www.pjrc.com/teensy/teensyduino.html). 

I went with my own pipeline for a few reasons:

- the arduino IDE is ugly and does not have many features
- I want compile and upload my hex files the same way every time
- Since I often have multiple teensies plugged into a computer at a time, I want to be able target specific teensies by serial number
- I don't want to have to memorize different steps based on whether I'm programming in python, arduino or c
- I want to be able to do all of the above with one command. 

The Components
==============

All components in this pipeline have been compiled for both Windows and Linux, so I have been able to follow the same pipeline on both operating systems.

My pipeline requires the following programs and binaries to be installed on your system for operation:

For arduino code compilation:

- [Arduino Software IDE](https://www.arduino.cc/en/Main/Software), creates the directory structure, and includes the arduino-builder, used for compiling the hex files.
- [Teensyduino beta](https://forum.pjrc.com/threads/38599-Teensyduino-1-31-Beta-2-Available), installs the teensy libraries in the arduino folder, as well as the binaries teensy (the little window that pops up when you upload hex files) to *Arduino folder/hardware/tools/*. If you are using the latest version of Arduino, which I would strongly advise, make sure you download the teensyduino beta instead of the version posted on the main PJRC website.

For C/C++ code and MicroPython:

- gcc-arm-embedded

For MicroPython code compilation:

- [MicroPython](https://github.com/micropython/micropython)

For all code:

- [TyQt](https://github.com/Koromix/ty) is a GUI that offers a few more debug options than the Arduino IDE. It also allows teensies to be targeted by serial number. 

**pyteensy**, my python scripts for compilation/uploading hexs. To install, run:

```
git clone git@github.com:CatherineH/teensy-python-makefile.git
cd teensy-python-makefile
python setup.py install
```

Make sure the following directories are added to your PATH variable:

- $arduino folder$
- $arduino folder$/hardware/tools
- $tyQt folder$/ty/build/$your OS$

on Windows, the arduino folder is usually under C:\Program Files\Arduino.

Using pyteensy
==============

There are two ways to use pyteensy. You can either import it as a module, for example, if you want to encorporate the functionality into your own scripts:

```python
from pyteensy import list_devices

latest_hex = find_hexes()
teensies = list_devices()

for teensy in teensies:
   upload_latest(teensy, latest_hex)
```

or, you can use it from the command line:

```
cd teensy-python-makefile
pyteensy -u -d teensyLC -p test_project_arduino
```

The project *test_project_arduino* in the *teensy-python-makefile* repository contains three common pieces of functionality: digital writing, ADC read, and USB and hardware serial. If it compiles and uploads, then most functionality will work.



