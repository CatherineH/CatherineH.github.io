---
layout: post
title: "arduino builder errors"
description: "ditching the arduino IDE"
category: programming
tags: [arduino, teensy, C]
---
{% include JB/setup %}
My life revolves around three boards: the digi rabbit, an altera FPGA, and a
teensy (an arduino-compatible microcontroller).

The provided IDE's for each of these boards **suck**, but teensy's **sucks the
least**. They are ugly and they get in the way of my productivity. Since the code to interface with the boards 
written in python I've been migrating my digi rabbit and altera
development to PyCharm. This post documents the errors encountered moving from the arduino IDE to the arduino-builder.

`index out of range` on Board Resolver
======================================

 The arduino-builder requires the full board name to be specified as
 something like package_name:platform_name:board_name . The colons are
 essential and the arduino-builder will not check to make sure the full board
  name follows this pattern. If you don't specify the board in that form, you
   will get the error:

```
$ arduino-builder -fqbn teensyLC -hardware ~/arduino-1.6.7/hardware/ -tools ~/arduino-1.6.7/tools experiment_control.ino
panic: runtime error: index out of range

goroutine 1 [running]:
arduino.cc/builder.(*TargetBoardResolver).Run(0x6c3050, 0xc20803c4e0, 0x0, 0x0)
	~/arduino-builder/src/arduino.cc/builder/target_board_resolver.go:46 +0xf44
arduino.cc/builder.(*ContainerSetupHardwareToolsLibsSketchAndProps).Run(0x6c3050, 0xc20803c4e0, 0x0, 0x0)
	~/arduino-builder/src/arduino.cc/builder/container_setup.go:59 +0x6b8
arduino.cc/builder.runCommands(0xc20803c4e0, 0xc20802db90, 0x1d, 0x1d, 0x418001, 0x0, 0x0)
	~/arduino-builder/src/arduino.cc/builder/builder.go:187 +0x139
arduino.cc/builder.(*Builder).Run(0xc20802dd88, 0xc20803c4e0, 0x0, 0x0)
	~/arduino-builder/src/arduino.cc/builder/builder.go:118 +0xef7
arduino.cc/builder.RunBuilder(0xc20803c4e0, 0x0, 0x0)
	~/arduino-builder/src/arduino.cc/builder/builder.go:218 +0x49
main.main()
	~/arduino-builder/main.go:333 +0x1eb2

```

It would be helpful if **target_board_resolver.go** first checked to make
sure your board follows the format required, instead of giving this unhelpful
 error.

Resolution
----------

Change the *-fqbn* parameter to the *package_name:platform_name:board_name*
format. You can guess what this needs to be by looking at the arduino folder
structure. For example, my folder structure has:

```
arduino-1.6.7
└── hardware
    ├── arduino
    └── teensy
        └── avr
            └── boards.txt

```

The *boards.txt* specifies the available boards for that platform. Opening up
 the file, I can see teensy30, teensy31, and so on. If I change the board
 name to **teensy:avr:teensyLC**, the error no longer occurs. Note that this
 string is case sensitive!

Not finding the arm compiler
============================

You may get the error:

```
fork/exec /../arm/bin/arm-none-eabi-g++: no such file or directory
```

Resolution
----------

Set the **-tools** argument to:

```
 -tools ~/arduino-1.6.7/hardware/tools/
```

Missing build variables
=======================

Because we're no longer in the arduino IDE, a bunch of menu-specified 
variables won't be set. This will result in errors like: 

```
<command-line>:0:1: error: macro names must be identifiers
In file included from ~/arduino-1.6.7/hardware/teensy/avr/cores/teensy3/core_pins.h:34:0,
                 from ~/arduino-1.6.7/hardware/teensy/avr/cores/teensy3/wiring.h:33,
                 from ~/arduino-1.6.7/hardware/teensy/avr/cores/teensy3/WProgram.h:15,
                 from ~/arduino-1.6.7/hardware/teensy/avr/cores/teensy3/Arduino.h:1,
                 from /tmp/arduino-sketch-55293F9A6EDF8EF849C232A18F1833A8/sketch/experiment_control.ino.cpp:1:
~/arduino-1.6.7/hardware/teensy/avr/cores/teensy3/kinetis.h:568:12: error: operator '==' has no left operand
 #if (F_CPU == 180000000)
            ^
```
or, alternatively, you may see something like these errors:

```
arm-none-eabi-g++: error: {build.flags.optimize}: No such file or directory
```

Resolution
----------

This is a hack (*build systems people avert your eyes*), but I've added: 

```
teensyLC.build.fcpu=48000000
teensyLC.build.flags.optimize=-Os
teensyLC.build.flags.ldspecs=--specs=nano.specs
teensyLC.build.keylayout=US_ENGLISH
teensyLC.build.usbtype=USB_SERIAL
```

to my **boards.txt** file.
