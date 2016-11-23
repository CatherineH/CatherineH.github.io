---
layout: post
title: "udev Raspbian vs Debian"
description: "aka the teensy doesn't show up in the usb subsystem"
category: programming
tags: [linux, teensy, raspberry pi]
---
{% include JB/setup %}

In order to use a Teensy through a Raspberry Pi's USB ports, you must change the supplied PJRC rule from:

```
SUBSYSTEMS=="usb", ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="04[789ABCD]?", MODE:="0666"
```

to:

```
ATTRS{idVendor}=="16c0", ATTRS{idProduct}=="04[789ABCD]?", MODE:="0666"
```

I'm really not sure why. dmesg looks pretty much the same to me on my Ubuntu 16.04 (xenial) machine:

```
[93358.756212] usb 6-1: new full-speed USB device number 7 using xhci_hcd
[93358.915929] usb 6-1: New USB device found, idVendor=16c0, idProduct=0483
[93358.915939] usb 6-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[93358.915945] usb 6-1: Product: USB Serial
[93358.915949] usb 6-1: Manufacturer: Teensyduino
[93358.915953] usb 6-1: SerialNumber: 1578410
[93358.918104] cdc_acm 6-1:1.0: ttyACM0: USB ACM device
```

as on my Rasbian 6 (jessie):

```
[   88.988423] usb 1-1.4: new full-speed USB device number 5 using dwc_otg
[   89.091861] usb 1-1.4: New USB device found, idVendor=16c0, idProduct=0483
[   89.091882] usb 1-1.4: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[   89.091895] usb 1-1.4: Product: USB Serial
[   89.091908] usb 1-1.4: Manufacturer: Teensyduino
[   89.091921] usb 1-1.4: SerialNumber: 1578410
[   89.133811] cdc_acm 1-1.4:1.0: ttyACM0: USB ACM device
[   89.135216] usbcore: registered new interface driver cdc_acm
[   89.135229] cdc_acm: USB Abstract Control Model driver for USB modems and ISDN adapters
```


